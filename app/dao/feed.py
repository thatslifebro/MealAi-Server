from sqlalchemy.exc import SQLAlchemyError

from app.dao.like import get_feed_likes
from app.database.database import engine
from sqlalchemy.sql import text


def get_feed_by_id(feed_id: int):
    with engine.connect() as conn:
        data = {"feed_id": feed_id}
        statement = text("""SELECT * FROM Feed WHERE feed_id = :feed_id""")
        result = conn.execute(statement, data)
        feed_data = result.mappings().first()
        return feed_data


def get_feed_food_by_id(feed_id: int):
    with engine.connect() as conn:
        data = {"feed_id": feed_id}
        statement = text("""SELECT * FROM FeedFood WHERE feed_id = :feed_id""")
        result = conn.execute(statement, data)
        feed_food_data = result.mappings().all()
        return feed_food_data


def get_food_info_by_id(food_id: int):
    with engine.connect() as conn:
        data = {"food_id": food_id}
        statement = text("""SELECT * FROM FoodInfo WHERE food_id = :food_id""")
        result = conn.execute(statement, data)
        food_info = result.mappings().first()
        return food_info


def get_feeds_num_by_goal(goal):
    with engine.connect() as conn:
        if goal == "all":
            statement = text("""SELECT COUNT(*) AS feeds_num FROM Feed""")
            result = conn.execute(statement)
            row = result.mappings().first()
            return row.feeds_num
        else:
            data = {"goal": goal}
            statement = text(
                """SELECT COUNT(*) AS feeds_num FROM Feed LEFT JOIN User ON Feed.user_id=User.user_id WHERE User.goal=:goal"""
            )
            result = conn.execute(statement, data)
            row = result.mappings().first()
            return row.feeds_num


def get_feeds_by_skip_limit(goal, filter, skip: int = 0, limit: int = 10):
    with engine.connect() as conn:
        filter_data = "created_at" if filter == "newest" else "likes DESC, created_at"
        if goal == "all":
            data = {"skip": skip, "limit": limit}
            if filter == "popularity":
                statement = text(
                    """SELECT F.* FROM Feed AS F LEFT JOIN (SELECT COUNT(*) as cou,feed_id FROM Likes GROUP BY feed_id) AS L ON F.feed_id =L.feed_id ORDER BY L.cou DESC, created_at DESC LIMIT :skip, :limit"""
                )
            else:
                statement = text(
                    """SELECT * FROM Feed ORDER BY created_at DESC LIMIT :skip, :limit"""
                )

        else:
            data = {
                "skip": skip,
                "limit": limit,
                "filter_data": filter_data,
                "goal": goal,
            }
            if filter == "popularity":
                statement = text(
                    """SELECT F.* FROM Feed AS F LEFT JOIN (SELECT COUNT(*) as cou,feed_id FROM Likes GROUP BY feed_id) AS L ON F.feed_id =L.feed_id LEFT JOIN User ON F.user_id=User.user_id WHERE User.goal=:goal ORDER BY L.cou DESC, created_at DESC LIMIT :skip, :limit"""
                )
            else:
                statement = text(
                    """SELECT Feed.* FROM Feed LEFT JOIN User ON Feed.user_id=User.user_id WHERE User.goal=:goal ORDER BY :filter_data DESC LIMIT :skip, :limit"""
                )

        feeds_num = get_feeds_num_by_goal(goal)

        result = conn.execute(statement, data)
        feeds = result.mappings().all()
        return feeds, feeds_num


def post_feed(session, post_feed_data):
    statement = text(
        """INSERT INTO Feed VALUES(:feed_id,:user_id,:image_url,:thumbnail_url,:meal_time,:date,:open,:created_at,:updated_at,:is_deleted)"""
    )

    session.execute(statement, post_feed_data)


def get_recent_post_id(session):
    statement = text("""SELECT LAST_INSERT_ID()""")
    result = session.execute(statement)
    feed_id = result.mappings().first()["LAST_INSERT_ID()"]
    return feed_id


def insert_feed_food(session, feed_id, food_data):
    post_food_data = {
        "food_id": food_data["food_id"],
        "image_url": food_data["image_url"],
        "weight": food_data["weight"],
        "is_deleted": 0,
        "feed_id": feed_id,
    }
    statement = text(
        """INSERT INTO FeedFood VALUES(:feed_id,:image_url,:food_id,:weight,:is_deleted)"""
    )

    session.execute(statement, post_food_data)


def delete_feed_food(session, feed_id: int):
    data = ({"feed_id": feed_id},)

    statement = text("""DELETE FROM FeedFood WHERE feed_id = :feed_id""")
    session.execute(statement, data)


def delete_feed(session, feed_id: int):
    data = ({"feed_id": feed_id},)
    statement = text("""DELETE FROM Feed WHERE feed_id = :feed_id""")
    session.execute(statement, data)


def patch_feed(session, patch_feed_data):
    statement = text(
        """UPDATE Feed SET updated_at=:updated_at, open=:open WHERE feed_id=:feed_id"""
    )
    session.execute(statement, patch_feed_data)


def match_feed_user(feed_id: int, user_id: int):
    with engine.connect() as conn:
        data = {"feed_id": feed_id}
        statement = text("""SELECT user_id FROM Feed WHERE feed_id=:feed_id""")
        result = conn.execute(statement, data)
        if user_id == int(result.mappings().first().user_id):
            return True
        else:
            return False


def search_food_by_name(name: str):
    with engine.connect() as conn:
        data = {"name": "%" + name + "%"}
        statement = text(
            """SELECT food_id, name, weight FROM FoodInfo WHERE name LIKE :name """
        )
        result = conn.execute(statement, data)
        return result.mappings().all()
