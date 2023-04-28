from fastapi import FastAPI, Depends
from typing import List
from fastapi_sqlalchemy import DBSessionMiddleware
from sqlalchemy.orm import Session
from app.database import models, crud, schemas
from app.database.database import engine, SessionLocal
from app.router import user, feed, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    DBSessionMiddleware,
    db_url="mysql+pymysql://root:team0808@elice08.cxtpwdmgwcgb.ap-northeast-2.rds.amazonaws.com:3306/test",
)


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(feed.router)
