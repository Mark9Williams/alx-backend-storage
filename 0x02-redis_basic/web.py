#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker"""
import redis
import requests
import time
from functools import wraps

# Initialize Redis client
redis_client = redis.Redis()


def cache_page(expiration: int):
    """Decorator to cache the page and track access count."""
    def decorator(func):
        @wraps(func)
        def wrapper(url: str) -> str:
            # Key for caching the page content
            cache_key = f"cache:{url}"
            count_key = f"count:{url}"

            # Check if the content is already cached
            cached_content = redis_client.get(cache_key)
            if cached_content:
                # Increment the access count and return cached content
                redis_client.incr(count_key)
                return cached_content.decode("utf-8")

            # Call the original function to get the page content
            page_content = func(url)

            # Cache the content with expiration and update the count
            redis_client.set(cache_key, page_content, ex=expiration)
            redis_client.incr(count_key)

            return page_content
        return wrapper
    return decorator


@cache_page(expiration=10)
def get_page(url: str) -> str:
    """Fetch the HTML content of a URL."""
    response = requests.get(url)
    return response.text
