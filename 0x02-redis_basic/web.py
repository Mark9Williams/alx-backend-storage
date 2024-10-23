#!/usr/bin/env python3
"""Implementing a web page caching system with Redis."""
import redis
import requests
from typing import Callable
import functools

# Connect to Redis
r = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """Decorator to count the number of times a URL is accessed."""
    @functools.wraps(method)
    def wrapper(url: str) -> str:
        # Increment the access count for the URL
        r.incr(f"count:{url}")
        return method(url)
    return wrapper


def cache_page(method: Callable) -> Callable:
    """Decorator to cache the HTML content of a URL for 10 seconds."""
    @functools.wraps(method)
    def wrapper(url: str) -> str:
        # Check if the result is already cached
        cached_content = r.get(f"cached:{url}")
        if cached_content:
            return cached_content.decode('utf-8')

        # If not cached, call the original method
        result = method(url)

        # Cache the result for 10 seconds
        r.setex(f"cached:{url}", 10, result)
        return result
    return wrapper


@count_requests
@cache_page
def get_page(url: str) -> str:
    """Retrieve the HTML content of a URL and cache it for 10 seconds."""
    response = requests.get(url)
    return response.text
