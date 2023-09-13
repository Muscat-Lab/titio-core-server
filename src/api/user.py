from fastapi import APIRouter
from src.schema.user import SignUpRequest


router = APIRouter(prefix="/users")


@router.post("/sign-up", status_code=201)
def user_sign_up_handler(request: SignUpRequest):
    return


@router.post("/sign-in")
def user_log_in_handler():
    return
