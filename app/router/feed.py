from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List
from app.dto.feed.RequestFeed import *
from app.dto.feed.ResponseFeed import *
from enum import Enum

router = APIRouter(
    prefix="/api/feeds",
)


@router.post("/")
def post_feed(req: PostFeed) -> str:
    return "ok"


@router.get("/")
def get_feeds(
    filter: str, purpose: str, page: int = 1, per_page: int = 7
) -> List[FeedData]:
    return


@router.get("/{feed_id}")
def get_feed_by_id(feed_id: int) -> FeedData:
    return


@router.patch("/{feed_id}")
def patch_feed_by_id(feed_id: int, req: PatchFeedData) -> FeedData:
    return


@router.delete("/{feed_id}")
def delete_feed_by_id(feed_id: int) -> str:
    return "ok"


@router.patch("/likes/{feed_id}")
def patch_likes_by_id(feed_id: int) -> str:
    return "ok"


@router.get("/likes")
def get_my_likes() -> List[FeedData]:
    return
