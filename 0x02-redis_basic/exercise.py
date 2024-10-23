#!/usr/bin/env python3
"""Implementing a Cache class"""
import uuid
import redis
from typing import Union


class Cache:
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()  # Clear the Redis database

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())  # Generate a random key
        self._redis.set(key, data)  # Store the data in Redis
        return key  # Return the generated key
