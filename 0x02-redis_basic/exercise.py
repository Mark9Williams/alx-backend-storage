#!/usr/bin/env python3
"""class Cache that will interact with Redis"""


import redis
import uuid
from typing import Union, Callable, Optional


def count_calls(method: Callable) -> Callable:
    """Decorator that increments the count for a method."""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function."""
        method_key = method.__qualname__
        self._redis.incr(method_key)
        return method(self, *args, **kwargs)

    return wrapper

# call_history decorator


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs in Redis."""
    @wraps(method)  # Preserve original method details (e.g., name, docstring)
    def wrapper(self, *args, **kwargs):
        # Input and output Redis keys using method's qualified name
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Store inputs in the input_key list
        self._redis.rpush(input_key, str(args))

        # Execute the original method and get the result/output
        result = method(self, *args, **kwargs)

        # Store the result/output in the output_key list
        self._redis.rpush(output_key, str(result))

        # Return the result of the original method
        return result

    return wrapper


class Cache:
    def __init__(self):
        """Initialize the Redis client and flush the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history  # Decorate the store method
    @count_calls  # Decorate the store mehod
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Generate a random key, store the data in Redis, return the key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)

    def get(
        self, key: str, fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float, None]:
        """Get the data stored at the key, apply fn to the data."""
        value = self._redis.get(key)
        if value is None:
            return None
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> Optional[str]:
        """Get the data stored at the key as a string."""
        return self.get(key, fn=lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """Get the data stored at the key as an integer."""
        return self.get(key, fn=int)


def replay(method: Callable):
    """Display the history of calls for a given method."""
    mthd_key = method.__qualname__  # Get the qualified name of the method
    input_key = f"{mthd_key}:inputs"  # Key for inputs
    output_key = f"{mthd_key}:outputs"  # Key for outputs

    # Retrieve inputs and outputs from Redis
    inputs = cache._redis.lrange(input_key, 0, -1)  # Get all inputs
    outputs = cache._redis.lrange(output_key, 0, -1)  # Get all outputs

    # Get the number of calls
    call_count = len(inputs)

    # Print the call count
    print(f"{mthd_key} was called {call_count} times:")

    # Loop over the inputs and outputs and print them
    for input_data, output_data in zip(inputs, outputs):
        # Decode bytes and format the output
        print(
            f"{mthd_key}(*{input_data.decode('utf-8')}) -> {output_data.decode('utf-8')}")
