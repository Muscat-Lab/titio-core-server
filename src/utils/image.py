import boto3
from boto3 import Session
from fastapi import Depends

from src.config import ConfigTemplate, get_config


def get_presigned_url_by_path(
    config: ConfigTemplate,
    path: str,
    expires_in: int = 3600,
) -> str:
    session = boto3.Session(
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
    )

    return session.client("s3").generate_presigned_url(
        "get_object",
        Params={
            "Bucket": config.AWS_S3_BUCKET_NAME,
            "Key": path,
        },
        ExpiresIn=expires_in,
    )


class ImageUtil:
    def __init__(
        self,
        config: ConfigTemplate = Depends(get_config),
    ):
        self.config = config
        self.session: Session = boto3.Session(
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        )

    def get_presigned_url_by_path(self, path: str) -> str:
        return self.session.client("s3").generate_presigned_url(
            "get_object",
            Params={
                "Bucket": self.config.AWS_S3_BUCKET_NAME,
                "Key": path,
            },
            ExpiresIn=3600,
        )
