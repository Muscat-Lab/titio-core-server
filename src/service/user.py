from fastapi import Depends

from src.schema.user import UserSchema
from src.models.user import User
from src.auth.hash_password import HashPassword
from src.database.connection import get_db
from src.repositories.user import UserRepository


class UserService:
    hash_password = HashPassword()

    def __init__(
        self,
        session=Depends(get_db),
        user_repository: UserRepository = Depends(UserRepository),
    ):
        self.session = session
        self.user_repository = user_repository

    def sign_up(self, email: str, password: str):
        # 사용자 아이디 중복확인
        # existing_user = self.user_repository.get_user_by_email(email)
        # if existing_user:
        # raise HTTPException(status_code=400, detail="Username already registered")

        # 비밀번호 해싱
        hashed_password = self.hash_password.create_hash(password)
        user: User = User.create(email=email, hashed_password=hashed_password)

        # 사용사 생성 및 저장
        user: User = self.user_repository.save_user(user=user)

        return UserSchema.model_validate(user)
