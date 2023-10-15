from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.request import ListRequestBase, ListResponseBase, ResponseBase
from src.models.model import Genre

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
) -> GenreListResponse:
    genres = [
        Genre(
            id=UUID("1d839208-6f3c-4740-8347-72e665f35b2a"),
            ident="romantic",
            name="로맨틱",
        ),
        Genre(
            id=UUID("9f0c69c4-7359-4102-9b7a-17b8eb374dde"),
            ident="pop",
            name="팝",
        ),
        Genre(
            id=UUID("7b62c3c7-91ff-4e39-acfb-9d7be2604d08"),
            ident="comedy",
            name="코미디",
        ),
        Genre(
            id=UUID("5817c863-a803-4612-a741-6866810140a3"),
            ident="creative",
            name="창작",
        ),
        Genre(
            id=UUID("df1ce3a8-4b67-44c0-917d-4bc7bcac0009"),
            ident="original",
            name="오리지널",
        ),
        Genre(
            id=UUID("8051b523-917b-4cd1-85a2-b54e5e534721"),
            ident="in-korea",
            name="내한공연",
        ),
    ]

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
