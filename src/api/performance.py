import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, File, Query, UploadFile
from pydantic import Field

from src.api.request import ListRequestBase, ListResponseBase, RequestBase, ResponseBase
from src.auth.jwt_handler import get_current_user, get_current_user_optional
from src.models.model import Performance
from src.service.performance import PerformanceService

router = APIRouter(prefix="/performances", tags=["performance"])


class PerformanceListRequest(ListRequestBase):
    pre_booking_enabled: bool | None = Query(None)
    genre_ident: str | None = Query(None)


class PerformanceListResponse(ListResponseBase):
    class Performance(ResponseBase):
        id: UUID
        title: str
        running_time: str
        grade: str
        begin: datetime.date
        end: datetime.date
        pre_booking_enabled: bool
        pre_booking_closed_at: datetime.datetime | None = None
        poster_image_url: str | None = None
        like: bool | None = None
        schedule_text: str = ""
        location_text: str = ""

    performances: list[Performance]


class PerformanceHotResponse(PerformanceListResponse):
    pass


@router.get("/hot")
async def performance_hot_handler(
    performance_service: PerformanceService = Depends(),
    user_id: UUID | None = Depends(get_current_user_optional),
) -> PerformanceHotResponse:
    performances = await performance_service.get_hot_performance(user_id=user_id)

    return PerformanceHotResponse(
        performances=[
            PerformanceHotResponse.Performance.model_validate(
                performance, from_attributes=True
            )
            for performance in performances
        ],
        next_cursor=(
            performances[-1].latest_cursor if len(performances) >= 20 else None
        ),
    )


@router.get("")
async def performance_list_handler(
    q: PerformanceListRequest = Depends(),
    performance_service: PerformanceService = Depends(),
    user_id: UUID | None = Depends(get_current_user_optional),
) -> PerformanceListResponse:
    performances = await performance_service.get_performance_list(
        limit=q.limit,
        cursor=q.cursor,
        pre_booking_enabled=q.pre_booking_enabled,
        genre_ident=q.genre_ident,
    )

    return PerformanceListResponse(
        performances=[
            PerformanceListResponse.Performance.model_validate(
                performance, from_attributes=True
            )
            for performance in performances
        ],
        next_cursor=(
            performances[-1].latest_cursor if len(performances) >= q.limit else None
        ),
    )


class PerformanceGetResponse(PerformanceListResponse.Performance):
    pass


@router.get("/{performanceId}")
async def performance_detail_handler(
    performanceId: UUID,
    performance_service: PerformanceService = Depends(),
    user_id: UUID | None = Depends(get_current_user_optional),
) -> PerformanceGetResponse:
    performance = await performance_service.get_performance(
        performance_id=performanceId,
        user_id=user_id,
    )

    return PerformanceGetResponse.model_validate(performance, from_attributes=True)


class PerformanceCreateRequest(RequestBase):
    title: str = Field(max_length=50)
    running_time: str = Field(max_length=30)
    grade: str = Field(max_length=30)
    begin: datetime.date
    end: datetime.date
    pre_booking_enabled: bool
    pre_booking_closed_at: datetime.datetime | None = None


class PerformanceCreateResponse(ResponseBase):
    id: UUID
    title: str
    running_time: str
    grade: str
    begin: datetime.date
    end: datetime.date
    pre_booking_enabled: bool
    pre_booking_closed_at: datetime.datetime | None = None


@router.post("")
async def performance_create_handler(
    q: PerformanceCreateRequest,
    performance_service: PerformanceService = Depends(),
) -> PerformanceCreateResponse:
    return PerformanceCreateResponse.model_validate(
        await performance_service.save_performance(
            Performance.create(
                title=q.title,
                running_time=q.running_time,
                grade=q.grade,
                begin=q.begin,
                end=q.end,
                pre_booking_enabled=q.pre_booking_enabled,
                pre_booking_closed_at=q.pre_booking_closed_at,
            )
        ),
        from_attributes=True,
    )


class PerformancePosterImageResponse(ResponseBase):
    poster_image_url: str


@router.post("/{performanceId}/poster_image")
async def performance_poster_image_create_handler(
    performanceId: UUID,
    poster_image: UploadFile = File(),
    performance_service: PerformanceService = Depends(),
) -> PerformancePosterImageResponse:
    uploaded_url = await performance_service.upload_poster_image(
        performance_id=performanceId,
        file=poster_image,
    )

    return PerformancePosterImageResponse(
        poster_image_url=uploaded_url,
    )


class PerformanceUpdateRequest(PerformanceCreateRequest):
    pass


class PerformanceUpdateResponse(PerformanceCreateResponse):
    pass


@router.put("/{performanceId}")
async def performance_update_handler(
    q: PerformanceUpdateRequest,
    performanceId: UUID,
    performance_service: PerformanceService = Depends(),
) -> PerformanceUpdateResponse:
    return PerformanceUpdateResponse.model_validate(
        await performance_service.save_performance(
            Performance(
                id=performanceId,
                title=q.title,
                running_time=q.running_time,
                grade=q.grade,
                begin=q.begin,
                end=q.end,
                pre_booking_enabled=q.pre_booking_enabled,
                pre_booking_closed_at=q.pre_booking_closed_at,
            ),
        )
    )


@router.delete("/{performanceId}")
async def performance_delete_handler(
    performanceId: UUID,
    performance_service: PerformanceService = Depends(),
) -> ResponseBase:
    await performance_service.delete_performance(performanceId)

    return ResponseBase()


@router.post("/{performanceId}/like")
async def performance_like_handler(
    performanceId: UUID,
    performance_service: PerformanceService = Depends(),
    user_id: UUID = Depends(get_current_user),
) -> ResponseBase:
    await performance_service.like_performance(performanceId, user_id)

    return ResponseBase()


@router.delete("/{performanceId}/like")
async def performance_unlike_handler(
    performanceId: UUID,
    performance_service: PerformanceService = Depends(),
    user_id: UUID = Depends(get_current_user),
) -> ResponseBase:
    await performance_service.unlike_performance(performanceId, user_id)

    return ResponseBase()
