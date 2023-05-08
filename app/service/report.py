from app.dao.report import *
from app.dao.feed import *
from app.service.feed import FeedService


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

            data_foods, total_nutrient = FeedService().service_get_food_info_by_data(
                feed_food_data
            )

            res = {
                "foods": data_foods,
                "user_name": "user_name",
                "my_like": True,
                "goal": "balance",
                "likes": likes,
            }

            res.update(total_nutrient)
            res.update(feed)

            array.append(res)

        return array
