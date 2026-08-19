select
    details.listing_id,
    details.link,
    details.title,
    details.price,
    details.address,
    details.mileage,
    details.brand,
    details.model,
    details.manufacture_year,
    details.transmission,
    details.fuel_type,
    details.body_type,
    details.seats,
    details.loaded_at as last_loaded_at,
    active.crawled_at as active_checked_at
from {{ ref('int_car_details_latest') }} as details
inner join {{ ref('int_current_listing_ids') }} as active
    on details.listing_id = active.listing_id
