{% macro copy_raw_active_listings() %}

{% set create_table_sql %}

CREATE TABLE IF NOT EXISTS CHOTOT_DB.RAW.ACTIVE_LISTINGS_RAW (
    listing_id STRING,
    link STRING,
    crawled_at STRING,
    loaded_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
)

{% endset %}

{% set copy_sql %}

COPY INTO CHOTOT_DB.RAW.ACTIVE_LISTINGS_RAW (
    listing_id,
    link,
    crawled_at
)
FROM (
    SELECT
        $1:"listing_id"::STRING,
        $1:"link"::STRING,
        $1:"crawled_at"::STRING
    FROM @CHOTOT_DB.RAW.CHOTOT_S3_STAGE
)
PATTERN = '.*raw/active_listings_v2/.*[.]parquet'
FILE_FORMAT = (
    FORMAT_NAME = 'CHOTOT_DB.RAW.PARQUET_FORMAT'
)

{% endset %}

{% do run_query(create_table_sql) %}
{% do run_query(copy_sql) %}

{% endmacro %}
