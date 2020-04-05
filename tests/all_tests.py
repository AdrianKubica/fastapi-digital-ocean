import asyncio

from starlette.testclient import TestClient

from app import app
from utils.db import execute, fetch
from utils.security import get_hashed_password

client = TestClient(app)


def insert_user(username, password):
    query = """INSERT INTO users(username, password) values(:username, :password)"""
    hashed_password = get_hashed_password(password)
    values = {"username": username, "password": hashed_password}
    data = asyncio.run(execute(query, False, values))


def check_user(name, mail):
    query = """SELECT * FROM personel WHERE name=:name AND mail=:mail"""
    values = {'name': name, 'mail': mail}

    result = asyncio.run(fetch(query, False, values))

    if result is None:
        return False
    return True


def get_auth_header():
    insert_user("test", "test")
    response = client.post("/token", dict(username="test", password="test"))
    jwt_token = response.json()['access_token']

    auth_header = {'Authorization': f'Bearer {jwt_token}'}
    return auth_header


def clear_db():
    tables = ['authors', 'books', 'personel', 'users']
    for table in tables:
        query = f"DELETE FROM {table}"
        asyncio.run(execute(query, False))


def test_token_successful():
    insert_user("user1", "pass1")
    response = client.post("/token", dict(username="user1", password="pass1"))

    assert response.status_code == 200
    assert "access_token" in response.json()

    clear_db()


def test_token_unauthorized():
    insert_user("user1", "pass1")
    response = client.post("/token", dict(username="user1", password="pass"))

    assert response.status_code == 401

    clear_db()


def test_post_user():
    auth_header = get_auth_header()
    auth_header['x-custom'] = 'testing custom header'
    user_dict = {'name': 'user1', 'password': 'secret', 'mail': 'a@b.com', 'role': 'admin'}

    response = client.post("/v1/users", json=user_dict, headers=auth_header)
    assert response.status_code == 201
    assert check_user(user_dict['name'], user_dict['mail']) is True

    clear_db()


def test_post_user_wrong_email():
    auth_header = get_auth_header()
    auth_header['x-custom'] = 'testing custom header'
    user_dict = {'name': 'user1', 'password': 'secret', 'mail': 'invalid', 'role': 'admin'}

    response = client.post("/v1/users", json=user_dict, headers=auth_header)
    assert response.status_code == 422
    clear_db()