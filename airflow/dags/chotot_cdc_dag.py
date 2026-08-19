from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum

PROJECT_ROOT = "/opt/airflow/project"

with DAG(
    dag_id="chotot_cdc_pipeline",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    schedule="0 */12 * * *",
    catchup=False,
    max_active_runs=1,
    tags=["chotot", "cdc"],
) as dag:

    crawl_active_listings = BashOperator(
        task_id="crawl_active_listings",
        bash_command="python src/ingestion/crawl_active_listings.py",
        cwd=PROJECT_ROOT,
    )

    crawl = BashOperator(
        task_id="crawl",
        bash_command="python src/ingestion/crawl_cdc.py",
        cwd=PROJECT_ROOT,
    )

    clean = BashOperator(
        task_id="clean",
        bash_command="python src/cleaning/clean.py",
        cwd=PROJECT_ROOT,
    )

    upload_to_s3 = BashOperator(
        task_id="upload_to_s3",
        bash_command="python src/loading/upload_to_s3.py",
        cwd=PROJECT_ROOT,
    )

    copy_raw = BashOperator(
        task_id="copy_raw",
        bash_command=(
            "cd /opt/airflow/project/dbt && "
            "dbt run-operation copy_raw_car_details --profiles-dir ."
        ),
        cwd=PROJECT_ROOT,
    )

    copy_raw_active_listings = BashOperator(
        task_id="copy_raw_active_listings",
        bash_command=(
            "cd /opt/airflow/project/dbt && "
            "dbt run-operation copy_raw_active_listings --profiles-dir ."
        ),
        cwd=PROJECT_ROOT,
    )

    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command=(
            "cd /opt/airflow/project/dbt && "
            "dbt build --profiles-dir . "
            "--select stg_car_details stg_active_listings "
            "int_car_details_latest int_current_listing_ids "
            "car_details_snapshot dim_car_current fct_listing_events"
        ),
        cwd=PROJECT_ROOT,
    )

    (
        crawl_active_listings
        >> crawl
        >> clean
        >> upload_to_s3
        >> copy_raw
        >> copy_raw_active_listings
        >> dbt_build
    )
