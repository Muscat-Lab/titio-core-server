import datetime
from uuid import UUID

from fastapi import Depends, HTTPException, UploadFile

from src.models.model import Performance
from src.repositories.image import ImageRepository
from src.repositories.performance import PerformanceRepository
from src.repositories.user import UserRepository
from src.utils.s3 import S3Util


class PerformanceService:
    def __init__(
        self,
        s3_util: S3Util = Depends(S3Util),
        performance_repository=Depends(PerformanceRepository),
        user_repository=Depends(UserRepository),
        image_repository: ImageRepository = Depends(ImageRepository),
    ):
        self.s3_util = s3_util
        self.performance_repository = performance_repository
        self.user_repository = user_repository
        self.image_repository = image_repository

    async def save_performance(self, performance: Performance) -> Performance:
        return await self.performance_repository.save_performance(performance)

    async def get_performance_list(
        self,
        limit: int,
        cursor: str | None = None,
        pre_booking_enabled: bool | None = None,
        genre_ident: str | None = None,
    ):
        return await self.performance_repository.get_performance_list(
            limit=limit,
            cursor=cursor,
            pre_booking_enabled=pre_booking_enabled,
            genre_ident=genre_ident,
        )

    async def get_performance(self, performance_id: UUID, user_id: UUID | None = None):
        return await self.performance_repository.find_performance_by_id(
            performance_id=performance_id,
            user_id=user_id,
        )

    async def delete_performance(self, performance_id):
        return await self.performance_repository.delete_performance(
            performance_id=performance_id
        )

    async def upload_poster_image(self, performance_id: UUID, file: UploadFile) -> str:
        if file is None or file.filename is None:
            raise HTTPException(status_code=400, detail="File is required")

        performance = await self.performance_repository.find_performance_by_id(
            performance_id=performance_id
        )

        if not performance:
            raise HTTPException(status_code=404, detail="Performance not found")

        image = await self.s3_util.upload_image_to_s3(
            file=file.file,
            filename=file.filename,
            path=f"poster_images/{performance_id}",
            save_name=datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
        )

        image = await self.image_repository.save_image(
            image=image,
        )

        performance.poster_image_id = image.id

        await self.performance_repository.save_performance(performance=performance)

        return await performance.poster_image_url

    def like_performance(self, performanceId: UUID, userId: UUID):
        user = self.user_repository.find_user_by_id(user_id=userId)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        performance = self.performance_repository.find_performance_by_id(
            performance_id=performanceId
        )

        if not performance:
            raise HTTPException(status_code=404, detail="Performance not found")

        performance.like_users.append(user)

        self.performance_repository.save_performance(performance=performance)

    def unlike_performance(self, performanceId: UUID, userId: UUID):
        user = self.user_repository.find_user_by_id(user_id=userId)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        performance = self.performance_repository.find_performance_by_id(
            performance_id=performanceId
        )

        if not performance:
            raise HTTPException(status_code=404, detail="Performance not found")

        performance.like_users.remove(user)

        self.performance_repository.save_performance(performance=performance)
