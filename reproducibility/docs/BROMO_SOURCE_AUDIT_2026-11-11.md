# Bromo source audit — 11 November 2026, stage 1

**Status:** This is a NEW, provisional source-anchored annual-mean scenario, not a reproduction of the historical seven-system simulation or Figures 5–8. Original notebook versions are preserved by Git history at commit `d68f19a7a52b899bd704c16537ddfdd053855180`.

## Source-verified quantities

| Quantity | Observed value | Scope and primary reporting evidence |
|---|---:|---|
| 2023 Bromo arrivals | 368,507 = 355,297 domestic + 13,210 foreign | Full year; [BB TNBTS cited by ANTARA (2024)](https://www.antaranews.com/berita/3930348/kunjungan-wisatawan-ke-bromo-pada-2023-) |
| 2024 Bromo arrivals | 485,696 = **465,770** domestic + 19,926 foreign | Full leap year; [BB TNBTS cited by ANTARA (2025)](https://www.antaranews.com/berita/4895561/tnbts-memperketat-pengawasan-di-bromo-cegah-masuknya-wisatawan-ilegal) |
| 2025 H1 Bromo arrivals | 321,732 = 309,564 domestic + 12,168 foreign | **1 January–30 June only**; [BB TNBTS cited by ANTARA (9 July 2025)](https://www.antaranews.com/berita/4954825/tnbts-catat-kunjungan-wisatawan-ke-bromo-di-semester-i-2025-meningkat) |
| 2023 PNBP | IDR 14.70 billion | Observed non-tax government revenue, not tourism vendor receipts; [ANTARA](https://www.antaranews.com/berita/3930348/kunjungan-wisatawan-ke-bromo-pada-2023-) |
| 2024 PNBP | IDR 21.15 billion | Observed non-tax government revenue, not model gross ticket receipts; [ANTARA](https://www.antaranews.com/berita/4895561/tnbts-memperketat-pengawasan-di-bromo-cegah-masuknya-wisatawan-ilegal) |
| Operational quota cited in 2024 | 2,752 entrants/day | Changeable **admission-management quota**, not an ecological carrying-capacity determination; [ANTARA](https://www.antaranews.com/berita/4046541/balai-besar-tnbts-belum-tambah-kuota-wisatawan-saat-libur-lebaran) |
| Temporary quota 11–15 April 2024 | 5,504 entrants/day | Temporary management policy; [ANTARA](https://www.antaranews.com/berita/4056318/kunjungan-wisatawan-ke-bromo-capai-8308-orang-saat-libur-lebaran-2024) |
| Ticket rates from **30 October 2024** | domestic weekdays IDR 54,000; domestic holidays IDR 79,000; foreign IDR 255,000 | Rates include insurance components; [Official TNBTS announcement](https://bromotenggersemeru.org/article/pengumuman-penyesuaian-tarif-tnbts-sesuai-pp-36-tahun-2024/) |

## Main corrections and limitations

1. Seven legacy notebooks share inconsistent visitor inputs. The frequent historical value **465,751** for 2024 domestic admissions differs from the independently reported **465,770** by 19 people. Fix it before any full original-equation rerun.
2. The former 2025 estimate `390487 * (12 / 9)` and `13300 * (12 / 9)` is **not** a verified calendar-year observation. Only 2025 H1 is sourced here. **Do not** replace annual 2025 data with a six-month count.
3. Annual admissions divided by the number of calendar days give an **annual-average admissions/day proxy** (2024 denominator **366**), not a measured time series or count of people currently staying in the park.
4. Quota 2,752/day is an **operational reference for 2024**, not fixed ecological capacity. The temporary 5,504/day quota is not a permanent ecological increase.
5. Assumptions inherited from historical notebooks (4.68% BAU growth, 3.5% intervention growth, -0.504 price elasticity, 1.08/1.25 ticket-price multipliers, 5/7 weekday weighting) remain **unverified scenario inputs**. Neither elasticity nor the resulting growth trajectories is an observed Bromo estimate.
6. The new script calculates **hypothetical nominal gross entrance-ticket revenue**, not observed PNBP, since the latter includes different components and the assumed ticket blend lacks transaction-level supporting data.
7. Source/estimate contamination in older placeholder-MAPE cells (including service, cultural, waste, facility and vendor indices) means the historical 6.45% multi-subsystem MAPE is **not established as independent predictive validation**. New MAPE must use matched observed/model variables and independent reference observations.
8. The new provisional comparison reports **annual-mean quota-reference crossing year**, not the old exact daily dates in 2038/2039 or a cultural/ecological crisis date. Keep revised graphics distinct from manuscript Figures 5–8 until verified.

## Reproduce stage-1 code

```bash
python -m pip install -r reproducibility/requirements.txt
python -m unittest discover -s reproducibility/tests -v
python reproducibility/scripts/source_grounded_bromo_scenario.py
```

Outputs under `reproducibility/outputs/source-grounded/` contain observed-aggregate and assumed-scenario CSVs and a **new illustrative figure**. These outputs do not overwrite root notebooks or original manuscript figures. They introduce **no raw individual reviews, personally identifying information or tokens**.

## Follow-up consistency audit

- **Methods**: periods, separate corpus and Bromo simulation scopes, observed vs assumed inputs, independent validity.
- **Supplementary**: input-source table, annual/historical calibration evidence, elasticity/sensitivity, MAPE claims and repeated tables.
- **Figures**: correct operational-quota label and units for visitor/facility graphs; separate actual PNBP from hypothetical ticket revenue; re-run original equations before replacing Figures 5–8.
- **Pending empirical source needs**: observed garbage generation/handling, facility capacity units, cultural index, visitor-service quality, informal-vendor income, and historical calibration series.

**No claim of full seven-subsystem correction or figure replication is made by stage 1.**
