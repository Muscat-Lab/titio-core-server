from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.request import ListRequestBase, ListResponseBase, ResponseBase
from src.auth.jwt_handler import get_current_user
from src.service.genre import GenreService

router = APIRouter(
    prefix="/genre",
    tags=["genre"],
)


class GenreListRequest(ListRequestBase):
    pass


class GenreListResponse(ListResponseBase):
    class Genre(ResponseBase):
        id: UUID
        ident: str
        name: str

    genres: list[Genre]


@router.get("")
async def genre_list_handler(
    q: GenreListRequest = Depends(),
    genre_service: GenreService = Depends(),
) -> GenreListResponse:
    genres = await genre_service.get_genre_list(
        limit=q.limit,
        cursor=q.cursor,
    )

    return GenreListResponse(
        genres=[
            GenreListResponse.Genre(
                id=genre.id,
                ident=genre.ident,
                name=genre.name,
            )
            for genre in genres
        ],
        next_cursor=None,
    )


class GenreLikeResponse(ResponseBase):
    pass


@router.post("{genreId}/like")
async def genre_like_handler(
    genreId: UUID,
    genre_service: GenreService = Depends(),
    user_id: UUID = Depends(get_current_user),
) -> GenreLikeResponse:
    await genre_service.like_genre(
        genre_id=genreId,
        user_id=user_id,
    )
    return GenreLikeResponse()


class GenreUnlikeResponse(ResponseBase):
    pass


@router.delete("{genreId}/like")
async def genre_unlike_handler(
    genreId: UUID,
    genre_service: GenreService = Depends(),
    user_id: UUID = Depends(get_current_user),
) -> GenreUnlikeResponse:
    await genre_service.unlike_genre(
        genre_id=genreId,
        user_id=user_id,
    )
    return GenreUnlikeResponse()
