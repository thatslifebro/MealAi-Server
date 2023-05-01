from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from app.database import database
from app.database.database import engine
from app.router import user, feed, auth

database.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    DBSessionMiddleware,
    db_url="mysql+pymysql://root:team0808@elice08.cxtpwdmgwcgb.ap-northeast-2.rds.amazonaws.com:3306/test",
)


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(feed.router)
