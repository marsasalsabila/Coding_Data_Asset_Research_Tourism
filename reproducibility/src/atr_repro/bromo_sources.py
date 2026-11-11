"""Bromo source observations and PROVISIONAL annual-mean scenarios, not validation."""
from calendar import isleap
from datetime import date

# Admission counts are yearly totals, NOT daily time series or on-site stocks.
OBSERVED_VISITS = {
    2023: {"domestic": 355297, "foreign": 13210, "total": 368507},
    2024: {"domestic": 465770, "foreign": 19926, "total": 485696},
}
OBSERVED_VISITS_2025_H1 = {"domestic": 309564, "foreign": 12168, "total": 321732}
OBSERVED_PNBP_IDR = {2023: 14_700_000_000, 2024: 21_150_000_000}
OPERATIONAL_QUOTA_2024_PER_DAY = 2752
APR_11_TO_15_2024_TEMPORARY_QUOTA_PER_DAY = 5504
TARIFF_EFFECTIVE = date(2024, 10, 30)
TARIFF_IDR = {"domestic_weekday": 54000, "domestic_holiday": 79000, "foreign": 255000}

def audit_sources():
    for row in list(OBSERVED_VISITS.values()) + [OBSERVED_VISITS_2025_H1]:
        if row["domestic"] < 0 or row["foreign"] < 0 or row["total"] != row["domestic"] + row["foreign"]:
            raise ValueError("Unreconciled Bromo admissions")

def daily_annual_average(year):
    """Arithmetic annual admissions/day proxy; not measured daily admissions."""
    audit_sources()
    return OBSERVED_VISITS[year]["total"] / (366 if isleap(year) else 365)

def daily_2025_first_half_average():
    """Only Jan 1–Jun 30 (181 days), NOT the full calendar year."""
    audit_sources()
    return OBSERVED_VISITS_2025_H1["total"] / 181

def scenario_row(year, bau_growth=0.0468, intervention_growth=0.035,
                 assumed_elasticity=-0.504, domestic_price_factor=1.08,
                 foreign_price_factor=1.25, intervention_year=2026,
                 weekday_weight=5/7):
    """Conditional scenario from verified FULL-YEAR 2024, without annualizing H1 2025.
    BAU growth, post-intervention growth, elasticity, price multipliers and day-mix
    are explicitly ASSUMED, not empirical estimators. Ticket receipts are gross
    nominal scenario amounts (ticket face prices include insurance), NOT PNBP.
    """
    audit_sources()
    if year < 2025 or intervention_year < 2025:
        raise ValueError("Projections start after the last confirmed annual observation")
    if min(1+bau_growth, 1+intervention_growth, domestic_price_factor,
           foreign_price_factor) <= 0 or not 0 <= weekday_weight <= 1:
        raise ValueError("Invalid growth, price factor or weekday share")
    base_dom = OBSERVED_VISITS[2024]["domestic"] / 366
    base_for = OBSERVED_VISITS[2024]["foreign"] / 366
    elapsed = year - 2024
    bau_dom = base_dom * (1 + bau_growth) ** elapsed
    bau_for = base_for * (1 + bau_growth) ** elapsed
    if year < intervention_year:
        int_dom, int_for = bau_dom, bau_for
    else:
        before = intervention_year - 2025
        after = year - intervention_year + 1
        dom_response = 1 + assumed_elasticity * (domestic_price_factor - 1)
        for_response = 1 + assumed_elasticity * (foreign_price_factor - 1)
        if min(dom_response, for_response) < 0:
            raise ValueError("Assumed linear response implies negative admissions")
        int_dom = base_dom * (1 + bau_growth) ** (before + 1) * (1 + intervention_growth) ** after * dom_response
        int_for = base_for * (1 + bau_growth) ** (before + 1) * (1 + intervention_growth) ** after * for_response
        if intervention_year > 2025:
            int_dom /= (1 + bau_growth)
            int_for /= (1 + bau_growth)
    blended_dom_ticket = (weekday_weight * TARIFF_IDR["domestic_weekday"]
                          + (1-weekday_weight) * TARIFF_IDR["domestic_holiday"])
    dom_price = domestic_price_factor if year >= intervention_year else 1
    for_price = foreign_price_factor if year >= intervention_year else 1
    calendar_days = 366 if isleap(year) else 365
    return {
        "year": year,
        "bau_annual_mean_admissions_per_day": bau_dom + bau_for,
        "intervention_annual_mean_admissions_per_day": int_dom + int_for,
        "bau_implied_annual_admissions": (bau_dom + bau_for)*calendar_days,
        "intervention_implied_annual_admissions": (int_dom + int_for)*calendar_days,
        "historical_2024_operational_quota_per_day": OPERATIONAL_QUOTA_2024_PER_DAY,
        "bau_hypothetical_gross_tickets_idr": (bau_dom*blended_dom_ticket +
                                             bau_for*TARIFF_IDR["foreign"])*calendar_days,
        "intervention_hypothetical_gross_tickets_idr": (
            int_dom*blended_dom_ticket*dom_price
            + int_for*TARIFF_IDR["foreign"]*for_price)*calendar_days,
    }

def first_annual_mean_quota_reference_year(rows, key="bau_annual_mean_admissions_per_day"):
    """Return a YEAR, never an exact daily crossing date or ecological event."""
    return next((r["year"] for r in rows
                 if r[key] >= OPERATIONAL_QUOTA_2024_PER_DAY), None)
