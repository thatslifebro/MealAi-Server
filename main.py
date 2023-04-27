from fastapi import FastAPI

from app.router import user, feed, auth

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(feed.router)
