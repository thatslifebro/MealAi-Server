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

    async def service_get_my_likes_feeds(self, user_id: int):
        feeds = get_my_likes_feeds(user_id)

        array = []

        for feed in feeds:
            likes = get_feed_likes(feed.feed_id)
            feed_food_data = get_feed_food_by_id(feed.feed_id)

            data_foods, total_nutrient = FeedService().service_get_food_info_by_data(
                feed_food_data
            )

            is_mine = user_id == feed.user_id

            user_daily_nutrient = await get_user_daily_nutrient(feed.user_id)

            res = {
                "foods": data_foods,
                "user_name": "user_name",
                "my_like": True,
                "goal": "balance",
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

        return array
