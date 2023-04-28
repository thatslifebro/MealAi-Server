from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from app.router import user, feed, auth

app = FastAPI()

app.add_middleware(
    DBSessionMiddleware,
    db_url="mysql+pymysql://root:team0808@elice08.cxtpwdmgwcgb.ap-northeast-2.rds.amazonaws.com:3306/test",
)


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(feed.router)
