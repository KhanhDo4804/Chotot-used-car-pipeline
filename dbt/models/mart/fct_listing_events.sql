with price_versions as (
    select
        listing_id,
        link,
        title,
        price as current_price,
        lag(price) over (
            partition by listing_id
            order by dbt_valid_from
        ) as previous_price,
        dbt_valid_from as changed_at
    from {{ ref('car_details_snapshot') }}
),

latest_snapshot_per_listing as (
    select
        listing_id,
        link,
        title,
        price as current_price,
        dbt_valid_to
    from {{ ref('car_details_snapshot') }}
    qualify row_number() over (
        partition by listing_id
        order by dbt_valid_from desc
    ) = 1
),

price_events as (
    select
        listing_id,
        link,
        title,
        previous_price,
        current_price,
        current_price - previous_price as price_change,
        round(
            (current_price - previous_price) * 100.0
                / nullif(previous_price, 0),
                2
            ) as price_change_percent,
        case
            when previous_price is null then 'NEW_LISTING'
            when current_price > previous_price then 'PRICE_INCREASED'
            when current_price < previous_price then 'PRICE_DECREASED'
        end as change_type,
        changed_at
    from price_versions
    where previous_price is null
        or current_price <> previous_price
),

removed_events as (
    select
        snapshot.listing_id,
        snapshot.link,
        snapshot.title,
        snapshot.current_price as previous_price,
        cast(null as number) as current_price,
        cast(null as number) as price_change,
        cast(null as number(38, 2)) as price_change_percent,
        'REMOVED_LISTING' as change_type,
        snapshot.dbt_valid_to as changed_at
    from latest_snapshot_per_listing as snapshot
    left join {{ ref('int_current_listing_ids') }} as active
        on snapshot.listing_id = active.listing_id
    where active.listing_id is null
      and snapshot.dbt_valid_to is not null
)

select * from price_events
union all
select * from removed_events

