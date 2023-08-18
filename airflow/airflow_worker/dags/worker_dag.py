# Since workers continuously check Redis, the DAG structure will be almost identical to the master's.

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'worker_dag',
    default_args=default_args,
    description='Run the Worker to fetch URLs from Redis and scrape',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 8, 18),
    catchup=False,
)

t1 = DockerOperator(
    task_id='worker_task',
    image='worker_image',  # Replace with the name you've built the worker's Docker image with.
    api_version='auto',
    auto_remove=True,
    network_mode="bridge",
    dag=dag
)
