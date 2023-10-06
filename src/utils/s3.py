import uuid
from typing import BinaryIO

import aioboto3
from aioboto3.session import Session
from PIL import Image as PILImage
from fastapi import Depends

from src.config import ConfigTemplate, get_config
from src.models.model import Image


class S3Util:
    def __init__(
        self,
        config: ConfigTemplate = Depends(get_config),
    ):
        self.config = config
        self.session: Session = aioboto3.Session(
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        )

    async def upload_image_to_s3(
        self,
        file: BinaryIO,
        filename: str,
        path: str,
        save_name: str,
    ) -> Image:
        await self._validate_file_extension(file, filename)

        extension = filename.split(".")[-1]

        file_path = f"{path}/{save_name}_{uuid.uuid4()}.{extension}"

        async with self.session.client(
            "s3",
            endpoint_url=self.config.AWS_S3_ENDPOINT_URL,
        ) as s3:
            await s3.upload_fileobj(file, self.config.AWS_S3_BUCKET_NAME, file_path)

        return Image(
            path=file_path,
            extension=extension,
        )

    async def _validate_file_extension(self, file: BinaryIO, filename: str):
        if not filename.endswith((".jpg", ".jpeg", ".png")):
            raise ValueError("Invalid file extension")

        # 이미지 크기 제한
        file.seek(0, 2)
        if file.tell() > self.config.MAX_UPLOAD_IMAGE_SIZE:
            raise ValueError("File size exceeds maximum size")

        # 이미지 파일 콘텐츠 검증
        file.seek(0)
        try:
            with PILImage.open(file) as img:
                img.verify()
        except Exception:
            raise ValueError("Invalid image file")

        # 파일 포인터를 다시 처음으로 이동
        file.seek(0)


    async def get_presigned_url_by_path(
        self,
        path: str,
    ):
        async with self.session.client(
            "s3",
            endpoint_url=self.config.AWS_S3_ENDPOINT_URL,
        ) as s3:
            return await s3.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": self.config.AWS_S3_BUCKET_NAME,
                    "Key": path,
                },
                ExpiresIn=60 * 60 * 24 * 7,  # 7일
            )
