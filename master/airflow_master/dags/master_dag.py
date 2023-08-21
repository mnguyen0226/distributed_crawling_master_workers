from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import redis 

def push_urls_to_redis():
    # Create a redis client
    redisClient = redis.from_url(
        "redis://default:T4p3kJQRmQDNRqxt1tG97qQWGKRFG6fQ@redis-12469.c81.us-east-1-2.ec2.cloud.redislabs.com:12469"
    )

    # Push URLs to Redis Queue
    redisClient.lpush("quotes_queue:start_urls", "https://quotes.toscrape.com/page/1/")
    redisClient.lpush("quotes_queue:start_urls", "https://quotes.toscrape.com/page/2/")
    redisClient.lpush("quotes_queue:start_urls", "https://quotes.toscrape.com/page/3/")
    redisClient.lpush("quotes_queue:start_urls", "https://quotes.toscrape.com/page/4/")
    redisClient.lpush("quotes_queue:start_urls", "https://quotes.toscrape.com/page/5/")
    redisClient.lpush("quotes_queue:start_urls", "https://quotes.toscrape.com/page/6/")
    redisClient.lpush("quotes_queue:start_urls", "https://quotes.toscrape.com/page/7/")
    redisClient.lpush("quotes_queue:start_urls", "https://quotes.toscrape.com/page/8/")
    redisClient.lpush("quotes_queue:start_urls", "https://quotes.toscrape.com/page/9/")
    redisClient.lpush("quotes_queue:start_urls", "https://quotes.toscrape.com/page/10/")


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    dag_id="master_dag_v0",
    default_args=default_args,
    description='Push URLs to Redis',
    schedule_interval=timedelta(days=1),  # Adjust this as required
    start_date=datetime(2023, 8, 18),
    # catchup=False
)

t1 = PythonOperator(
    task_id='push_to_redis',
    python_callable=push_urls_to_redis,
    dag=dag
)
