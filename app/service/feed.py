from app.dao.feed import *


def service_get_feed_by_id(feed_id: int):
    return get_feed(feed_id)


def service_get_feeds(page: int, per_page: int):
    return get_feeds(skip=(page - 1) * per_page, limit=per_page)


def service_post_feed(req: PostFeed):
    return post_feed(req)
