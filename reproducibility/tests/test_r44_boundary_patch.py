"""R4.4 boundary guards applied to in-memory copies of original source cells.

No original notebook bytes are modified. These patches are candidate corrections for
source-domain stress tests and must not be called empirical validation.
"""
from pathlib import Path
import json, math, unittest, subprocess
from datetime import date, timedelta
from test_r44_original_source_extreme import SRC, get_original_cells, cell

REPLACEMENTS = {
"P": {
  2: [(
"""    rasio_kepadatan = stock_populasi / batas_overtourism

    if rasio_kepadatan > 1.0:
        # Semakin kebablasan, penaltinya semakin terasa, tapi awalnya sangat kecil
        penalti_dinamis = (rasio_kepadatan - 1.0) * 0.0004
        reputasi_destinasi -= penalti_dinamis

    # Batas bawah reputasi dipasang di 0.80 (80%) agar tidak terjun bebas
    # Ini yang membuat grafik turunnya melandai perlahan
    reputasi_destinasi = max(0.80, reputasi_destinasi)""",
"""    if batas_overtourism <= 0:
        # Closure: no new admissions, current visitors may depart.
        reputasi_destinasi = 0.0
    else:
        rasio_kepadatan = stock_populasi / batas_overtourism
        if rasio_kepadatan > 1.0:
            penalti_dinamis = (rasio_kepadatan - 1.0) * 0.0004
            reputasi_destinasi -= penalti_dinamis
        reputasi_destinasi = max(0.80, reputasi_destinasi)""")]
},
"F": {
 9: [(
"""    if pop_int > cap_int: reputasi_int -= (pop_int / cap_int - 1.0) * 0.0004
    reputasi_int = max(0.80, reputasi_int)""",
"""    if cap_int <= 0:
        # Closure: do not divide by zero or generate new arrivals.
        reputasi_int = 0.0
    else:
        if pop_int > cap_int:
            reputasi_int -= (pop_int / cap_int - 1.0) * 0.0004
        reputasi_int = max(0.80, reputasi_int)""")]
},
"S": {
 2: [
 ("    trained_bau = anggaran_pelatihan_bau / biaya_pelatihan_bau",
  "    trained_bau = anggaran_pelatihan_bau / biaya_pelatihan_bau if biaya_pelatihan_bau > 0 else 0.0"),
 ("    trained_int = anggaran_pelatihan_int / biaya_curr",
  "    trained_int = anggaran_pelatihan_int / biaya_curr if biaya_curr > 0 else 0.0")
 ]
},
"E": {
 2: [("pkl_bau = max(10, pkl_bau + in_bau - out_bau)",
      "pkl_bau = max(0, pkl_bau + in_bau - out_bau)")],
 9: [
 ("pkl_bau = max(10, pkl_bau + in_bau_pkl - out_bau_pkl)",
  "pkl_bau = max(0, pkl_bau + in_bau_pkl - out_bau_pkl)"),
 ("pkl_int = min(kuota_maksimal_pkl, max(10, pkl_int + in_int_pkl - out_int_pkl))",
  "pkl_int = min(kuota_maksimal_pkl, max(0, pkl_int + in_int_pkl - out_int_pkl))"),
 ("pkl_int = max(10, pkl_int + in_int_pkl - out_int_pkl)",
  "pkl_int = max(0, pkl_int + in_int_pkl - out_int_pkl)")
 ]
}
}

def patched_source(prefix,index,source):
    for old,new in REPLACEMENTS.get(prefix,{}).get(index,[]):
        if source.count(old)!=1:
            raise ValueError("patch unique anchor mismatch: "+prefix+" cell "+str(index)+", count="+str(source.count(old)))
        source=source.replace(old,new,1)
    return source

def run_engine(prefix,intervention,patched,caseid=None):
    _,nb,_=get_original_cells(prefix)
    _,_,bc,be,ic,ie=SRC[prefix]
    cfg=ic if intervention and ic is not None else bc
    eng=ie if intervention and ie is not None else be
    ns={"__name__":"__r44_guarded__"}
    exec(cell(nb,0),ns)
    exec(cell(nb,cfg),ns)
    code=patched_source(prefix,eng,cell(nb,eng)) if patched else cell(nb,eng)
    if caseid:
        if caseid=="P03":
            ns["batas_overtourism"]=0
            ns["days"]=1
            ns["end_date"]=ns["start_date"]
        if caseid=="F03":
            ns["initial_kapasitas"]=0
            ns["days"]=1
            ns["end_date"]=ns["start_date"]
        if caseid=="S03":
            ns["biaya_pelatihan_bau"]=0
            ns["days"]=1
            ns["end_date"]=ns["start_date"]
        if caseid=="E01":
            ns["initial_pkl"]=0
            ns["days"]=1
            ns["end_date"]=ns["start_date"]
            code=code.replace("curr_dom_bau, curr_man_bau = dom_2023 / 365, man_2023 / 365", "curr_dom_bau, curr_man_bau = 0.0, 0.0",1)
    exec(code,ns)
    # Numeric outputs as built by original engines.
    if prefix=="P":return [ns["total_bau"][-1],ns["total_int"][-1]] if intervention else [ns["history_populasi"][-1],ns["history_reputasi"][-1]]
    if prefix=="W":return [ns["data_timbulan"][-1],ns["data_pembersihan"][-1],ns.get("data_stock",[0])[-1] if not intervention else ns["data_kapasitas_int"][-1]]
    if prefix=="R":return [ns["rev_bau_daily"][-1],ns["rev_int_daily"][-1]] if intervention else [ns["data_revenue_daily"][-1]]
    if prefix=="F":return [ns["data_vis_int"][-1],ns["data_cap_int"][-1]] if intervention else [ns["data_visitors"][-1],ns["data_kapasitas"][-1]]
    if prefix=="S":return [ns["data_indeks_bau"][-1],ns["data_indeks_int"][-1]]
    if prefix=="C":return [ns["data_culture_bau"][-1],ns["data_culture_int"][-1]]
    if prefix=="E":return [ns["data_pkl_int"][-1],ns["data_inc_int"][-1]] if intervention else [ns["data_pkl_bau"][-1],ns["data_inc_bau"][-1]]
    raise AssertionError(prefix)

class R44BoundaryPatchEvaluation(unittest.TestCase):
    def test_original_baselines_unchanged(self):
        count=0
        for prefix in "PWRFSCE":
            for intervention in ([False,True] if prefix in ("P","W","R","F","E") else [False]):
                try:
                    original=run_engine(prefix,intervention,False)
                    corrected=run_engine(prefix,intervention,True)
                    same=all(math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-9) for a,b in zip(original,corrected))
                    print("R44_BASELINE "+json.dumps({"prefix":prefix,"intervention":intervention,"original":original,"patched":corrected,"same":same}),flush=True)
                    self.assertTrue(same)
                    count+=1
                except Exception as e:
                    print("R44_BASELINE_EXCEPTION "+json.dumps({"prefix":prefix,"intervention":intervention,"error":str(e)}),flush=True)
                    raise
        self.assertEqual(count,12)
    def test_boundary_stress_cases_after_patch(self):
        for cid,prefix,intervention in [("P03","P",False),("F03","F",True),("S03","S",False),("E01","E",False)]:
            val=run_engine(prefix,intervention,True,caseid=cid)
            print("R44_PATCHED_EXTREME "+json.dumps({"case_id":cid,"outputs":val,"finite":all(math.isfinite(v) for v in val)}),flush=True)
            self.assertTrue(all(math.isfinite(v) for v in val))
            if cid=="E01":self.assertEqual(val[0],0.0)
            if cid=="S03":self.assertLess(val[0],71.2)
if __name__ == "__main__":
    unittest.main(verbosity=2)
