# distributed_crawling_master_workers

# S1: Master-Worker Communication
## Scrapy-Redis vs Redis
### scrapy_redis:

Pros:
Built for Distributed Scraping: scrapy_redis is built specifically for Scrapy to support distributed crawling. It provides out-of-the-box integration of Redis with Scrapy, making the setup of distributed scraping easier.

Cooperative Scraping: With scrapy_redis, multiple spiders can share the same Redis queue. This means that you can scale out easily by just running another worker/spider.

Built-in Deduplication: It comes with a Redis-backed dupefilter, which ensures that URLs aren't crawled multiple times by different spiders.

Persistence: Crawls can be paused and resumed, which can be beneficial in cases where you have large crawling tasks that might need interruptions.

Cons:
Learning Curve: If you're not familiar with it, there's a bit of a learning curve involved. It introduces new concepts and components, such as the RedisSpider.

Complexity: For simpler use-cases, integrating scrapy_redis might be overkill and add unnecessary complexity.

### Regular redis:
Pros:
Flexibility: Using regular Redis gives you greater flexibility to define and control the workflow, as you have more granular control over the operations.

Simplicity: If you're only using Redis as a simple queue or storage without needing distributed features, regular Redis operations can be simpler and more direct.

Broader Application: Your knowledge on Redis can be applied beyond Scrapy, to other applications or systems that require caching, storage, or message brokering.

Cons:
More Manual Setup: If you're aiming for a distributed system, you might have to handle things like request deduplication manually.

Less Integration with Scrapy: Doesn't provide Scrapy-specific features out of the box.

```sh
# master
python master.py

# worker
scrapy crawl name_scraper_worker
```

# S2: Dockerization of Master, Worker, and Docker-Compose

## [Docker-compose](https://www.youtube.com/watch?v=DM65_JyGxCo&ab_channel=NetworkChuck)
- Compose is a tool for defining and running multi-container Docker applications
- It's a tool to defining & running multi-container docker applications
- Use yaml files to configure application services (docker-compose.yml)
- It can start all services with a single command: docker compose up
- It can stop all services with as single command: docker compose down
- It can scale up selected services when required.
```yml
version: '3.8'

services:

  master:
    build:
      context: ./master
      dockerfile: Dockerfile
    environment:
      - REDIS_URL=redis://default:T4p3kJQRmQDNRqxt1tG97qQWGKRFG6fQ@redis-12469.c81.us-east-1-2.ec2.cloud.redislabs.com:12469

  worker:
    build:
      context: ./worker
      dockerfile: Dockerfile
    volumes:
      - ./output:/app/output
    environment:
      - REDIS_URL=redis://default:T4p3kJQRmQDNRqxt1tG97qQWGKRFG6fQ@redis-12469.c81.us-east-1-2.ec2.cloud.redislabs.com:12469
```

## How to measure run time?
To log the scraping time for a single worker, you can add some custom logging code in your Scrapy spider. Here's a step-by-step guide:

Modify Your Spider:

Open mini_spider.py inside the spiders directory. At the top, import the necessary modules:

python
Copy code
import logging
import time
Next, you'll want to record the start time and end time of your spider's scraping process.

In your spider class, override the __init__ method to set the start time:

```python
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.start_time = time.time()
```

At the end of the spider's run, you'll want to record the end time and calculate the total scraping time. You can do this by overriding the closed method:

```python
def closed(self, reason):
    end_time = time.time()
    elapsed_time = end_time - self.start_time
    logging.info(f"Spider ran for {elapsed_time:.2f} seconds.")
    ```
Ensure Logging Settings:

Ensure your Scrapy settings (settings.py) have the following configurations to show the log message:

```python
LOG_LEVEL = 'INFO'
```

Run the Spider:

Now when you run the spider using Docker Compose, you should see a log message at the end of the spider's run indicating how long the spider ran for.

Given that you've set up Docker and Docker Compose, the log message will show in the console output when you run docker compose up.

Note: The method closed is called when a spider finishes its run for any reason. By overriding it, you can perform any necessary teardown or logging like we did above

## How to fix the error
Create a customed docker image

```sh
  File "/usr/local/lib/python3.9/site-packages/scrapy_redis/spiders.py", line 197, in schedule_next_requests
    self.crawler.engine.crawl(req, spider=self)
TypeError: crawl() got an unexpected keyword argument 'spider'
```

Change setting in worker's Docker file
```sh
# Set the base image
FROM python:3.9-slim

# Set the working directory in docker
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY mini_scraper/ ./mini_scraper/
COPY scrapy.cfg .

# Overwrite the original spiders.py with your modified version
COPY customed_image_files/modified_spiders.py /usr/local/lib/python3.9/site-packages/scrapy_redis/spiders.py

# Specify the command to run on container start
CMD ["scrapy", "crawl", "mini_spider"]
```

Then build a Custom Docker Image
```sh
docker build -t custom_worker_image ./worker
```

Build Worker's custom Docker Image
```
docker build -t custom_worker_image ./worker
```

Update docker-compose.yml
```

```

Run docker-compose
```
docker compose down -v
docker compose build
docker compose up
```

## Comparison 1 workers
```sh
# mini_spider.py
    # Number of url to fetch from redis on each attempt
    redis_batch_size = 1

    # Max idle time(in seconds) before the spider stops checking redis and shuts down
    max_idle_time = 10

# settings.py
DOWNLOAD_DELAY = 2
```

For single worker: `2023-08-18 01:22:17 [root] INFO: Spider ran for 30.27 seconds.`

For 3 workers:
```sh
2023-08-18 01:42:02 [root] INFO: Spider (645ec1b83bc3) ran for 15.33 seconds.
2023-08-18 01:42:02 [root] INFO: Spider (701e7eff38bb) ran for 15.26 seconds.
2023-08-18 01:42:02 [root] INFO: Spider (d37dba0878bd) ran for 15.22 seconds.
```

# Let's separate the docker compose into 2 sections
- You have to run 2 threads: to build and to run. Master first then Worker
- "Hello, so I got the code repository for distributed web scraping that has the master push the code web urls into the Redis queue while the worker can take the URL one by one to scrape and get the info, then save to csv file. I was able to get it to work by running docker-compose. Here is the tree of the project."

- Starting from branch `3`
## Create airflow for master: [un-pw] = [airflow-airflow]
### Initialize folder
```
(learning_scraper) mnguyen0226@pop-os:~/Documents/school/graduate/homebase/learning/distributed_crawling_master_workers/master$ mkdir airflow

export AIRFLOW_HOME=.
airflow db init
airflow users create --username admin --firstname firstname --lastname lastname --role Admin --email admin@domain.com
airflow webserver -p 8080

# after login
export AIRFLOW_HOME=.
airflow scheduler
```

### Run Airflow in Docker
- [Source](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
- Run Docker Desktop and Check
```sh
(learning_airflow) mnguyen0226@pop-os:~/Documents/school/graduate/homebase/learning/web_crawlers/airflow_projects$ docker --version
Docker version 24.0.5, build ced0996
(learning_airflow) mnguyen0226@pop-os:~/Documents/school/graduate/homebase/learning/web_crawlers/airflow_projects$ docker-compose --version
docker-compose version 1.25.5, build unknown
```

Download docker-compose.yaml
```sh
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.6.3/docker-compose.yaml'
```

Change:
```sh
  # from
  AIRFLOW__CORE__EXECUTOR: CeleryExecutor

  # to
  AIRFLOW__CORE__EXECUTOR: LocalExecutor
```

Delete:
```sh
  AIRFLOW__CELERY__RESULT_BACKEND: db+postgresql://airflow:airflow@postgres/airflow
  AIRFLOW__CELERY__BROKER_URL: redis://:@redis:6379/0


  redis:
    condition: service_healthy

  redis:
    image: redis:latest
    expose:
      - 6379
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 30s
      retries: 50
      start_period: 30s
    restart: always

  airflow-worker:
    <<: *airflow-common
    command: celery worker
    healthcheck:
      test:
        - "CMD-SHELL"
        - 'celery --app airflow.executors.celery_executor.app inspect ping -d "celery@$${HOSTNAME}"'
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s
    environment:
      <<: *airflow-common-env
      # Required to handle warm shutdown of the celery workers properly
      # See https://airflow.apache.org/docs/docker-stack/entrypoint.html#signal-propagation
      DUMB_INIT_SETSID: "0"
    restart: always
    depends_on:
      <<: *airflow-common-depends-on
      airflow-init:
        condition: service_completed_successfully

  flower:
    <<: *airflow-common
    command: celery flower
    profiles:
      - flower
    ports:
      - "5555:5555"
    healthcheck:
      test: ["CMD", "curl", "--fail", "http://localhost:5555/"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s
    restart: always
    depends_on:
      <<: *airflow-common-depends-on
      airflow-init:
        condition: service_completed_successfully
```

Initialize environment
```sh
(learning_airflow) mnguyen0226@pop-os:~/Documents/school/graduate/homebase/learning/web_crawlers/airflow_projects/2_airflow_docker$ mkdir -p ./dags ./logs ./plugins ./config

# for linux
(learning_airflow) mnguyen0226@pop-os:~/Documents/school/graduate/homebase/learning/web_crawlers/airflow_projects/2_airflow_docker$ echo -e "AIRFLOW_UID=$(id -u)" > .env
```

Initialize database 
- This is where it will download all the docker images
```sh
(learning_airflow) mnguyen0226@pop-os:~/Documents/school/graduate/homebase/learning/web_crawlers/airflow_projects/2_airflow_docker$ docker compose up airflow-init

# output success > 2_airflow_docker-airflow-init-1 exited with code 0
```

Run Airflow in the background
```sh
(learning_airflow) mnguyen0226@pop-os:~/Documents/school/graduate/homebase/learning/web_crawlers/airflow_projects/2_airflow_docker$ docker compose up -d
```

Check running container
```sh
(learning_airflow) mnguyen0226@pop-os:~/Documents/school/graduate/homebase/learning/web_crawlers/airflow_projects/2_airflow_docker$ docker ps

CONTAINER ID   IMAGE                  COMMAND                  CREATED          STATUS                             PORTS                    NAMES
6658dadfd3e8   apache/airflow:2.6.3   "/usr/bin/dumb-init …"   44 seconds ago   Up 24 seconds (health: starting)   8080/tcp                 2_airflow_docker-airflow-triggerer-1
bd3f1dbb75a2   apache/airflow:2.6.3   "/usr/bin/dumb-init …"   44 seconds ago   Up 25 seconds (health: starting)   0.0.0.0:8080->8080/tcp   2_airflow_docker-airflow-webserver-1
19d78357b6a8   apache/airflow:2.6.3   "/usr/bin/dumb-init …"   44 seconds ago   Up 24 seconds (health: starting)   8080/tcp                 2_airflow_docker-airflow-scheduler-1
ac17a73bed3f   postgres:13            "docker-entrypoint.s…"   2 minutes ago    Up 2 minutes (healthy)             5432/tcp                 2_airflow_docker-postgres-1
```
- Here, we can see there airflow webserver and scheduler and postgres database

Check on Docker Desktop

Quickcheck
```sh
http://0.0.0.0:8080/

# UN: airflow
# PW: airflow
```

To shut down the container and clear the volume defined in the `docker-compose.yaml`, we will do `docker compose down -v`

### Final
Make sure you follow all steps, to connect to Redis [check image](), you just need to set up connection. To have it run property
```
# 2 terminals
docker compose up # 1
airflow scheduler # 2

# to shut down
docker compose down -v
```

This means that we actually don't need dockerfile and docker compose in the `/master`
