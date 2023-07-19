#!/usr/bin/env python3
"""
Exercise file
"""
import redis
import uuid
from typing import Union, Callable, Optional

class Cache:
    def __init__(self):
        # Connect to the Redis server running on localhost
        self._redis = redis.Redis(host='localhost', port=6379)

        # Flush the Redis database to start with an empty database
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        # Generate a random key using uuid
        key = str(uuid.uuid4())

        # Convert data to bytes if it's not already
        if not isinstance(data, bytes):
            data = str(data).encode()

        # Store the data in Redis using the random key
        self._redis.set(key, data)

        # Return the key
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        # Retrieve the data from Redis
        data = self._redis.get(key)

        # If the key does not exist, return None
        if data is None:
            return None

        # If a conversion function is provided, apply it to the data
        if fn is not None:
            data = fn(data)

        return data

    def get_str(self, key: str) -> Union[str, None]:
        # Automatically parametrize Cache.get with the correct conversion function
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        # Automatically parametrize Cache.get with the correct conversion function
        return self.get(key, fn=int)

# Test the implementation
if __name__ == "__main__":
    cache = Cache()

    TEST_CASES = {
        b"foo": None,
        123: int,
        "bar": lambda d: d.decode("utf-8")
    }

    for value, fn in TEST_CASES.items():
        key = cache.store(value)
        assert cache.get(key, fn=fn) == value
