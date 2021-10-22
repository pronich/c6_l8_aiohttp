from datetime import datetime
from gino import Gino
from asyncpg import UniqueViolationError
from aiohttp import web

db = Gino()

class BaseModelMixin:

    @classmethod
    async def by_id(cls, obj_id):
        obj = await cls.get(obj_id)
        if obj:
            return obj
        else:
            raise web.HTTPNotFound()

    @classmethod
    async def create_model(cls, **kwargs):
        try:
            obj = await cls.create(**kwargs)
            return obj

        except UniqueViolationError:
            raise web.HTTPBadRequest()

    @classmethod
    async def update_model(cls, obj_id, **kwargs):
        get = await cls.by_id(obj_id)
        await get.update(**kwargs).apply()
        response = await cls.by_id(obj_id)
        return response


class Posts(db.Model, BaseModelMixin):

    __tablename__ = "posts"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(1000))
    created_date = db.Column(db.DateTime, default=datetime.today)
    author = db.Column(db.String(100))

    def to_dict(self):
        posts = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_date": str(self.created_date),
            "author": self.author
        }
        return posts


async def return_all_posts():
    get = await db.all(Posts.query)
    some_list = []
    for post in get:
        some_list.append({"id": post.id, "header": post.title, "text": post.description,
                          "created_date": str(post.created_date), "owner_id": str(post.author)})
    return some_list