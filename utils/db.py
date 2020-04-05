# import asyncio
# from databases import Database
# from utils.const import DB_URL

# from utils.orm_db import authors


# async def connect_db():
#     db = Database(DB_URL)
#     await db.connect()
#     return db
#
#
# async def disconnect_db(db):
#     await db.disconnect()
#
from utils.const import TESTING
from utils.db_object import db


async def execute(query, is_many, values=None):
    # db = await connect_db()
    if TESTING:  # we need to add this because in testing mode setup and shutdown function are not called
        await db.connect()

    if is_many:
        await db.execute_many(query=query, values=values)
    else:
        await db.execute(query=query, values=values)
    # await disconnect_db(db)

    if TESTING:
        await db.disconnect()


async def fetch(query, is_one, values=None):
    # db = await connect_db()
    if TESTING:
        await db.connect()

    if is_one:
        result = await db.fetch_one(query=query, values=values)
        if result is None:
            out = None
        else:
            out = dict(result)
    else:
        result = await db.fetch_all(query=query, values=values)
        if result is None:
            out = None
        else:
            out = [dict(row) for row in result]
    # await disconnect_db(db)

    if TESTING:
        await db.disconnect()

    return out


# async def test_orm():
#     # query = authors.insert().values({"id": 1, "name": "author1", "books": ["book1", "book2"]})
#     # await execute(query, False)
#     query = authors.select().where(authors.c.id == 1)
#     out = await fetch(query, True)
#     print(out)
#
# asyncio.run(test_orm())

# if __name__ == '__main__':
#     query = "INSERT INTO books VALUES(:isbn, :name, :author, :year)"
#     values = [
#         {"isbn": "isbn1", "name": "book1", "author": "author1", "year": 2019},
#         {"isbn": "isbn2", "name": "book2", "author": "author2", "year": 2018}
#     ]
#
#     # asyncio.run(execute(query, True, values))
#     res = asyncio.run(fetch("SELECT * FROM books", False))
#     print(res)

