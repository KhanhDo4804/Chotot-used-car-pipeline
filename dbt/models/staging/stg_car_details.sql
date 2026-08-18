SELECT 
    listing_id,
    link,
    ten as title,
    gia as price,
    dia_chi as address,
    so_km_da_di as mileage,
    xuat_xu as origin,
    tinh_trang as condition,
    hang as brand,
    dong_xe as model,
    nam_san_xuat as manufacture_year,
    hop_so as transmission,
    nhien_lieu as fuel_type,
    kieu_dang as body_type,
    so_cho as seats,
    crawled_at,
    loaded_at
from {{ source('raw', 'car_details_raw') }}
