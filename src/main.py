from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from src.api.routes import apis
from src.exceptions.exception import ServiceException

app = FastAPI()

for api in apis:
    app.include_router(api.router)


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
