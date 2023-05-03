from app.database.database import engine
from sqlalchemy.sql import text


def get_report_week(week: int):
    with engine.connect() as conn:
        statement = text("""SELECT MAX(WEEK(date,1)) FROM Feed""")
        latest_week = conn.execute(statement).scalar()
        search_week = latest_week
        for i in range(week - 1):
            data = {"search_week": search_week}
            statement = text(
                """SELECT MAX(WEEK(date,1)) FROM Feed WHERE WEEK(date,1)<:search_week"""
            )
            search_week = conn.execute(statement, data).scalar()

        data = {"search_week": search_week}
        statement = text(
            """SELECT * FROM Feed WHERE WEEK(date,1) = :search_week ORDER BY date"""
        )
        result = conn.execute(statement, data)
        feeds = result.mappings().all()

        array = []

        for feed in feeds:
            data = {"feed_id": feed.feed_id}
            statement = text("""SELECT COUNT(*) FROM Likes WHERE feed_id = :feed_id""")
            likes = conn.execute(statement, data).scalar()

            data = {"feed_id": feed.feed_id}
            statement = text("""SELECT * FROM FeedFood WHERE feed_id = :feed_id""")
            result = conn.execute(statement, data)
            feed_food_data = result.mappings().all()

            kcal = 0
            carbohydrate = 0
            protein = 0
            fat = 0

            data_foods = []

            for feed_food in feed_food_data:
                data_food = {}
                data = {"food_id": feed_food.food_id}
                statement = text("""SELECT * FROM FoodInfo WHERE food_id = :food_id""")
                result = conn.execute(statement, data)
                food_info = result.mappings().first()
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
