import asyncio

from utils.db import execute, fetch


async def db_check_token_user(user):
    query = """SELECT * FROM users WHERE username = :username"""
    values = {'username': user.username}

    result = await fetch(query, False, values)
    if result is None:
        return None
    else:
        return result


async def db_check_jwt_username(username):
    query = """SELECT * FROM users WHERE username = :username"""
    values = {'username': username}

    result = await fetch(query, True)
    if result is None:
        return False
    else:
        return True


async def db_insert_personel(user):
    query = """INSERT INTO personel(name, password, mail, role)
               values(:name, :password, :mail, :role)"""
    values = dict(user)
    await execute(query, False, values)


async def db_check_personel(username, password):
    query = """SELECT * FROM personel WHERE name = :username AND password = :password"""
    values = {'username': username, 'password': password}
    result = await fetch(query, True, values)
    if result is None:
        return False
    else:
        return True


async def db_get_book_by_isbn(isbn):
    query = """SELECT * FROM books WHERE isbn = :isbn"""
    values = {'isbn': isbn}

    book = await fetch(query, True, values)
    return book  # fetch zwroci book jak znajdzie albo None jak nie znajdzie w bazie


async def db_get_author(author_name):
    query = """SELECT * FROM authors WHERE name = :name"""
    values = {'name': author_name}

    author = await fetch(query, True, values)
    return author  # fetch zwroci book jak znajdzie albo None jak nie znajdzie w bazie


async def db_get_author_from_id(id):
    query = """SELECT * FROM authors WHERE id = :id"""
    values = {'id': id}

    author = await fetch(query, True, values)
    return author


async def db_patch_author_name(id, name):
    query = """UPDATE authors SET name = :name WHERE id = :id"""
    values = {'name': name, 'id': id}
    await execute(query, False, values)

