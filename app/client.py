import asyncio
from aiohttp import ClientSession


async def get_posts():
    async with ClientSession() as session:
        async with session.get("http://127.0.0.1:8080/posts") as resp:
            return await resp.json()


async def get_post(post_id):
    async with ClientSession() as session:
        async with session.get(f"http://127.0.0.1:8080/post/{post_id}") as resp:
            return await resp.text()


async def post_posts(post):
    async with ClientSession() as session:
        async with session.post(f"http://127.0.0.1:8080/post", json=post) as resp:
            if resp.status != 201:
                return await resp.text()
            return await resp.json()


async def patch_posts(author, title, description, post_id):
    async with ClientSession() as session:
        async with session.patch(f"http://127.0.0.1:8080/post/{post_id}", json={
            "title": title,
            "description": description,
            "author": author
        }) as resp:
            if resp.status != 200:
                return await resp.text()
            return await resp.json()


async def delete_post(post_id):
    async with ClientSession() as session:
        async with session.delete(f"http://127.0.0.1:8080/post/{post_id}") as resp:
            return {"status": resp.status}


async def main():
    advert = [{"title": "Iron",
               "description": "Electric. With a steamer.",
               "author": "Sid Vicious"},
              {"title": "Washer.",
               "description": "New. Bosh",
               "author": "Chester benington"},
              {"title": "grinder.",
               "description": "Electric. Siemens",
               "author": "Kurt Cobain"},
              ]
    response1 = await get_posts()
    print(response1)
    response2 = await get_post(34)
    print(response2)
    for post in advert:
        response3 = await post_posts(post)
        print(response3)
    response4 = await patch_posts("max", "data", "mine header", 3)
    print(response4)
    response5 = await delete_post(1)
    print(response5)
    response6 = await delete_post(100)
    print(response6)


asyncio.run(main())