-- assert_demand_not_negative.sql
--
-- Custom data quality test: electricity demand should never be a negative
-- number. If this query returns ANY rows, the test fails.

select
    region_key,
    date_key,
    period_id,
    demand_mw

from {{ ref('fact_demand') }}

where demand_mw < 0