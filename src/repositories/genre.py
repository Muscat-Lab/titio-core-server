from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from src.database.connection import get_db
from src.models.model import Genre, UserGenreLike


class GenreRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    async def get_genre_list(
        self, limit: int, cursor: str | None = None
    ) -> list[Genre]:
        query = select(Genre)

        if cursor is not None:
            query = query.where(Genre.created_at < cursor)

        query = query.order_by(Genre.created_at.desc()).limit(limit)

        return list(self.session.execute(query).scalars().all())

    async def get_genre_list_with_like_count(
        self,
        limit: int,
        cursor: str | None = None,  # Genre.id
    ) -> list[Genre]:
        query = select(Genre).options(
            joinedload(Genre.users),
        )

        if cursor is not None:
            query = query.where(Genre.id < cursor)

        query = query.order_by(Genre.id.desc()).limit(limit)

        return list(self.session.execute(query).unique().scalars().all())

    async def save_genre(self, genre: Genre) -> Genre:
        self.session.add(instance=genre)
        self.session.commit()
        self.session.refresh(instance=genre)

        return genre

    async def like(self, genre_like: UserGenreLike) -> UserGenreLike:
        self.session.add(instance=genre_like)
        self.session.commit()
        self.session.refresh(instance=genre_like)

        return genre_like

    async def unlike(self, genre_like: UserGenreLike) -> None:
        self.session.delete(instance=genre_like)
        self.session.commit()
