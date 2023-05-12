from app.dao.feed import get_feed_food_by_id, get_food_info_by_id
from app.dao.like import *
from app.service.feed import *


class LikeService:
    def __init__(self):
        ...

    def service_patch_likes_by_id(self, feed_id: int, user_id):
        if get_feed_by_id(feed_id) is None:
            raise NoFeedIdException

        result = get_feed_likes_user(feed_id, user_id)

        if result == 1:
            push_likes(feed_id, user_id)
        else:
            cancel_likes(feed_id, user_id)

        return "ok"

    async def service_get_my_likes_feeds(self, page: int, per_page: int, user_id: int):
        feeds, feeds_num = get_my_likes_feeds(
            user_id, skip=(page - 1) * per_page, limit=per_page
        )

        prev_page = False if page == 1 else True
        next_page = False if page * per_page >= feeds_num else True

        array = []

        for feed in feeds:
            if not feed.open and feed.user_id != user_id:
                continue

            res = await FeedService().form_feed_res(feed, user_id)
            res.update({"user_daily_nutrient": None})
            array.append(res)

        return {"prev_page": prev_page, "next_page": next_page, "feeds": array}
