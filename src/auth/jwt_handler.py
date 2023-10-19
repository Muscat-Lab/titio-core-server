import time
from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from src.config import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="oauth/token", auto_error=False)


def create_access_token(user_id: str):
    payload = {"user_id": user_id, "expires": time.time() + 3600}

    token = jwt.encode(payload, config.SECRET_KEY, algorithm="HS256")
    return token


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UUID:
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="not authenticated"
        )

    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No access token supplied",
            )

        return UUID(user_id)

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
        )


def get_current_user_optional(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> UUID | None:
    if token is None:
        return None

    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")

        if user_id is None:
            return None

        return UUID(user_id)

    except JWTError:
        return None
