#!/usr/bin/env python3
"""
Exercise file
"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps

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

def call_history(method: Callable) -> Callable:
    # Use functools.wraps to conserve the original function's name and docstring
    @wraps(method)
    def wrapped_method(self, *args, **kwargs):
        # Create the input and output list keys
        inputs_key = "{}:inputs".format(method.__qualname__)
        outputs_key = "{}:outputs".format(method.__qualname__)

        # Append the input arguments to the input list in Redis
        self._redis.rpush(inputs_key, str(args))

        # Execute the original method to get the output
        output = method(self, *args, **kwargs)

        # Append the output to the output list in Redis
        self._redis.rpush(outputs_key, output)

        return output

    return wrapped_method

# Decorate Cache.store with call_history
Cache.store = call_history(Cache.store)

# Test the implementation
if __name__ == "__main__":
    cache = Cache()

    s1 = cache.store("first")
    print(s1)
    s2 = cache.store("second")
    print(s2)
    s3 = cache.store("third")
    print(s3)

    inputs = cache._redis.lrange("{}:inputs".format(cache.store.__qualname__), 0, -1)
    outputs = cache._redis.lrange("{}:outputs".format(cache.store.__qualname__), 0, -1)

    print("inputs: {}".format(inputs))
    print("outputs: {}".format(outputs))
