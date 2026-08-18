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
)


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



