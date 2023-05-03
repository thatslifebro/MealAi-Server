from app.dao.feed import *
from app.dto.feed.FeedRequest import PostFeed


def service_get_feed_by_id(feed_id: int):
    feed_data, feed_food_data = get_feed(feed_id)
    res = {
        "foods": feed_food_data,
        "user_name": "user_name",
        "my_like": True,
        "goal": "balance",
        "kcal": 0,
        "carbohydrate": 0,
        "protein": 0,
        "fat": 0,
        "likes": 0,
    }
    res.update(feed_data)
    # my_like 는 인증기능 구현필요, user_name 도 goal 도
    return res


def service_get_feeds(page: int, per_page: int):
    return get_feeds(skip=(page - 1) * per_page, limit=per_page)


def service_post_feed(req: PostFeed):
    post_feed_data = {
        "image_url": req.image_url,
        "meal_time": req.meal_time,
        "date": req.date,
        "open": req.open,
        "feed_id": "null",  # auto increment
        "user_id": "1",  # 유저 인증기능 구현 필요
        "thumbnail_url": "abc",
        "created_at": "null",
        "updated_at": "null",
        "is_deleted": 0,
    }

    foods_data = req.foods

    return post_feed(post_feed_data, foods_data)
