from fastapi import FastAPI
from .api import user, oauth, performance

app = FastAPI()
app.include_router(user.router)
app.include_router(oauth.router)
app.include_router(performance.router)

@app.get("/")
def health_check_handler():
    return {"ping": "pong"}
