from fastapi import Depends
from redis.asyncio import Redis

from src.database.connection import get_redis


class LikeRepository:
    def __init__(self, redis: Redis = Depends(get_redis)):
        self.redis = redis
        self.LIKE_CHOICE_KEY = "LIKE_CHOICE"

    async def create_like_choice(
        self, key_score: dict[str, int], ttl: int = 60 * 60
    ) -> None:
        pipe = await self.redis.pipeline()

        await pipe.delete(self.LIKE_CHOICE_KEY)
        await pipe.zadd(self.LIKE_CHOICE_KEY, key_score)
        await pipe.expire(self.LIKE_CHOICE_KEY, ttl)

        await pipe.execute()

    async def get_like_choice_list(self, limit: int, cursor: str = "0") -> list[bytes]:
        return await self.redis.zrevrange(
            self.LIKE_CHOICE_KEY, start=int(cursor), end=int(cursor) + limit - 1
        )

    async def flush_like_choice(self) -> None:
        await self.redis.delete(self.LIKE_CHOICE_KEY)