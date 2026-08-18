FROM apache/airflow:2.10.5

COPY docker/requirements-airflow.txt /requirements-airflow.txt

RUN pip install --no-cache-dir \
    "apache-airflow==${AIRFLOW_VERSION}" \
    -r /requirements-airflow.txt
