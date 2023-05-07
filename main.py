from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from app.database import database
from app.model import feed as model_feed
from app.model import like as model_like
from app.model import user as model_user
from app.model import auth as model_auth
from app.database.database import engine
from app.router import user, feed, auth, report
from app.error.base import CustomException
from fastapi.responses import JSONResponse

model_feed.Base.metadata.create_all(bind=engine)
model_user.Base.metadata.create_all(bind=engine)
model_like.Base.metadata.create_all(bind=engine)
model_auth.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(feed.router)
app.include_router(report.router)


@app.exception_handler(CustomException)
async def custom_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.code, content={"error": exc.error_name, "message": exc.message}
    )
