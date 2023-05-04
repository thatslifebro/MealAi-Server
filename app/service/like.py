from app.dao.feed import get_feed_food_by_id, get_food_info_by_id
from app.dao.like import *


class LikeService:
    def __init__(self):
        ...

    def service_patch_likes_by_id(self, feed_id: int):
        user_id = 1  # 유저인증 구현 후 지정

        result = get_feed_likes_user(feed_id, user_id)

        if result == 1:
            push_likes(feed_id, user_id)
        else:
            cancel_likes(feed_id, user_id)

        return "ok"

    def service_get_my_likes(self):
        user_id = 1  # 유저기능 구현 후 지정
        feeds = get_my_likes_feeds(user_id)

        array = []

        for feed in feeds:
            likes = get_feed_likes(feed.feed_id)
            feed_food_data = get_feed_food_by_id(feed.feed_id)

            kcal = 0
            carbohydrate = 0
            protein = 0
            fat = 0

            data_foods = []

            for feed_food in feed_food_data:
                data_food = {}
                food_info = get_food_info_by_id(feed_food.food_id)
                ratio = feed_food.weight / food_info.weight

                nutrient = {
                    "kcal": food_info.kcal * ratio,
                    "carbohydrate": food_info.carbohydrate * ratio,
                    "protein": food_info.protein * ratio,
                    "fat": food_info.fat * ratio,
                }

                kcal += nutrient["kcal"]
                carbohydrate += nutrient["carbohydrate"]
                protein += nutrient["protein"]
                fat += nutrient["fat"]

                data_food.update(feed_food)
                data_food.update(nutrient)
                data_foods.append(data_food)

            res = {
                "foods": data_foods,
                "user_name": "user_name",
                "my_like": True,
                "goal": "balance",
                "kcal": kcal,
                "carbohydrate": carbohydrate,
                "protein": protein,
                "fat": fat,
                "likes": likes,
            }
            res.update(feed)
            array.append(res)

        return array
