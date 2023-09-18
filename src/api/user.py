from fastapi import APIRouter, Depends, HTTPException


from src.service.user import UserService
from src.schema.user import SignUpRequest
from src.auth.hash_password import HashPassword


router = APIRouter(prefix="/users", tags=["user"])
hash_password = HashPassword()


@router.get("/")
def user_list_handler(
    user_service: UserService = Depends(),
):
    return user_service.get_user_list()


@router.post("/sign-up", status_code=201)
def user_sign_up_handler(
    request: SignUpRequest,
    user_service: UserService = Depends(),
):
    # 1.유저가 있으면,exist User?에러 발생.
    # if user:
    #     raise HTTPException(
    #         status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 사용자입니다."
    #     )
    #  유저가 없으면 해쉬 패스워드 하고, 유저생성해줌. 그리고 리턴
    user_service.sign_up(request.email, request.password)  # 작동안함

    return


@router.post("/sign-in")
def user_log_in_handler():
    return
