# Test Plan — Energy Market Data Platform

## Purpose
This document records the data quality tests applied to the star schema
built in Phase 3, following a standard UAT (User Acceptance Testing) format:
test case, expected result, actual result, and sign-off.

All tests are implemented as dbt tests and are run automatically with:
```
dbt test
```

---

## Test Summary

| Test ID | Test Case                                                        | Type        | Expected Result        | Actual Result | Status |
|---------|-------------------------------------------------------------------|-------------|-------------------------|----------------|--------|
| T01     | `dim_date.date_key` must be unique                                | Uniqueness  | No duplicate dates      | 0 duplicates   | ✅ PASS |
| T02     | `dim_date.date_key` must not be null                              | Completeness| No missing dates        | 0 nulls        | ✅ PASS |
| T03     | `dim_region.region_key` must be unique                            | Uniqueness  | No duplicate regions    | 0 duplicates   | ✅ PASS |
| T04     | `dim_region.region_key` must not be null                          | Completeness| No missing regions      | 0 nulls        | ✅ PASS |
| T05     | `fact_demand.region_key` must not be null                         | Completeness| No missing region keys  | 0 nulls        | ✅ PASS |
| T06     | `fact_demand.date_key` must not be null                           | Completeness| No missing date keys    | 0 nulls        | ✅ PASS |
| T07     | `fact_demand.period_id` must not be null                          | Completeness| No missing periods      | 0 nulls        | ✅ PASS |
| T08     | `fact_demand.demand_mw` must not be null                          | Completeness| No missing demand values| 0 nulls        | ✅ PASS |
| T09     | `fact_demand.region_key` must exist in `dim_region`               | Referential Integrity | No orphan region keys | 0 orphans | ✅ PASS |
| T10     | `fact_demand.date_key` must exist in `dim_date`                   | Referential Integrity | No orphan date keys   | 0 orphans | ✅ PASS |
| T11     | `fact_demand.demand_mw` must never be negative (custom test)      | Business Rule | No negative demand values | 0 negative rows | ✅ PASS |

**Total tests: 11 | Passed: 11 | Failed: 0**

---

## Test Categories Explained

**Completeness tests** — confirm no critical field is left blank. A blank
demand value or missing date would break downstream reporting.

**Uniqueness tests** — confirm each dimension table has exactly one row
per business key (one row per date, one row per region). Duplicate
dimension rows would cause double-counting in Power BI.

**Referential integrity tests** — confirm every fact row can be correctly
joined to its dimension rows. An "orphan" fact row (pointing to a region
or date that doesn't exist in the dimension table) would silently drop
out of any Power BI report using an inner join.

**Business rule tests** — domain-specific logic. Electricity demand is a
physical quantity and can never be negative; a negative value would
indicate a data extraction or unit error upstream.

---

## How to Run

```bash
cd energy_market
dbt test
```

Expected output: `PASS=11 WARN=0 ERROR=0 SKIP=0 NO-OP=0 TOTAL=11`

---

## Sign-off

| Role              | Name                        | Date       | Result   |
|-------------------|-----------------------------|------------|----------|
| Developer / Tester | Anne Subashini Sritharan    | 2026-07-31 | Approved |

---

## Notes for Future Expansion
- If more NEM regions (NSW1, VIC1, QLD1, TAS1) are added to the pipeline,
  no new tests are needed — the existing tests already validate any
  region present in the data.
- If price data is added in a future phase, an equivalent set of
  completeness, uniqueness, and business-rule tests should be added
  for the new fact/dimension tables.