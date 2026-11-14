"""R4.4: isolate and execute original notebook simulation code cells under extreme inputs.

Read-only for the seven original notebook files. Some tests substitute ONLY initial
state assignment statements in an in-memory copy of a source cell to create zero or
high starting conditions. The update equations and feedback logic are unchanged.
All expected failures are retained as recorded stress-test observations, not hidden.
Research diagnostics are distinct from unit-test framework success.
"""
import csv
import io
import json
import math
import subprocess
import sys
import unittest
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = {
    "P": ("Tourist_Population_Subsystem.ipynb", "7233f7842d91d07e7afe6fb61376484db0bb7a7c", 1, 2, 8, 9),
    "W": ("Environmental_Sanitation_Subsystem.ipynb", "ed078d9ae8465a5d5a76145a2539636b886712e5", 1, 2, 7, 8),
    "R": ("Tourism_Revenue_Subsystem.ipynb", "940d82f00ff80493ef5b2ba88aec93a805548005", 1, 2, 8, 9),
    "F": ("Tourism_Facilities_Availability_Subsystem.ipynb", "2cd90a87f788613133ab3ea72391af689ac87985", 1, 2, 8, 9),
    "S": ("Tourism_Services_Subsystem.ipynb", "39f13c2ffa791e806af18912f5156f60ec89ba6c", 1, 2, None, None),
    "C": ("Cultural_Preservation_Subsystem.ipynb", "769fea7a8c9de00d1695b93e3e73729c9c121ee0", 1, 2, None, None),
    "E": ("Economic_Subsystem_of_the_Local_Community_in_the_Tourism_Sector.ipynb", "d7c687588e811d34a715fd2ad2159d8eb37b6a81", 1, 2, 8, 9),
}
CASE_DESIGNS = [
    ("P01","P",False,30,{"stock_populasi_init":0}, "Zero initial visitors", "Visitor stock remains zero"),
    ("P02","P",False,30,{"rate_bau":0.468}, "Tenfold assumed annual growth", "Finite nonnegative population"),
    ("P03","P",False,1,{"batas_overtourism":0}, "Zero capacity with visitors", "No unhandled denominator failure"),
    ("W01","W",False,30,{"stock_populasi_init":0}, "Zero visitors with initial waste", "No waste generation and backlog clears"),
    ("W02","W",False,30,{"kapasitas_pembersihan_real":0}, "Zero cleaning capacity", "Waste accumulates without cleanup"),
    ("W03","W",False,30,{"stock_sampah":0,"kapasitas_pembersihan_real":10000}, "Zero initial waste, high cleaning", "Waste stock nonnegative and mass-balanced"),
    ("R01","R",False,30,{"avg_tiket_dom":0,"avg_tiket_man":0}, "Zero ticket prices", "Ticket receipts zero"),
    ("R02","R",False,30,{"visitors_init":"zero"}, "Zero visitors with prices", "Ticket receipts zero"),
    ("R03","R",False,30,{"visitors_init":"high"}, "100-fold initial visitors", "Nonnegative finite receipts"),
    ("F01","F",False,30,{"visitors_init":"zero","initial_stock_anggaran":0,"avg_tiket_dom":0,"avg_tiket_man":0}, "Zero visitors, budget and prices", "Procurement zero, existing facilities depreciate"),
    ("F02","F",False,30,{"alokasi_belanja_modal":0}, "Zero capital allocation", "No new procurement"),
    ("F03","F",True,1,{"initial_kapasitas":0}, "Zero facility capacity under intervention", "No unhandled denominator failure"),
    ("S01","S",False,30,{"visitors_init":"zero","initial_stock_anggaran":0}, "Zero visitors and training budget", "No training, skill decays"),
    ("S02","S",False,30,{"initial_stock_anggaran":1e18}, "Extremely high initial budget", "Service skill remains capped at 1000"),
    ("S03","S",False,1,{"biaya_pelatihan_bau":0}, "Zero unit cost of training", "No unhandled denominator failure"),
    ("C01","C",False,30,{"visitors_init":"zero","initial_stock_anggaran":0}, "Zero visitors and preservation budget", "Cultural index decays without revitalization"),
    ("C02","C",False,30,{"initial_stock_anggaran":0}, "Zero initial budget with visitors", "Finite cultural index, endogenous ticket revenue possible"),
    ("C03","C",False,30,{"initial_stock_anggaran":1e18}, "Extremely high budget", "Culture index bounded at 100"),
    ("E01","E",False,1,{"visitors_init":"zero","initial_pkl":0}, "Zero visitors and zero starting vendors", "No spontaneous vendor creation"),
    ("E02","E",False,30,{"visitors_init":"zero","initial_pkl":200}, "Zero visitors, 200 vendors", "Gross revenue zero, vendors decrease"),
    ("E03","E",True,30,{"visitors_init":"high","kuota_maksimal_pkl":450}, "100-fold visitors and vendor quota", "Vendors at most 450, receipts finite"),
]
VIS_BAU = "curr_dom_bau, curr_man_bau = dom_2023 / 365, man_2023 / 365"
VIS_INT = "curr_dom_int, curr_man_int = dom_2023 / 365, man_2023 / 365"

def get_original_cells(prefix):
    fn,sha,*_ = SRC[prefix]
    p=ROOT/fn
    assert p.is_file(), fn
    actual = subprocess.check_output(["git","hash-object",str(p)],text=True).strip()
    assert actual == sha, "Original source modified: %s: %s != %s" % (fn,actual,sha)
    nb = json.loads(p.read_text(encoding="utf-8"))
    return p,nb,sha

def cell(nb,n):
    x=nb["cells"][n]["source"]
    return "".join(x) if isinstance(x,list) else x

def run_case(row):
    caseid,prefix,intervention,days,inputs,description,expected=row
    p,nb,sha = get_original_cells(prefix)
    _,_,bau_cfg,bau_engine,int_cfg,int_engine=SRC[prefix]
    cfg=cell(nb,int_cfg if intervention and int_cfg is not None else bau_cfg)
    engine_idx=int_engine if intervention and int_engine is not None else bau_engine
    code=cell(nb,engine_idx)
    ns={"__name__":"__r44_test__"}
    exec(compile(cell(nb,0),str(p)+":cell0","exec"),ns)
    exec(compile(cfg,str(p)+":config","exec"),ns)
    ns["start_date"]=date(2026 if intervention else 2025,1,1)
    ns["end_date"]=ns["start_date"]+timedelta(days=days-1)
    ns["days"]=days
    notes=[]
    for k,v in inputs.items():
        if k == "stock_populasi_init":
            old="stock_populasi = 1009.6"
            new="stock_populasi = "+repr(float(v))
            assert code.count(old)==1,(caseid,old,code.count(old))
            code=code.replace(old,new,1)
            notes.append("in-memory initialization override: "+old+" => "+new)
        elif k == "visitors_init":
            if v == "zero": repl="0.0, 0.0"
            elif v == "high": repl="90000.0, 3600.0"
            else: raise AssertionError("unsupported visitor input")
            found=0
            for old in (VIS_BAU,VIS_INT):
                if old in code:
                    code=code.replace(old,old.split("=")[0]+"= "+repl,1)
                    found+=1
            assert found>=1,(caseid,"visitor assignment not found",code[:400])
            notes.append("in-memory visitor initial-state override to "+v+" ("+str(found)+" assignments)")
        else:
            assert k in ns,(caseid,"config parameter missing",k)
            ns[k]=v
            notes.append("namespace parameter override "+k+"="+str(v))
    error=None
    try:
        exec(compile(code,str(p)+":cell"+str(engine_idx)+"("+caseid+")","exec"),ns)
    except Exception as exc:
        error=type(exc).__name__+": "+str(exc)
    actual={}
    try:
        if prefix=="P":
            seq=ns.get("history_populasi",[])
            actual={"visitors_last":seq[-1] if seq else None,
                    "visitors_min":min(seq) if seq else None,
                    "reputation_last":ns.get("reputasi_destinasi")}
            if caseid=="P01": passed=error is None and len(seq)==days and seq[-1]==0
            elif caseid=="P02":passed=error is None and len(seq)==days and all(math.isfinite(x) and x>=0 for x in seq)
            else:passed=error is None
        elif prefix=="W":
            g=ns.get("data_timbulan",[])
            cl=ns.get("data_pembersihan",[])
            st=ns.get("data_stock",[])
            actual={"waste_generated":sum(g),"waste_cleaned":sum(cl),
                    "waste_stock_last":st[-1] if st else None}
            if caseid=="W01":passed=error is None and len(g)==days and sum(g)==0 and st[-1]==0
            elif caseid=="W02":passed=error is None and len(g)==days and sum(cl)==0 and st[-1]>500
            else:passed=error is None and len(g)==days and st[-1]>=0 and abs(st[-1]-(0+sum(g)-sum(cl)))<1e-5
        elif prefix=="R":
            seq=ns.get("data_revenue_daily",[])
            actual={"annualized_receipts_last":seq[-1] if seq else None}
            if caseid in ("R01","R02"):passed=error is None and len(seq)==days and all(x==0 for x in seq)
            else:passed=error is None and len(seq)==days and all(math.isfinite(x) and x>=0 for x in seq)
        elif prefix=="F":
            seq=ns.get("data_cap_int" if intervention else "data_kapasitas",[])
            actual={"capacity_last":seq[-1] if seq else None,
                    "budget_last":ns.get("budget_int" if intervention else "stock_anggaran")}
            if caseid=="F01":passed=error is None and len(seq)==days and seq[-1]<2752 and ns.get("stock_anggaran")==0
            elif caseid=="F02":passed=error is None and len(seq)==days and seq[-1]<2752
            else:passed=error is None
        elif prefix=="S":
            seq=ns.get("data_indeks_bau",[])
            actual={"service_index_last":seq[-1] if seq else None,"skill_last":ns.get("skill_bau")}
            if caseid=="S01":passed=error is None and len(seq)==days and seq[-1]<71.2
            elif caseid=="S02":passed=error is None and len(seq)==days and seq[-1]==100
            else:passed=error is None
        elif prefix=="C":
            seq=ns.get("data_culture_bau",[])
            actual={"culture_index_last":seq[-1] if seq else None}
            if caseid=="C01":passed=error is None and len(seq)==days and 0<seq[-1]<80 and ns.get("budget_bau")==0
            elif caseid=="C02":passed=error is None and len(seq)==days and 0<=seq[-1]<=100
            else:passed=error is None and len(seq)==days and seq[-1]==100
        elif prefix=="E":
            count=ns.get("data_pkl_int" if intervention else "data_pkl_bau",[])
            gross=ns.get("data_inc_int" if intervention else "data_inc_bau",[])
            actual={"vendors_last":count[-1] if count else None,
                    "gross_per_vendor_last":gross[-1] if gross else None}
            if caseid=="E01":passed=error is None and len(count)==days and count[-1]==0
            elif caseid=="E02":passed=error is None and len(count)==days and count[-1]<200 and all(x==0 for x in gross)
            else:passed=error is None and len(count)==days and count[-1]<=450 and all(math.isfinite(x) for x in gross)
        else:
            raise AssertionError(prefix)
    except Exception as evaluation_error:
        passed=False
        actual["evaluation_error"]=repr(evaluation_error)
    if error is not None:passed=False
    return dict(case_id=caseid,subsystem=prefix,source_notebook=p.name,source_blob_sha=sha,
                config_cell=(int_cfg if intervention and int_cfg is not None else bau_cfg),
                engine_cell=engine_idx,days=days,description=description,
                inputs=inputs,expected=expected,actual=actual,error=error,
                status="PASS" if passed else "FAIL",intervention=intervention,
                overrides=notes,method="Original GitHub source cell execution with recorded input overrides")

class OriginalNotebookSourceExtremeTests(unittest.TestCase):
    def test_original_source_extreme_screening(self):
        rows=[]
        for spec in CASE_DESIGNS:
            r=run_case(spec)
            rows.append(r)
            print("R44_RESULT "+json.dumps(r,sort_keys=True,default=str),flush=True)
        summary={"n_cases":len(rows),"pass":sum(r["status"]=="PASS" for r in rows),
                 "fail":sum(r["status"]=="FAIL" for r in rows),
                 "cases_with_input_initialization_override":sum(any("in-memory" in x for x in r["overrides"]) for r in rows),
                 "source_method":"GitHub-verified original source cells, with recorded in-memory test input changes",
                 "no_original_notebook_modified":True}
        print("R44_SUMMARY "+json.dumps(summary,sort_keys=True),flush=True)
        self.assertEqual(len(rows),21)
        self.assertEqual({r["case_id"] for r in rows},{s[0] for s in CASE_DESIGNS})
        self.assertEqual(len({r["source_notebook"] for r in rows}),7)
        self.assertTrue(all(r["status"] in ("PASS","FAIL") for r in rows))

if __name__ == "__main__":
    unittest.main(verbosity=2)
