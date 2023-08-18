import scrapy
from scrapy_redis.spiders import RedisSpider
from urllib.parse import parse_qs, urlparse


class MiniSpiderSpider(RedisSpider):
    name = "mini_spider"
    # allowed_domains = ["mnguyen0226.github.io"]
    # start_urls = ["https://mnguyen0226.github.io/"]

    redis_key = "quotes_queue:start_urls"

    # Number of url to fetch from redis on each attempt
    redis_batch_size = 1

    # Max idle time(in seconds) before the spider stops checking redis and shuts down
    max_idle_time = 7

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }
