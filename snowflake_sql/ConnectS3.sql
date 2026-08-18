CREATE DATABASE IF NOT EXISTS CHOTOT_DB;
CREATE SCHEMA IF NOT EXISTS CHOTOT_DB.RAW;

USE DATABASE CHOTOT_DB;
USE SCHEMA RAW;


-- create integration
CREATE OR REPLACE STORAGE INTEGRATION chotot_s3_int
    TYPE = EXTERNAL_STAGE
    STORAGE_PROVIDER = 'S3'
    STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::850041402358:role/AcceptSnowflakeS3'
    ENABLED = TRUE
    STORAGE_ALLOWED_LOCATIONS=('s3://chotot-used-car-data/');

DESC INTEGRATION chotot_s3_int

-- check connect 

CREATE OR REPLACE FILE FORMAT parquet_format
    TYPE = parquet;
    
CREATE OR REPLACE STAGE chotot_s3_stage
    URL = 's3://chotot-used-car-data/'
    STORAGE_INTEGRATION = chotot_s3_int
    FILE_FORMAT = parquet_format;

LIST @chotot_s3_stage;

SELECT *
FROM TABLE(
  INFER_SCHEMA(
    LOCATION => '@CHOTOT_S3_STAGE',
    FILE_FORMAT => 'CHOTOT_DB.RAW.PARQUET_FORMAT'
  )
);