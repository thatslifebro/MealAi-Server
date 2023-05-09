from redis import Redis

redis = Redis()


async def get_redis() -> Redis:
    return redis
