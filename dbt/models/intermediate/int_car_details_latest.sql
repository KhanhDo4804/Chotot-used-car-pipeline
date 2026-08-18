select * 
from {{ ref('stg_car_details') }}
qualify row_number() over (
    partition by listing_id 
    order by 
        crawled_at desc,
        loaded_at desc
) = 1