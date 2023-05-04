from app.dao.report import *
from app.dao.feed import *


class ReportService:
    # report week 은 주차별로 feed 데이터와 feed별 영양소의 합을 가져옴. 전체 합과 개인의 goal 정보를 통한 목표치 비교는 이후에 예정.
    def service_get_report_week(self, week: int):
        user_id = 3
        latest_week = get_feeds_of_latest_week(user_id)
        search_week = latest_week
        for i in range(week - 1):
            search_week = get_previous_week(user_id, search_week)

        feeds = get_feeds_by_week(user_id, search_week)

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
