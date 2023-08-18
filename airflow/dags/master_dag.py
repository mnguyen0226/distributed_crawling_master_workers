from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'master_dag',
    default_args=default_args,
    description='Master DAG pushing URLs to Redis',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 8, 17),
    catchup=False,
)

run_master = DockerOperator(
    task_id='run_master_container',
    image='custom_master_image:latest',
    api_version='auto',
    auto_remove=True,
    command='python master.py',
    docker_url='unix://var/run/docker.sock',
    network_mode='bridge',
    environment={
        'REDIS_URL': 'redis://default:T4p3kJQRmQDNRqxt1tG97qQWGKRFG6fQ@redis-12469.c81.us-east-1-2.ec2.cloud.redislabs.com:12469'
    },
    dag=dag
)
