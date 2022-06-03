from fastapi import FastAPI

from routes.user import user
from routes.auth import auth

app = FastAPI()
app.include_router(auth)
app.include_router(user)