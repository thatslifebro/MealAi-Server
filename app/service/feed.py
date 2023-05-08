import datetime

from app.dao.feed import *
from app.dao.user import read_by_user_id
from app.dto.feed.FeedRequest import PostFeed, PatchFeedData
from fastapi import HTTPException
from app.error.feed import *
from app.database.database import SessionLocal


class FeedService:
    def __init__(self):
        pass

    def service_get_food_info_by_data(self, feed_food_data):
        kcal = 0
        carbohydrate = 0
        protein = 0
        fat = 0

        data_foods = []

        # food_info와 feed_food 비교하여 영양소 구하기
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

        total_nutrient = {
            "kcal": kcal,
            "carbohydrate": carbohydrate,
            "protein": protein,
            "fat": fat,
        }
        return data_foods, total_nutrient

    def service_get_feed_by_id(self, feed_id: int):
        feed_data = get_feed_by_id(feed_id)
        if feed_data is None:
            raise NoFeedIdException
        likes = get_feed_likes(feed_id)

        feed_food_data = get_feed_food_by_id(feed_id)

        data_foods, total_nutrient = self.service_get_food_info_by_data(feed_food_data)

        # my_like 는 인증기능 구현필요, user_name 도 goal 도
        res = {
            "foods": data_foods,
            "user_name": "user_name",
            "my_like": True,
            "goal": "balance",
            "likes": likes,
        }

        res.update(total_nutrient)
        res.update(feed_data)

        return res

    def service_get_feeds(self, page: int, per_page: int):
        feeds = get_feeds_by_skip_limit(skip=(page - 1) * per_page, limit=per_page)

        array = []

        for feed in feeds:
            likes = get_feed_likes(feed.feed_id)
            feed_food_data = get_feed_food_by_id(feed.feed_id)

            data_foods, total_nutrient = self.service_get_food_info_by_data(
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

    def service_post_feed(self, req: PostFeed, user_id: int):
        user = read_by_user_id(user_id)
        post_feed_data = {
            "image_url": req.image_url,
            "meal_time": req.meal_time,
            "date": req.date,
            "open": req.open,
            "feed_id": "null",  # auto increment
            "user_id": user_id,  # 유저 인증기능 구현 필요
            "thumbnail_url": "abc",
            "created_at": datetime.datetime.utcnow(),
            "updated_at": datetime.datetime.utcnow(),
            "is_deleted": 0,
            "goal": user.goal,
        }

        foods_data = req.foods

        session = SessionLocal()
        post_feed(session, post_feed_data, foods_data)
        feed_id = get_recent_post_id(session)
        session.commit()

        for food_data in foods_data:
            insert_feed_food(feed_id, food_data)

        return "ok"

    def service_delete_feed(self, feed_id: int, user_id):
        feed_data = get_feed_by_id(feed_id)
        if feed_data is None:
            raise NoFeedIdException
        elif not match_feed_user(feed_id, user_id):
            raise NotFeedOwnerException

        session = SessionLocal()
        try:
            delete_feed_food(session, feed_id)
            delete_feed(session, feed_id)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise DeleteFeedException

        return "ok"

    def service_patch_feed(self, feed_id: int, req: PatchFeedData, user_id: int):
        if not match_feed_user(feed_id, user_id):
            raise NotFeedOwnerException

        patch_feed_data = {
            "feed_id": feed_id,
            "meal_time": req.meal_time,
            "open": req.open,
            "date": req.date,
            "updated_at": datetime.datetime.utcnow(),
        }
        foods_data = req.foods

        session = SessionLocal()
        try:
            patch_feed(feed_id, patch_feed_data)
            delete_feed_food(feed_id)
            insert_feed_food(foods_data)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise UpdateFeedException

        return self.service_get_feed_by_id(feed_id)

    def error(self):
        return error_test()
