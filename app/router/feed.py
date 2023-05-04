from fastapi import APIRouter
from app.dto.feed.FeedRequest import *
from app.dto.feed.FeedResponse import *
from app.service.feed import *
from app.service.like import *

router = APIRouter(
    prefix="/api/feeds",
)


@router.post(
    "",
    description="피드 작성",
    response_model=str,
    tags=["feed"],
)
def post_feed(req: PostFeed) -> str:
    return FeedService.service_post_feed(req)


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
    return FeedService.service_get_feeds(page, per_page)


@router.get(
    "/likes",
    description="내가 좋아요한 피드",
    response_model=List[FeedData],
    tags=["feed"],
)
def get_my_likes():
    return LikeService.service_get_my_likes()


@router.patch(
    "/likes/{feed_id}",
    description="좋아요 토글",
    response_model=str,
    tags=["feed"],
)
def patch_likes_by_id(feed_id: int):
    return LikeService.service_patch_likes_by_id(feed_id)


@router.get(
    "/{feed_id}",
    description="상세 피드 조회",
    response_model=FeedData,
    tags=["feed"],
)
def get_feed_by_id(feed_id: int):
    return FeedService.service_get_feed_by_id(feed_id)


@router.patch(
    "/{feed_id}",
    description="피드 수정",
    response_model=FeedData,
    tags=["feed"],
)
def patch_feed_by_id(feed_id: int, req: PatchFeedData) -> FeedData:
    return FeedService.service_patch_feed(feed_id, req)


@router.delete(
    "/{feed_id}",
    description="피드 삭제",
    response_model=str,
    tags=["feed"],
)
def delete_feed_by_id(feed_id: int):
    return FeedService.service_delete_feed(feed_id)
