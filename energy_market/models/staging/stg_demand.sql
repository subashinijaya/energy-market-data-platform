-- stg_demand.sql
-- Staging model: renames raw columns into clean, business-friendly names.
-- This is the first transformation layer on top of raw_demand.

select
    REGIONID           as region_id,
    SETTLEMENTDATE      as settlement_date,
    PERIODID            as period_id,
    DEMAND               as demand_mw

from {{ source('raw', 'raw_demand') }}