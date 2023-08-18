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

# Specify the command to run on container start
CMD ["scrapy", "crawl", "mini_spider"]