FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip \
    && pip install dbt-core==1.7.9 dbt-snowflake==1.7.5 protobuf==4.25.3

WORKDIR /usr/app/dbt
