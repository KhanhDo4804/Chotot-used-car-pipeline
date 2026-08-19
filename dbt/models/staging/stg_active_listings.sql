select
    listing_id,
    link,
    try_to_timestamp_ntz(crawled_at::string) as crawled_at,
    loaded_at
from {{ source('raw', 'active_listings_raw') }}
where listing_id is not null
  and try_to_timestamp_ntz(crawled_at::string) is not null
