from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.request import RequestBase, ResponseBase
from src.models.model import PerformanceContent
from src.service.performance_content import PerformanceContentService

router = APIRouter(prefix="/performanceContents", tags=["performanceContent"])


class PerformanceContentRequest(RequestBase):
    performance_id: UUID


class PerformanceContentResponse(ResponseBase):
    id: UUID
    performance_id: UUID
    notice: str | None
    introduction: str | None


@router.get("")
async def performance_content_handler(
    q: PerformanceContentRequest = Depends(),
    performance_content_service: PerformanceContentService = Depends(),
) -> PerformanceContentResponse:
    performance_content = await performance_content_service.get_performance_content(
        performance_id=q.performance_id,
    )

    return PerformanceContentResponse.model_validate(
        performance_content, from_attributes=True
    )


class PerformanceContentSaveRequest(RequestBase):
    performance_id: UUID
    notice: str | None
    introduction: str | None


class PerformanceContentSaveResponse(ResponseBase):
    performance_id: UUID
    notice: str | None
    introduction: str | None


@router.post("")
async def performance_content_save_handler(
    q: PerformanceContentSaveRequest,
    performance_content_service: PerformanceContentService = Depends(),
) -> PerformanceContentSaveResponse:
    performance_content = await performance_content_service.save_performance_content(
        PerformanceContent.create(
            performance_id=q.performance_id,
            notice=q.notice,
            introduction=q.introduction,
        )
    )

    return PerformanceContentSaveResponse(
        performance_id=performance_content.performance_id,
        notice=performance_content.notice,
        introduction=performance_content.introduction,
    )
