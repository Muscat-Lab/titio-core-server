from fastapi import FastAPI, Request, status, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from src.api import (
    user,
    oauth,
    performance,
    performance_content,
    schedule,
    casting,
    booking,
    seat,
    area,
    pre_booking,
)
from src.exceptions.exception import ServiceException

app = FastAPI()
app.include_router(user.router)
app.include_router(oauth.router)
app.include_router(performance.router)
app.include_router(performance_content.router)
app.include_router(casting.router)
app.include_router(schedule.router)
app.include_router(booking.router)
app.include_router(seat.router)
app.include_router(area.router)
app.include_router(pre_booking.router)


@app.exception_handler(ValueError)
async def validation_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


@app.exception_handler(ServiceException)
async def http_exception_handler(request: Request, exc: ServiceException):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(
            {
                "message": exc.message,
                "error_code": exc.error_code,
            }
        ),
    )


@app.get("/")
def health_check_handler():
    return {"ping": "pong"}
