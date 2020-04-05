import os

JWT_SECRET_KEY = "2a258f354247b80df4ad5e5848b1bf2a4d99c3a829e040968a44952487c486e5"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_TIME_MINUTES = 60 * 24 * 5

TOKEN_DESCRIPTION = 'It checks username and password'
TOKEN_SUMMARY = 'It returns access token for user'

BOOK_ISBN_DESCRIPTION = "ISBN number"

DB_HOST = '192.168.99.103'
DB_HOST_PRODUCTION = '165.22.71.84'
DB_USER = 'admin'
DB_PASSWORD = 'admin'
DB_NAME = 'bookstore'
DB_PORT = 5432
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DB_URL_PRODUCTION = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST_PRODUCTION}:{DB_PORT}/{DB_NAME}"

REDIS_URL = f"redis://localhost"
REDIS_URL_PRODUCTION = f"redis://165.22.71.84"


def check_mode():
    try:
        return os.environ['MODE'] == 'PRODUCTION'
    except KeyError:
        return False


TESTING = True
IS_LOAD_TEST = False
IS_PRODUCTION = check_mode()

TEST_DB_HOST = '192.168.99.103'
TEST_DB_USER = 'admin'
TEST_DB_PASSWORD = 'admin'
TEST_DB_NAME = 'bookstore'
TEST_DB_PORT = 5432
TEST_DB_URL = f"postgresql://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"

TEST_REDIS_URL = f"redis://192.168.99.103:6379"