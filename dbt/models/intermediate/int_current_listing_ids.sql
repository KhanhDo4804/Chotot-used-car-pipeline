with latest_crawl as (
    select max(crawled_at) as crawled_at
    from {{ ref('stg_active_listings') }}
)

select
    listings.listing_id,
    max(listings.link) as link,
    listings.crawled_at
from {{ ref('stg_active_listings') }} as listings
inner join latest_crawl
    on listings.crawled_at = latest_crawl.crawled_at
group by listings.listing_id, listings.crawled_at
