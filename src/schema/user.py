from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class SignUpRequest(BaseModel):
    username: str = Field("test", title="Nickname")
    password: str = Field(default="test1234", title="password")


class UserSchema(BaseModel):
    id: int = Field(titl="ID", description="user id")
    password: str = Field(title="password")
    email: str = Field("test@test.com", title="Email")
    username: str = Field("test", title="Nickname")
    created_at: datetime = Field(description="Create Time")
    updated_at: datetime = Field(description="Update Time")

    model_config = ConfigDict(from_attributes=True)
