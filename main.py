from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from app.database import database
from app.model import feed as model_feed
from app.model import like as model_like
from app.model import user as model_user
from app.database.database import engine
from app.router import user, feed, auth, report

model_feed.Base.metadata.create_all(bind=engine)
model_user.Base.metadata.create_all(bind=engine)
model_like.Base.metadata.create_all(bind=engine)


app = FastAPI()

# app.add_middleware(
#     DBSessionMiddleware,
#     db_url="mysql+pymysql://root:team0808@elice08.cxtpwdmgwcgb.ap-northeast-2.rds.amazonaws.com:3306/test",
# )


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(feed.router)
app.include_router(report.router)
