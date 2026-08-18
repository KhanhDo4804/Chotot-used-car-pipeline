{% macro copy_raw_car_details() %}

{% set copy_sql %}

COPY INTO CHOTOT_DB.RAW.CAR_DETAILS_RAW (
    listing_id,
    link,
    ten,
    gia,
    dia_chi,
    so_km_da_di,
    xuat_xu,
    tinh_trang,
    hang,
    dong_xe,
    nam_san_xuat,
    hop_so,
    nhien_lieu,
    kieu_dang,
    so_cho,
    crawled_at
)
FROM (
    SELECT
        $1:"listing_id"::STRING,
        $1:"Link"::STRING,
        $1:"Tên"::STRING,
        $1:"Giá"::NUMBER,
        $1:"Địa chỉ"::STRING,
        $1:"Số KM đã đi"::NUMBER,
        $1:"Xuất xứ"::STRING,
        $1:"Tình trạng"::STRING,
        $1:"Hãng"::STRING,
        $1:"Dòng xe"::STRING,
        $1:"Năm sản xuất"::STRING,
        $1:"Hộp số"::STRING,
        $1:"Nhiên liệu"::STRING,
        $1:"Kiểu dáng"::STRING,
        $1:"Số chỗ"::STRING,
        $1:"crawled_at"::TIMESTAMP_NTZ
    FROM @CHOTOT_DB.RAW.CHOTOT_S3_STAGE
)
FILE_FORMAT = (
    FORMAT_NAME = 'CHOTOT_DB.RAW.PARQUET_FORMAT'
);

{% endset %}

{% do run_query(copy_sql) %}

{% endmacro %}