-- dim_region.sql
-- Dimension table: one row per NEM region.
-- Currently only SA1 is loaded, but structured to support all 5 NEM regions
-- (SA1, NSW1, VIC1, QLD1, TAS1) if the pipeline is expanded later.

with distinct_regions as (

    select distinct
        region_id

    from {{ ref('stg_demand') }}

)

select
    region_id                                              as region_key,
    region_id                                              as region_code,
    case region_id
        when 'SA1'  then 'South Australia'
        when 'NSW1' then 'New South Wales'
        when 'VIC1' then 'Victoria'
        when 'QLD1' then 'Queensland'
        when 'TAS1' then 'Tasmania'
        else 'Unknown'
    end                                                      as region_name

from distinct_regions