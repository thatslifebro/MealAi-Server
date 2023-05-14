from app.dao.like import get_feed_likes_user
from app.dao.report import *
from app.dao.feed import *
from app.dao.user import get_user_daily_nutrient
from app.service.feed import FeedService
from app.service.user import UserService
import datetime


class ReportService:
    # report week 은 주차별로 feed 데이터와 feed별 영양소의 합을 가져옴. 전체 합과 개인의 goal 정보를 통한 목표치 비교는 이후에 예정.

    async def service_get_report_week(self, week: int, user_id: int):
        latest_week = get_feeds_of_latest_week(user_id)
        if latest_week is None:
            return None
        search_week = latest_week
        for i in range(week - 1):
            search_week = get_previous_week(user_id, search_week)

        feeds = get_feeds_by_week(user_id, search_week)

        array = [[] for i in range(7)]

        user_info = await UserService().get_user_info(user_id)
        user_goal = user_info.goal

        for feed in feeds:
            likes = get_feed_likes(feed.feed_id)

            feed_food_data = get_feed_food_by_id(feed.feed_id)

            data_foods, total_nutrient = FeedService().service_get_food_info_by_data(
                feed_food_data
            )
            feed_data = {}
            feed_data.update(total_nutrient)
            feed_data.update(feed)

            array[feed.date.weekday()].append(feed_data)

        tkcal, tcarbohydrate, tprotein, tfat = 0, 0, 0, 0
        nutrient = []
        for i in range(7):
            kcal, carbohydrate, protein, fat = 0, 0, 0, 0
            for feed in array[i]:
                if len(feed) == 0:
                    continue
                kcal += round(feed["kcal"])
                carbohydrate += round(feed["carbohydrate"])
                protein += round(feed["protein"])
                fat += round(feed["fat"])
            tkcal += kcal
            tcarbohydrate += carbohydrate
            tprotein += protein
            tfat += fat
            nutrient.append(
                {
                    "kcal": kcal,
                    "carbohydrate": carbohydrate,
                    "protein": protein,
                    "fat": fat,
                }
            )
        weekly_nutrient = {
            "kcal": tkcal,
            "carbohydrate": tcarbohydrate,
            "protein": tprotein,
            "fat": tfat,
        }
        user_daily_goal = await get_user_daily_nutrient(user_id)
        user_weekly_goal = {
            "kcal": round(user_daily_goal["kcal"] * 7),
            "carbohydrate": round(user_daily_goal["carbohydrate"] * 7),
            "protein": round(user_daily_goal["protein"] * 7),
            "fat": round(user_daily_goal["fat"] * 7),
        }
        user_daily_goal_round = {
            "kcal": round(user_daily_goal["kcal"]),
            "carbohydrate": round(user_daily_goal["carbohydrate"]),
            "protein": round(user_daily_goal["protein"]),
            "fat": round(user_daily_goal["fat"]),
        }

        # start_of_week =

        d = "2023-W"+str(search_week)
        start_of_week = datetime.datetime.strptime(d + '-1', "%Y-W%W-%w")
        end_of_week = datetime.datetime.strptime(d+'-0', "%Y-W%W-%w")

        return {
            "goal": user_goal,
            "weekly_goal": user_weekly_goal,
            "weekly_nutrient": weekly_nutrient,
            "daily_goal": user_daily_goal_round,
            "daily_nutrient": nutrient,
            "start_of_week":str(start_of_week).split(" ")[0],
            "end_of_week":str(end_of_week).split(" ")[0]
        }

    async def service_get_report_history(self, week: int, user_id: int):
        user_info = await UserService().get_user_info(user_id)
        user_goal = user_info.goal

        latest_week = get_feeds_of_latest_week(user_id)
        search_week = latest_week
        for i in range(week - 1):
            search_week = get_previous_week(user_id, search_week)

        feeds = get_feeds_by_week(user_id, search_week)

        array = [[] for i in range(7)]

        for feed in feeds:
            likes = get_feed_likes(feed.feed_id)

            feed_food_data = get_feed_food_by_id(feed.feed_id)

            data_foods, total_nutrient = FeedService().service_get_food_info_by_data(
                feed_food_data
            )

            my_like = get_feed_likes_user(feed.feed_id, user_id)

            res = {
                "foods": data_foods,
                "user_name": "user_name",
                "my_like": my_like,
                "goal": user_goal,
                "likes": likes,
            }

            res.update(total_nutrient)
            res.update(feed)
            del res["foods"]

            array[feed.date.weekday()].append(res)

            # array.append(res)

        nutrient = []
        for i in range(7):
            kcal, carbohydrate, protein, fat = 0, 0, 0, 0
            for feed in array[i]:
                if len(feed) == 0:
                    continue
                kcal += feed["kcal"]
                carbohydrate += feed["carbohydrate"]
                protein += feed["protein"]
                fat += feed["fat"]
            nutrient.append(
                {
                    "kcal": kcal,
                    "carbohydrate": carbohydrate,
                    "protein": protein,
                    "fat": fat,
                }
            )

        user_daily_goal = await get_user_daily_nutrient(user_id)

        return {"goal": user_daily_goal, "nutrient": nutrient, "data": array}
