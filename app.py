from settings import db_name, username, password
from aiohttp import web
from app.views import PostsView, PostView, MainPage
from app.models import db

DB_DSN = f'postgres://{username}:{password}@127.0.0.1:5432/{db_name}'


async def register_orm(app):
    await db.set_bind(DB_DSN)
    await db.gino.create_all()
    yield
    await db.pop_bind().close()


if __name__ == "__main__":
    app = web.Application()
    app.add_routes([
        web.get("/", MainPage)
    ])
    app.add_routes([
        web.get("/posts", PostsView)
    ])
    app.add_routes([
        web.get("/post/{post_id:\d+}", PostView),
        web.post("/post", PostView),
        web.patch("/post/{post_id:\d+}", PostView),
        web.delete("/post/{post_id:\d+}", PostView)
    ])
    app.cleanup_ctx.append(register_orm)
    web.run_app(app, port=8080)
