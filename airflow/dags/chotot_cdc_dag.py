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

    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command=(
            "cd /opt/airflow/project/dbt && "
            "dbt build --profiles-dir . "
            "--select stg_car_details int_car_details_latest "
            "car_details_snapshot fct_listing_events"
        ),
        cwd=PROJECT_ROOT,
    )

    crawl >> clean >> upload_to_s3 >> copy_raw >> dbt_build
