from datetime import datetime

from fastapi import File

from app.dao.feed import *
from app.dao.like import get_feed_likes_user, delete_likes
from app.dao.user import read_by_user_id, get_user_daily_nutrient
from app.database.database import SessionLocal
from app.dto.feed.FeedRequest import PostFeed, PatchFeedData
from app.error.feed import *
from app.utils.predict import *


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
                "kcal": round(food_info.kcal * ratio),
                "carbohydrate": round(food_info.carbohydrate * ratio),
                "protein": round(food_info.protein * ratio),
                "fat": round(food_info.fat * ratio),
            }

            kcal += nutrient["kcal"]
            carbohydrate += nutrient["carbohydrate"]
            protein += nutrient["protein"]
            fat += nutrient["fat"]

            data_food.update({"food_name": food_info.name})
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

    async def form_feed_res(self, feed_data, user_id):
        likes = get_feed_likes(feed_data.feed_id)  #

        feed_food_data = get_feed_food_by_id(feed_data.feed_id)  #

        userInfo = await read_by_user_id(feed_data.user_id)  #
        is_mine = user_id == feed_data.user_id  #

        data_foods, total_nutrient = self.service_get_food_info_by_data(
            feed_food_data
        )  #

        # my_like 는 인증기능 구현필요, user_name 도 goal 도
        if user_id == -1:  #
            my_like = False
        else:
            my_like = get_feed_likes_user(feed_data.feed_id, user_id)

        res = {
            "foods": data_foods,
            "user_name": userInfo.nickname,
            "my_like": my_like,
            "goal": userInfo.goal,
            "likes": likes,
            "is_mine": is_mine,
        }
        res.update(total_nutrient)
        res.update(feed_data)

        return res

    async def service_get_feed_by_id(self, feed_id: int, user_id: int):
        feed_data = get_feed_by_id(feed_id)
        if feed_data is None:
            raise NoFeedIdException

        if not feed_data.open and feed_data.user_id != user_id:
            raise UnauthorizedFeedException

        res = await self.form_feed_res(feed_data, user_id)

        user_daily_nutrient = await get_user_daily_nutrient(feed_data.user_id)
        user_daily_nutrient_data = {
            "user_daily_nutrient": {
                "kcal": round(user_daily_nutrient.kcal),
                "carbohydrate": round(user_daily_nutrient.carbohydrate),
                "protein": round(user_daily_nutrient.protein),
                "fat": round(user_daily_nutrient.fat),
            },
        }
        res.update(user_daily_nutrient_data)

        return res

    async def service_get_feeds(
        self, goal, filter, page: int, per_page: int, user_id: int
    ):
        feeds, feeds_num = get_feeds_by_skip_limit(
            goal, filter, skip=(page - 1) * per_page, limit=per_page
        )

        prev_page = False if page == 1 else True
        next_page = False if page * per_page >= feeds_num else True

        array = []

        for feed in feeds:
            if not feed.open:
                continue

            res = await self.form_feed_res(feed, user_id)
            res.update({"user_daily_nutrient": None})

            array.append(res)

        return {"prev_page": prev_page, "next_page": next_page, "feeds": array}

    async def service_post_feed(
        self, req: PostFeed, user_id: int, file: UploadFile = File(...)
    ):
        image_url = None
        thumbnail_url = None

        # contents = await file.read()
        image_data = await predict_image(file)
        image_url = image_data["origin"]["image_key"] + ".png"

        user = await read_by_user_id(user_id)

        post_feed_data = {
            "image_url": image_url,
            "meal_time": req["meal_time"],
            "date": req["date"],
            "open": True,
            "feed_id": "null",  # auto increment
            "user_id": user_id,  # 유저 인증기능 구현 필요
            "thumbnail_url": thumbnail_url,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "is_deleted": 0,
            "goal": user.goal,
        }

        # 분석한 이미지를 여기에 저장해야함
        session = SessionLocal()
        try:
            post_feed(session, post_feed_data)
        except SQLAlchemyError:
            session.rollback()
            session.close()
            raise Test1Exception
        try:
            feed_id = get_recent_post_id(session)
        except SQLAlchemyError:
            session.rollback()
            session.close()
            raise Test2Exception
        try:
            foods_data = []

            for crop in image_data["crops"]:
                food_data = get_food_info_by_id(crop["food_id"])
                crop_url = crop["image_key"] + ".png"
                foods_data.append(
                    {
                        "food_id": food_data.food_id,
                        "image_url": crop_url,
                        "weight": food_data.weight,
                        "is_deleted": 0,
                        "feed_id": feed_id,
                    }
                )
        except SQLAlchemyError:
            session.rollback()
            session.close()
            raise Test3Exception
        try:
            for food in foods_data:
                insert_feed_food(session, feed_id, food)
                session.commit()
                session.close()
        except SQLAlchemyError:
            session.rollback()
            session.close()
            raise Test4Exception

        return feed_id

    def service_delete_feed(self, feed_id: int, user_id):
        feed_data = get_feed_by_id(feed_id)
        if feed_data is None:
            raise NoFeedIdException
        elif not match_feed_user(feed_id, user_id):
            raise UnauthorizedFeedException

        feed_foods = get_feed_food_by_id(feed_id)
        array = []
        data, nutrient = self.service_get_food_info_by_data(feed_foods)

        session = SessionLocal()
        try:
            delete_feed_food(session, feed_id)
            delete_likes(session, feed_id)
            delete_feed(session, feed_id)
            session.commit()
            session.close()
        except SQLAlchemyError:
            session.rollback()
            session.close()
            raise DeleteFeedException

        return data

    async def service_patch_feed(self, feed_id: int, req: PatchFeedData, user_id: int):
        if not match_feed_user(feed_id, user_id):
            raise UnauthorizedFeedException

        patch_feed_data = {
            "feed_id": feed_id,
            # "meal_time": req.meal_time,
            "open": req.open,
            # "date": req.date,
            "updated_at": datetime.utcnow(),
        }
        foods_data = req.foods

        session = SessionLocal()
        try:
            patch_feed(session, patch_feed_data)
            delete_feed_food(session, feed_id)
            for food_data in foods_data:
                insert_feed_food_patch(session, feed_id, food_data)
            session.commit()
            session.close()
        except SQLAlchemyError:
            session.rollback()
            session.close()
            raise UpdateFeedException

        return await self.service_get_feed_by_id(feed_id, user_id)

    def service_search_food_by_name(self, food_name: str):
        return search_food_by_name(food_name)
