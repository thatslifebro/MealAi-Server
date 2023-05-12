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

            likes = get_feed_likes(feed.feed_id)
            feed_food_data = get_feed_food_by_id(feed.feed_id)

            userInfo = await read_by_user_id(feed.user_id)

            data_foods, total_nutrient = FeedService().service_get_food_info_by_data(
                feed_food_data
            )

            is_mine = user_id == feed.user_id

            user_daily_nutrient = await get_user_daily_nutrient(feed.user_id)

            res = {
                "foods": data_foods,
                "user_name": userInfo.nickname,
                "my_like": True,
                "goal": userInfo.goal,
                "likes": likes,
                "is_mine": is_mine,
                "user_daily_nutrient": {
                    "kcal": round(user_daily_nutrient.kcal),
                    "carbohydrate": round(user_daily_nutrient.carbohydrate),
                    "protein": round(user_daily_nutrient.protein),
                    "fat": round(user_daily_nutrient.fat),
                },
            }

            res.update(total_nutrient)
            res.update(feed)

            array.append(res)

        return {"prev_page": prev_page, "next_page": next_page, "feeds": array}
