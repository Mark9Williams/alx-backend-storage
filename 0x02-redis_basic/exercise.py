#!/usr/bin/env python3
"""Implementing a Cache class"""
import uuid
import redis
from typing import Union, Optional, Callable
import functools


def count_calls(method: Callable) -> Callable:
    """Decorator to count calls to a method using Redis."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        count = self._redis.incr(key)  # Increment the count in Redis
        result = method(self, *args, **kwargs)  # Call the original method
        return result  # Return the result of the original method
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs in Redis."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        # Create input and output list keys based on qualified name
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Normalize and store input arguments
        self._redis.rpush(input_key, str(args))  # Store input as a string

        result = method(self, *args, **kwargs)  # Call the original method

        # Store the output
        self._redis.rpush(output_key, str(result))  # Store output as a string

        return result  # Return the output
    return wrapper


def replay(method: Callable) -> None:
    """
    Display the history of calls of a particular function.
    Uses Redis keys to retrieve inputs and outputs of previous calls.
    """
    # Define Redis list keys for the inputs and outputs
    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"

    # Retrieve the list of inputs and outputs from Redis
    redis_instance = method.__self__._redis
    inputs = redis_instance.lrange(input_key, 0, -1)
    outputs = redis_instance.lrange(output_key, 0, -1)

    # Display the number of times the method was called
    print(f"{method.__qualname__} was called {len(inputs)} times:")

    # Pair inputs and outputs using zip, and display them
    for input_data, output_data in zip(inputs, outputs):
        # Decode the Redis byte strings to display as UTF-8
        input_str = input_data.decode('utf-8')
        output_str = output_data.decode('utf-8')
        print(f"{method.__qualname__}(*{input_str}) -> {output_str}")


class Cache:
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()  # Clear the Redis database

    @count_calls  # Decorate with count_calls to count method calls
    @call_history  # Decorate with call_history to record inputs and outputs
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())  # Generate a random key
        self._redis.set(key, data)  # Store the data in Redis
        return key  # Return the generated key

    def get(
        self, key: str, fn: Optional[Callable] = None
    ) -> Optional[Union[str, int, float]]:
        """Retrieve a value from Redis and convert using callable."""
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
