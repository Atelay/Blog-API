from fastapi_limiter import FastAPILimiter
from redis import asyncio as aioredis

from src.config import settings


redis = aioredis.from_url(
    str(settings.redis_url), encoding="utf8", decode_responses=True
)


async def init_redis() -> None:
    await FastAPILimiter.init(redis)
