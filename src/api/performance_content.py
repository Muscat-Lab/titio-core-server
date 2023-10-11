from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.request import ListRequestBase, ListResponseBase, RequestBase, ResponseBase
from src.models.model import PerformanceContent
from src.service.performance_content import PerformanceContentService

router = APIRouter(prefix="/performanceContents", tags=["performanceContent"])


class PerformanceContentListRequest(ListRequestBase):
    performance_id: UUID


class PerformanceContentListResponse(ListResponseBase):
    class PerformanceContent(ResponseBase):
        id: UUID
        performance_id: UUID
        heading: str
        content: str

    performance_contents: list[PerformanceContent]


@router.get("")
async def performance_content_list_handler(
    q: PerformanceContentListRequest = Depends(),
    performance_content_service: PerformanceContentService = Depends(),
) -> PerformanceContentListResponse:
    performance_contents = (
        await performance_content_service.get_performance_content_list(
            performance_id=q.performance_id,
            limit=q.limit,
            cursor=q.cursor,
        )
    )

    return PerformanceContentListResponse(
        performance_contents=[
            PerformanceContentListResponse.PerformanceContent.model_validate(
                performance_content, from_attributes=True
            )
            for performance_content in performance_contents
        ],
        next_cursor=(
            performance_contents[-1].sequence
            if len(performance_contents) >= q.limit
            else None
        ),
    )


class PerformanceContentSaveRequest(RequestBase):
    performance_id: UUID
    sequence: int
    heading: str
    content: str


class PerformanceContentSaveResponse(ResponseBase):
    performance_id: UUID
    sequence: int
    heading: str
    content: str


@router.post("")
async def performance_content_save_handler(
    q: PerformanceContentSaveRequest,
    performance_content_service: PerformanceContentService = Depends(),
) -> PerformanceContentSaveResponse:
    performance_content = await performance_content_service.save_performance_content(
        PerformanceContent.create(
            performance_id=q.performance_id,
            sequence=q.sequence,
            heading=q.heading,
            content=q.content,
        )
    )

    return PerformanceContentSaveResponse(
        performance_id=performance_content.performance_id,
        sequence=performance_content.sequence,
        heading=performance_content.heading,
        content=performance_content.content,
    )
