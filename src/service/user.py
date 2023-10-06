import datetime
from uuid import UUID

from fastapi import Depends, HTTPException, UploadFile

from src.models.model import User
from src.repositories.image import ImageRepository
from src.repositories.user import UserRepository
from src.utils.s3 import S3Util


class UserService:
    def __init__(
        self,
        s3_util: S3Util = Depends(S3Util),
        user_repository: UserRepository = Depends(UserRepository),
        image_repository: ImageRepository = Depends(ImageRepository),
    ):
        self.s3_util = s3_util
        self.user_repository = user_repository
        self.image_repository = image_repository

    async def save_user(self, user: User) -> User:
        return await self.user_repository.save_user(user=user)

    async def get_user_list(self) -> list[User]:
        return self.user_repository.get_user_list()

    async def find_user_by_id(self, user_id: UUID) -> User:
        user = self.user_repository.find_user_by_id(user_id=user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    async def find_user_by_username(self, username: str) -> User:
        user = self.user_repository.find_user_by_username(username=username)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    async def upload_avatar_image(self, user_id: UUID, file: UploadFile) -> str:
        if file is None or file.filename is None:
            raise HTTPException(status_code=400, detail="File is required")

        user = self.user_repository.find_user_by_id(user_id=user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        image = await self.s3_util.upload_image_to_s3(
            file=file.file,
            filename=file.filename,
            path=f"avatars/{user_id}",
            save_name=datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
        )

        image = await self.image_repository.save_image(image=image)

        user.avatar_image_id = image.id

        return await self.s3_util.get_presigned_url_by_path(path=image.path)
