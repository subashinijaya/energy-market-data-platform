-- dim_date.sql
-- Dimension table: one row per unique date, with calendar attributes.
-- Built from the distinct dates found in stg_demand.

with distinct_dates as (

    select distinct
        date(settlement_date) as date_day

    from {{ ref('stg_demand') }}

)

select
    date_day                                   as date_key,
    date_day                                   as full_date,
    cast(strftime('%Y', date_day) as integer)   as year,
    cast(strftime('%m', date_day) as integer)   as month,
    cast(strftime('%d', date_day) as integer)   as day_of_month,
    cast(strftime('%w', date_day) as integer)   as day_of_week,   -- 0=Sunday
    case
        when cast(strftime('%w', date_day) as integer) in (0, 6)
        then 1 else 0
    end                                          as is_weekend

from distinct_dates