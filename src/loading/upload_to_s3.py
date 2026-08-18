import os
from datetime import datetime, timezone
from pathlib import Path

import boto3
from dotenv import load_dotenv

DEFAULT_PARQUET_FILE = "data/data_cleaning/cleaned_car_details.parquet"
load_dotenv()


def get_object_key():
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"raw/car_details/cleaned_car_details_{timestamp}.parquet"


def upload_parquet_to_s3(
    parquet_file=DEFAULT_PARQUET_FILE,
    bucket_name=None,
    object_key=None,
):
    parquet_path = Path(parquet_file)
    if not parquet_path.exists():
        raise FileNotFoundError(f"Parquet file not found: {parquet_path}")

    bucket_name = bucket_name or os.getenv("S3_BUCKET_NAME")
    object_key = object_key or get_object_key()
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION"),
    )

    s3_client.upload_file(str(parquet_path), bucket_name, object_key)
    print(f"Uploaded: s3://{bucket_name}/{object_key}")


if __name__ == "__main__":
    upload_parquet_to_s3()
