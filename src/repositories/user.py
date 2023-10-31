from uuid import UUID

from fastapi import Depends
from sqlalchemy import delete, select

from src.database.connection import get_db
from src.models.model import User, UserGenreLike, UserPerformerLike


class UserRepository:
    def __init__(self, session=Depends(get_db)):
        self.session = session

    async def get_user_list(self) -> list[User]:
        query = select(User).order_by(User.created_at.desc()).limit(10)

        users = await self.session.execute(query)

        return users.scalars().all()

    async def get_user_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)

        user = await self.session.execute(query)

        return user.scalars().first()

    async def save_user(self, user: User) -> User:
        self.session.add(instance=user)
        await self.session.commit()  # db save
        await self.session.refresh(instance=user)
        return user

    async def get_user_by_kakao_id(self, kakao_id: str) -> User | None:
        query = select(User).where(User.kakao_id == kakao_id)

        user = await self.session.execute(query)

        return user.scalars().first()

    async def find_user_by_id(self, user_id: UUID) -> User | None:
        query = select(User).where(User.id == user_id)

        user = await self.session.execute(query)

        return user.scalars().first()

    async def find_user_by_username(self, username: str) -> User | None:
        query = select(User).where(User.username == username)

        user = await self.session.execute(query)

        return user.scalars().first()

    async def like_performers(self, performer_ids: list[UUID], user_id: UUID) -> None:
        for performer_id in performer_ids:
            self.session.add(
                instance=UserPerformerLike(
                    user_id=user_id,
                    performer_id=performer_id,
                )
            )

        await self.session.commit()

    async def unlike_performer(self, performer_id: UUID, user_id: UUID) -> None:
        query = (
            delete(UserPerformerLike)
            .where(UserPerformerLike.user_id == user_id)
            .where(UserPerformerLike.performer_id == performer_id)
        )

        await self.session.execute(query)
        await self.session.commit()

    async def like_genres(self, genre_ids: list[UUID], user_id: UUID) -> None:
        for genre_id in genre_ids:
            self.session.add(
                instance=UserGenreLike(
                    user_id=user_id,
                    genre_id=genre_id,
                )
            )

        await self.session.commit()

    async def unlike_genre(self, genre_id: UUID, user_id: UUID) -> None:
        query = (
            delete(UserGenreLike)
            .where(UserGenreLike.user_id == user_id)
            .where(UserGenreLike.genre_id == genre_id)
        )

        await self.session.execute(query)
        await self.session.commit()

    async def get_like_performance_list(
        self,
        user_id: UUID,
        performance_ids: list[UUID] | None = None,
    ):
        query = select(UserPerformerLike).where(UserPerformerLike.user_id == user_id)

        if performance_ids is not None:
            query = query.where(UserPerformerLike.performer_id.in_(performance_ids))

        like_performances = await self.session.execute(query)

        return like_performances.scalars().all()

    async def find_user_by_email(self, email: str):
        query = select(User).where(User.email == email)

        user = await self.session.execute(query)

        return user.scalars().first()
