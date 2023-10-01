from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class SignUpRequest(BaseModel):
    email: str = Field("test@test.com", title="email")
    password: str = Field(default="test1234", title="password")
    username: str = Field(default="test", title="username")


class UserSchema(BaseModel):
    id: UUID = Field(titl="ID", description="user id")
    password: str = Field(title="password")
    email: str = Field("test@test.com", title="Email")
    username: str = Field("test", title="Nickname")
    created_at: datetime = Field(description="Create Time")
    updated_at: datetime = Field(description="Update Time")

    model_config = ConfigDict(from_attributes=True)
