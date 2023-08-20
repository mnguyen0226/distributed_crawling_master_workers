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