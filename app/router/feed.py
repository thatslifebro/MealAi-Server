from fastapi import APIRouter
from app.dto.feed.FeedRequest import *
from app.dto.feed.FeedResponse import *
from app.service.feed import *
from app.service.like import *
from app.utils.depends import *

router = APIRouter(
    prefix="/api/feeds",
)


@router.post(
    "",
    description="피드 작성",
    response_model=str,
    tags=["feed"],
)
def post_feed(req: PostFeed, user_id: int = Depends(current_user_id)) -> str:
    return FeedService().service_post_feed(req, user_id)


@router.get(
    "",
    description="전체 피드 조회",
    response_model=List[FeedData],
    tags=["feed"],
)
def get_feeds(
    goal: GoalEnum = "balance",
    filter: FilterEnum = "newest",
    page: int = 1,
    per_page: int = 7,
):
    return FeedService().service_get_feeds(page, per_page)


@router.get("/error")
def get_feeds():
    return FeedService().error()


@router.get(
    "/likes",
    description="내가 좋아요한 피드",
    response_model=List[FeedData],
    tags=["feed"],
)
def get_my_likes(user_id: int = Depends(current_user_id)):
    return LikeService().service_get_my_likes_feeds(user_id)


@router.patch(
    "/likes/{feed_id}",
    description="좋아요 토글",
    response_model=str,
    tags=["feed"],
)
def patch_likes_by_id(feed_id: int, user_id: int = Depends(current_user_id)):
    return LikeService().service_patch_likes_by_id(feed_id, user_id)


@router.get(
    "/{feed_id}",
    description="상세 피드 조회",
    response_model=FeedData,
    tags=["feed"],
)
def get_feed_by_id(feed_id: int):
    return FeedService().service_get_feed_by_id(feed_id=feed_id)


@router.patch(
    "/{feed_id}",
    description="피드 수정",
    response_model=FeedData,
    tags=["feed"],
)
def patch_feed_by_id(
    feed_id: int, req: PatchFeedData, user_id: int = Depends(current_user_id)
) -> FeedData:
    return FeedService().service_patch_feed(feed_id, req, user_id)


@router.delete(
    "/{feed_id}",
    description="피드 삭제",
    response_model=str,
    tags=["feed"],
)
def delete_feed_by_id(feed_id: int, user_id: int = Depends(current_user_id)):
    return FeedService().service_delete_feed(feed_id, user_id)
