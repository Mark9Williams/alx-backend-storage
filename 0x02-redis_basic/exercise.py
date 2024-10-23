#!/usr/bin/env python3
"""Implementing a Cache class"""
import uuid
import redis
from typing import Union, Optional, Callable
import functools


def count_calls(method: Callable) -> Callable:
    """Decorator to count calls to a method using Redis."""
    @functools.wraps(method)  # Preserve the original function's metadata
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__  # Use the qualified name
        count = self._redis.incr(key)  # Increment the count in Redis
        result = method(self, *args, **kwargs)  # Call the original method
        return result  # Return the result of the original method
    return wrapper


class Cache:
    def __init__(self) -> None:
        """Constructor method"""
        self._redis = redis.Redis()
        self._redis.flushdb()  # Clear the Redis database

    @count_calls  # Decorate the store method with count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store the input data in Redis"""
        key = str(uuid.uuid4())  # Generate a random key
        self._redis.set(key, data)  # Store the data in Redis
        return key  # Return the generated key

    def get(
        self, key: str, fn: Optional[Callable] = None
    ) -> Optional[Union[str, int, float]]:
        """Retrieve a value from Redis and convert it using callable."""
        value = self._redis.get(key)  # Get the value from Redis

        if value is None:
            return None  # Return None if the key does not exist

        if fn:
            return fn(value)  # Convert the value using the provided callable

        return value  # Return the raw value if no conversion function

    def get_str(self, key: str) -> Optional[str]:
        """Get a string value from Redis."""
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """Get an integer value from Redis."""
        return self.get(key, fn=int)
