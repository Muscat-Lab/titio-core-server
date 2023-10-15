import pytest

from src.repositories.like import LikeRepository


class TestLikeRepository:
    @pytest.fixture
    def like_repository(self, redis):
        return LikeRepository(redis=redis)

    @pytest.mark.asyncio
    async def test_create_like_choice(self, like_repository: LikeRepository):
        await like_repository.create_like_choice(
            key_score={
                "key1": 1,
                "key2": 2,
                "key3": 3,
                "key4": 4,
                "key5": 5,
                "key6": 6,
            }
        )

        assert await like_repository.redis.zcard(like_repository.LIKE_CHOICE_KEY) == 6

        assert [
            key.decode() for key in await like_repository.get_like_choice_list(limit=3)
        ] == ["key6", "key5", "key4"]

        assert [
            key.decode()
            for key in await like_repository.get_like_choice_list(limit=2, cursor="3")
        ] == ["key3", "key2"]
