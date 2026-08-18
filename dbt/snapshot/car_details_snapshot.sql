{% snapshot car_details_snapshot %}

{{
    config(
        target_schema='snapshots',
        unique_key='listing_id',
        strategy='check',
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
from {{ ref('int_car_details_latest') }}

{% endsnapshot %}
