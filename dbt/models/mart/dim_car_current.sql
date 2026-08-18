select
    listing_id,
    link,
    title,
    price,
    address,
    mileage,
    brand,
    model,
    manufacture_year,
    transmission,
    fuel_type,
    body_type,
    seats,
    loaded_at as last_loaded_at
from {{ ref('int_car_details_latest') }}