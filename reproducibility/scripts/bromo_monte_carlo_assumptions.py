"""Assumption-conditioned Monte Carlo for Bromo annual-mean visitor demand and
separate cultural-index bookkeeping from manuscript Figures 6 and 8.

NOT a Monte Carlo of an empirically validated seven-stock model. Triangular or
uniform ranges are hypothetical and independently sampled (uncalibrated).
"""
import argparse
import json
from pathlib import Path
from calendar import isleap
import numpy as np
import pandas as pd

BASE_DOM, BASE_FOR = 465770 / 366, 19926 / 366
REF_VISITORS, REF_CULTURE = 2752, 60.
BASE_DOM_PRICE = (5 * 54000 + 2 * 79000) / 7
BASE_FOR_PRICE = 255000
START_BUDGET = 3976500000.
ABSORPTION_PER_DAY = 1 - (1 - .90) ** (1 / 365)


def simulate(n=10000, seed=20261113, stochastic=True, distribution="triangular"):
    """Crossing at first YEAR with annual mean admissions >= 2752; culture < 60
    at end-year. Missing crossings through 2045 are -1, never 2046.
    """
    rng = np.random.default_rng(seed)

    def tri(base, variation=.2):
        if not stochastic:
            return np.full(n, float(base))
        if distribution == "triangular":
            multiplier = rng.triangular(1-variation, 1, 1+variation, size=n)
        elif distribution == "uniform":
            multiplier = rng.uniform(1-variation, 1+variation, size=n)
        else:
            raise ValueError("distribution must be triangular or uniform")
        return base * multiplier

    growth_bau = tri(.0468, .10)
    growth_int = tri(.035, .10)
    elasticity = tri(-.504, .20)
    initial_culture = tri(80., .05)
    annual_erosion = tri(.005, .20)
    visitor_pressure = tri(.0000045, .20)
    restoration_cost = tri(350e6, .20)
    share_bau = tri(.005, .20)
    share_int = tri(.025, .20)
    erosion_daily = 1 - (1 - annual_erosion) ** (1 / 365)

    dom_bau, for_bau = np.full(n, BASE_DOM), np.full(n, BASE_FOR)
    dom_int, for_int = dom_bau.copy(), for_bau.copy()
    culture_bau, culture_int = initial_culture.copy(), initial_culture.copy()
    budget_bau = np.full(n, START_BUDGET)
    budget_int = np.full(n, START_BUDGET)
    cross_bau_visit = np.full(n, -1, dtype=int)
    cross_int_visit = np.full(n, -1, dtype=int)
    cross_bau_culture = np.full(n, -1, dtype=int)
    cross_int_culture = np.full(n, -1, dtype=int)
    snapshots = []

    for year in range(2025, 2046):
        dom_bau *= 1 + growth_bau
        for_bau *= 1 + growth_bau
        if year == 2025:
            dom_int, for_int = dom_bau.copy(), for_bau.copy()
        else:
            dom_int *= 1 + growth_int
            for_int *= 1 + growth_int
            if year == 2026:
                dom_int *= 1 + elasticity * .08
                for_int *= 1 + elasticity * .25
        admissions_bau = dom_bau + for_bau
        admissions_int = dom_int + for_int
        cross_bau_visit[(cross_bau_visit == -1) & (admissions_bau >= REF_VISITORS)] = year
        cross_int_visit[(cross_int_visit == -1) & (admissions_int >= REF_VISITORS)] = year
        ticket_bau = dom_bau * BASE_DOM_PRICE + for_bau * BASE_FOR_PRICE
        ticket_int = (dom_int * BASE_DOM_PRICE * (1.08 if year >= 2026 else 1)
                      + for_int * BASE_FOR_PRICE * (1.25 if year >= 2026 else 1))
        active_int_share = share_int if year >= 2026 else share_bau
        for _ in range(366 if isleap(year) else 365):
            spent_bau = budget_bau * ABSORPTION_PER_DAY
            spent_int = budget_int * ABSORPTION_PER_DAY
            budget_bau = np.maximum(0, budget_bau + .85 * ticket_bau - spent_bau)
            budget_int = np.maximum(0, budget_int + .85 * ticket_int - spent_int)
            culture_bau = np.clip(culture_bau + spent_bau * share_bau / restoration_cost
                                  - culture_bau * erosion_daily
                                  - admissions_bau * visitor_pressure, 0, 100)
            culture_int = np.clip(culture_int + spent_int * active_int_share / restoration_cost
                                  - culture_int * erosion_daily
                                  - admissions_int * visitor_pressure, 0, 100)
        cross_bau_culture[(cross_bau_culture == -1) & (culture_bau < REF_CULTURE)] = year
        cross_int_culture[(cross_int_culture == -1) & (culture_int < REF_CULTURE)] = year
        snapshots.extend([
            {"year":year,"scenario":scenario,"indicator":indicator,
             "p05":float(np.percentile(values,5)),
             "median":float(np.median(values)),
             "p95":float(np.percentile(values,95))}
            for scenario, pairs in [
                ("BAU",[("annual_mean_admissions_day",admissions_bau),
                        ("culture_index_end_year",culture_bau)]),
                ("Intervention",[("annual_mean_admissions_day",admissions_int),
                                 ("culture_index_end_year",culture_int)])
            ]
            for indicator, values in pairs])

    draws = pd.DataFrame({
        "bau_growth":growth_bau,"intervention_growth":growth_int,
        "demand_elasticity":elasticity,"initial_culture_index":initial_culture,
        "annual_culture_erosion":annual_erosion,
        "culture_pressure_per_admission":visitor_pressure,
        "restoration_cost_idr_per_point":restoration_cost,
        "bau_culture_budget_share":share_bau,
        "intervention_culture_budget_share":share_int,
        "bau_visitor_crossing_year":cross_bau_visit,
        "intervention_visitor_crossing_year":cross_int_visit,
        "bau_culture_crossing_year":cross_bau_culture,
        "intervention_culture_crossing_year":cross_int_culture,
    })
    return draws, pd.DataFrame(snapshots)


def describe(draws):
    out = {}
    for indicator in ["bau_visitor","intervention_visitor",
                      "bau_culture","intervention_culture"]:
        crossed = draws.loc[draws[indicator+"_crossing_year"] >= 0,
                            indicator+"_crossing_year"].to_numpy()
        out[indicator] = {
            "n":len(draws),"crossed_by_2045":int(len(crossed)),
            "not_crossed_by_2045":int(len(draws)-len(crossed)),
            "crossing_share_pct":round(100*len(crossed)/len(draws),2),
            "crossing_year_p05_conditional":float(np.percentile(crossed,5)) if len(crossed) else None,
            "crossing_year_median_conditional":float(np.median(crossed)) if len(crossed) else None,
            "crossing_year_p95_conditional":float(np.percentile(crossed,95)) if len(crossed) else None,
            "earliest_crossing_year":int(crossed.min()) if len(crossed) else None,
            "latest_crossing_year":int(crossed.max()) if len(crossed) else None,
        }
    return out


def plot_envelopes(snapshots, filename, distribution="triangular"):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MaxNLocator
    fig, axes = plt.subplots(2,1,figsize=(11,8),sharex=True)
    for ax, indicator, ref, ylabel in [
        (axes[0],"annual_mean_admissions_day",REF_VISITORS,"Annual-mean admissions / day"),
        (axes[1],"culture_index_end_year",REF_CULTURE,"Modeled cultural index (0–100)")]:
        for scenario,color,linestyle in [
            ("BAU","#283b50","-"),("Intervention","#a7583c","--")]:
            d = snapshots.loc[(snapshots.indicator==indicator)&(snapshots.scenario==scenario)]
            years=d.year.to_numpy(dtype=float)
            ax.plot(years,d["median"],label=f"{scenario} median",color=color,lw=2,linestyle=linestyle)
            ax.fill_between(years,d["p05"].to_numpy(dtype=float),
                            d["p95"].to_numpy(dtype=float),color=color,
                            alpha=.16,label=f"{scenario} assumed 5–95% envelope")
        ax.axhline(ref,color="black",linestyle=":",lw=1.5,label="Scenario reference")
        ax.set_ylabel(ylabel); ax.grid(alpha=.17)
        ax.spines[["top","right"]].set_visible(False)
        ax.legend(loc="best",fontsize=8,ncol=2)
    axes[0].set_title("(a) Annual-average visitor-demand scenarios")
    axes[1].set_title("(b) Modeled cultural sustainability at year-end")
    axes[1].set_xlabel("Year")
    axes[1].xaxis.set_major_locator(MaxNLocator(integer=True,nbins=11))
    fig.text(.5,.012,
        f"Assumed independent {distribution} ranges; not empirically calibrated prediction intervals.",
        ha="center",va="bottom",fontsize=8)
    fig.tight_layout(rect=[0,.03,1,1])
    fig.savefig(filename,dpi=300,bbox_inches="tight")
    plt.close(fig)


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--n",type=int,default=10000)
    p.add_argument("--seed",type=int,default=20261113)
    p.add_argument("--output-dir",default="reproducibility/outputs/monte-carlo-2026-11-13")
    p.add_argument("--distribution",choices=["triangular","uniform"],default="triangular")
    args=p.parse_args()
    if args.n<1:p.error("--n must be >= 1")
    output=Path(args.output_dir);output.mkdir(parents=True,exist_ok=True)
    draws,snapshots=simulate(n=args.n,seed=args.seed,distribution=args.distribution)
    summary=describe(draws)
    draws.to_csv(output/"assumption_conditioned_mc_draws.csv",
                 index=False,float_format="%.12g")
    snapshots.to_csv(output/"assumption_conditioned_mc_trajectories.csv",
                     index=False,float_format="%.6f")
    (output/"assumption_conditioned_mc_summary.json").write_text(json.dumps({
        "n":args.n,"seed":args.seed,"distribution":args.distribution,
        "status":"assumed independent bounded distributions; not empirically calibrated",
        "reference_visitor_admissions_per_day":REF_VISITORS,
        "reference_culture_index":REF_CULTURE,"summary":summary},indent=2)+"\n",
        encoding="utf-8")
    plot_envelopes(snapshots,output/"assumption_conditioned_mc_envelopes.png",
                   distribution=args.distribution)
    for name,record in summary.items():print(name,record)
    print("Files:",output)


if __name__=="__main__":
    main()
