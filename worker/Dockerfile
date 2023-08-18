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
