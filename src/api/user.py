from fastapi import APIRouter

router = APIRouter(prefix="/users")

@router.post("/sign-up",status_code=201)
def user_sign_up_handler():
    return

@router.post("/sign-in")
def user_log_in_handler():
    return