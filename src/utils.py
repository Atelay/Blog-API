from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

from src.redis import init_redis


def rate_limit(times: int = 2, seconds: int = 5) -> RateLimiter:
    """
    A rate limit function that can be used to limit the number of requests
    that a client can make within a given time frame.

    Args:
        times (int, optional): The number of requests to allow within the given time frame.
            Defaults to 100.
        seconds (int, optional): The time frame in which the rate limit applies.
            Defaults to 60.

    Returns:
        RateLimiter: The rate limit function.
    """
    return RateLimiter(times=times, seconds=seconds)


async def lifespan(app: FastAPI):
    await init_redis()
    yield
    await FastAPILimiter.close()
