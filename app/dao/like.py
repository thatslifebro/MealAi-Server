from app.database.database import engine
from sqlalchemy.sql import text


def patch_likes(feed_id: int, user_id: int):
    with engine.connect() as conn:
        data = {"feed_id": feed_id, "user_id": user_id}
        statement = text(
            """SELECT COUNT(*) FROM Likes WHERE feed_id = :feed_id AND user_id = :user_id"""
        )
        result = conn.execute(statement, data).scalar()

        if result == 1:
            statement = text(
                """DELETE FROM Likes WHERE feed_id = :feed_id AND user_id = :user_id"""
            )
            conn.execute(statement, data)
            conn.commit()
        else:
            statement = text("""INSERT INTO Likes VALUES(:feed_id,:user_id)""")
            conn.execute(statement, data)
            conn.commit()

        return "ok"


def get_my_likes(user_id: int):
    with engine.connect() as conn:
        data = {"user_id": user_id}
        statement = text(
            """SELECT * FROM Feed AS F LEFT OUTER JOIN Likes AS L ON F.feed_id = L.feed_id WHERE L.user_id = :user_id"""
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
