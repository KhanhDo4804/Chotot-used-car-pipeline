{% snapshot car_details_snapshot %}

{{
    config(
        target_schema='snapshots',
        unique_key='listing_id',
        strategy='check',
        invalidate_hard_deletes=True,
        check_cols=[
            'price',
            'address',
            'mileage',
            'condition',
            'title'
        ]
    )
}}

select
    listing_id,
    link,
    title,
    price,
    address,
    mileage,
    origin,
    condition,
    brand,
    model,
    manufacture_year,
    transmission,
    fuel_type,
    body_type,
    seats,
    loaded_at
from {{ ref('int_car_details_latest') }} as details
where exists (
    select 1
    from {{ ref('int_current_listing_ids') }} as active
    where active.listing_id = details.listing_id
)

{% endsnapshot %}
