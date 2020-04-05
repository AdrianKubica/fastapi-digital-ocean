import datetime
import time

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from starlette.exceptions import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

from models.jwt_user import JWTUser
from utils.const import JWT_EXPIRATION_TIME_MINUTES, JWT_SECRET_KEY, JWT_ALGORITHM
from utils.db_functions import db_check_token_user, db_check_jwt_username

pwd_context = CryptContext(schemes=["bcrypt"])
jwt_user1 = {
    'username': 'user1',
    'password': '$2b$12$7otSOl8Qg0i0QTkcCLHGh..CDX/U0DVe6NG0nA6LiqGeE0P.nuCjG',
    'disabled': False,
    'role': 'admin'
}
jwt_user1 = JWTUser(**jwt_user1)
oauth_schema = OAuth2PasswordBearer(tokenUrl='/token')


def get_hashed_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        return False


# hashed = '$2b$12$7otSOl8Qg0i0QTkcCLHGh..CDX/U0DVe6NG0nA6LiqGeE0P.nuCjG'
# print(get_hashed_password("mysecret"))
# print(verify_password('mysecret', '$2b$12$7otSOl8Qg0i0QTkcCLHGh..CDX/U0DVe6NG0nA6LiqGeE0P.nuCjG'))


# Authenticate username and password to give JWT token
async def authenticate_user(user: JWTUser):
    valid_users = await db_check_token_user(user)
    is_valid = False
    for db_user in valid_users:
        if verify_password(user.password, db_user['password']):
            is_valid = True
    # if jwt_user1.username == user.username:
    #     if verify_password(user.password, jwt_user1.password):
    #         user.role = 'admin'
    #         return user
    if is_valid:
        user.role = 'admin'
        return user
    return None


# Create access JWT token
def create_jwt_token(user: JWTUser):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=JWT_EXPIRATION_TIME_MINUTES)
    jwt_payload = {
        "sub": user.username,
        "role": user.role,
        "exp": expiration
    }
    jwt_token = jwt.encode(jwt_payload, JWT_SECRET_KEY, JWT_ALGORITHM)
    return jwt_token


# Check whether JWT token is correct
async def check_jwt_token(token: str = Depends(oauth_schema)):
    try:
        jwt_payload = jwt.decode(token, JWT_SECRET_KEY, JWT_ALGORITHM)
        username = jwt_payload.get("sub")
        role = jwt_payload.get("role")
        expiration = jwt_payload.get("exp")
        if time.time() < expiration:
            is_valid = db_check_jwt_username(username)
            # if jwt_user1.username == username:
            if is_valid:
                return final_checks(role)
    except Exception as e:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)


# Last checking and returning the final
def final_checks(role: str):
    if role == 'admin':
        return True
    else:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
