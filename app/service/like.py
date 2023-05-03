from app.dao.like import *


def service_patch_likes_by_id(feed_id: int):
    user_id = 1  # 유저인증 구현 후 지정

    return patch_likes(feed_id, user_id)


def service_get_my_likes():
    user_id = 1  # 유저기능 구현 후 지정

    return get_my_likes(user_id)
