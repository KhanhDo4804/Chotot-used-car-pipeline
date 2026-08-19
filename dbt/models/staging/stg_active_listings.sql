select
    listing_id,
    link,
    crawled_at,
    loaded_at
from {{ source('raw', 'active_listings_raw') }}
where listing_id is not null
  and crawled_at is not null
