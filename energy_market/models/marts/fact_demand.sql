-- fact_demand.sql
-- Fact table: one row per region + settlement period.
-- This is the centre of the star schema, linking out to dim_date and dim_region.

select
    stg.region_id                       as region_key,
    date(stg.settlement_date)            as date_key,
    stg.period_id                        as period_id,
    stg.settlement_date                  as settlement_datetime,
    stg.demand_mw                        as demand_mw

from {{ ref('stg_demand') }} as stg
