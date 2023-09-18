from fastapi import FastAPI
from .api import user

app = FastAPI()
app.include_router(user.router)


@app.get("/")
def health_check_handler():
    return {"ping": "pong"}
