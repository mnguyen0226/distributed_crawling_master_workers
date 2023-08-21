import redis

# # Create a redis client
# redisClient = redis.from_url(
#     "redis://default:T4p3kJQRmQDNRqxt1tG97qQWGKRFG6fQ@redis-12469.c81.us-east-1-2.ec2.cloud.redislabs.com:12469"
# )

# # Push URLs to Redis Queue
# redisClient.lpush("quotes_queue:start_urls", "https://quotes.toscrape.com/page/1/")
# redisClient.lpush("quotes_queue:start_urls", "https://quotes.toscrape.com/page/2/")
# redisClient.lpush("quotes_queue:start_urls", "https://quotes.toscrape.com/page/3/")
# redisClient.lpush("quotes_queue:start_urls", "https://quotes.toscrape.com/page/4/")
# redisClient.lpush("quotes_queue:start_urls", "https://quotes.toscrape.com/page/5/")
# redisClient.lpush("quotes_queue:start_urls", "https://quotes.toscrape.com/page/6/")
# redisClient.lpush("quotes_queue:start_urls", "https://quotes.toscrape.com/page/7/")
# redisClient.lpush("quotes_queue:start_urls", "https://quotes.toscrape.com/page/8/")
# redisClient.lpush("quotes_queue:start_urls", "https://quotes.toscrape.com/page/9/")
# redisClient.lpush("quotes_queue:start_urls", "https://quotes.toscrape.com/page/10/")

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

if __name__ == '__main__':
    push_urls_to_redis()