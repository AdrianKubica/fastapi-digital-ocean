import time
from datetime import datetime

import aioredis
import uvicorn
from fastapi import FastAPI, Body, Header, File, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.exceptions import HTTPException

from models.jwt_user import JWTUser
from routes.v1 import app_v1
from routes.v2 import app_v2
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_401_UNAUTHORIZED

from utils.const import TOKEN_SUMMARY, TOKEN_DESCRIPTION, REDIS_URL, TESTING, IS_LOAD_TEST, IS_PRODUCTION, \
    REDIS_URL_PRODUCTION
from utils.db_object import db
from utils.redis_object import check_test_redis
from utils.security import check_jwt_token, authenticate_user, create_jwt_token
from utils import redis_object as re

app = FastAPI(title='Bookstore API documentation', description='It is an API that is used for Bookstore', version='1.0')
# app.mount('/v1', app_v1)
app.include_router(app_v1, prefix='/v1', dependencies=[Depends(check_jwt_token), Depends(check_test_redis)])
# app.mount('/v2', app_v2)
app.include_router(app_v2, prefix='/v2', dependencies=[Depends(check_jwt_token), Depends(check_test_redis)])


@app.on_event("startup")  # ta funkcja nie uruchamia sie w testach
async def connect_db():
    print('start')
    if not TESTING:
        await db.connect()
        if IS_PRODUCTION:
            re.redis = await aioredis.create_redis_pool(REDIS_URL_PRODUCTION)
        else:
            re.redis = await aioredis.create_redis_pool(REDIS_URL)


@app.on_event("shutdown")  # ta funkcja nie uruchamia sie w testach
async def disconnect_db():
    print('stop')
    if not TESTING:
        await db.disconnect()
        re.redis.close()
        await re.redis.wait_close()


@app.get("/awesome")
def get_awesome_data():
    return {"TYGRYS": "TO JEST TEN TYGRYS :)"}


@app.get("/")
async def health_check():
    return {"status": "OK"}


# Depends oznacza ze najpierw nalezy uruchomic funkcje od ktorej zalezy
@app.post('/token', summary=TOKEN_SUMMARY, description=TOKEN_DESCRIPTION, tags=["OAuth2.0"])  # trzeba to przeniesc tutaj i zamiast wersji uzyc ogolnej postaci bo autoryzacja i przypisywanie tokenow musi dzialac dla wszystkich endpointow
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):  # user must send username and password its predefined in this url
    """
    To jest testowy enpoint z przypisywaniem tokenow dla uzytkownikaw
    :param form_data:
    :return:
    """
    jwt_user_dict = {'username': form_data.username, 'password': form_data.password}
    jwt_user = JWTUser(**jwt_user_dict)
    user = await authenticate_user(jwt_user)
    if user is None:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
    jwt_token = create_jwt_token(user)
    return {'access_token': jwt_token}  # swagger looks for 'access_token' field


@app.middleware('http')
async def middleware(request: Request, call_next):
    s = time.perf_counter()
    d = datetime.utcnow()
    # modify request here
    # wszystko ponizej jest dodane w powyzszym app.include_router() Depends() wiec nie jest juz konieczne sprawdzanie tokena w middleware
    # if not any(word in str(request.url) for word in ['docs', '/token', '/openapi.json']):
    #     try:
    #         jwt_token = request.headers['Authorization'].split(" ")[1]
    #         is_valid = await check_jwt_token(jwt_token)
    #     except Exception as e:
    #         is_valid = False
    #     if not is_valid:  # middleware musi zwrocic obiekt response
    #         return Response("Unathorized", status_code=HTTP_401_UNAUTHORIZED)
    response = await call_next(request)
    # modify response here
    print(f'Done in {time.perf_counter() - s} sec')
    execution_time = (datetime.utcnow() - d).microseconds
    response.headers['x-execution-time'] = str(execution_time)  # headers always use strings
    return response

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
