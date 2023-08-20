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
    'worker_dag',
    default_args=default_args,
    description='Worker DAG pulling URLs from Redis, scraping data, and storing it in CSV',
    schedule_interval=timedelta(hours=1),  # You can adjust this based on your needs.
    start_date=datetime(2023, 8, 19),
    catchup=False,
)

run_worker = DockerOperator(
    task_id='run_worker_container',
    image='custom_worker_image:latest',
    api_version='auto',
    auto_remove=True,
    command='scrapy crawl mini_spider',
    docker_url='unix://var/run/docker.sock',
    network_mode='bridge',
    volumes=['./output:/app/output'],
    environment={
        'REDIS_URL': 'redis://default:T4p3kJQRmQDNRqxt1tG97qQWGKRFG6fQ@redis-12469.c81.us-east-1-2.ec2.cloud.redislabs.com:12469'
    },
    dag=dag
)
