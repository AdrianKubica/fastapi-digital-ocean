from fastapi import FastAPI, Body, Header, File, APIRouter

from models.author import Author
from models.book import Book
from models.user import User

from starlette.status import HTTP_201_CREATED
from starlette.responses import Response

# app_v2 = FastAPI(openapi_prefix='/v2')
app_v2 = APIRouter()

users = []


@app_v2.post('/user/photo', tags=["User"])  # this need to install python multipart library
async def upload_user_photo(response: Response, profile_photo: bytes = File(...)):
    response.headers['x-file-size'] = str(len(profile_photo))
    response.set_cookie(key='cookie-api', value='test-api-cookie')
    return {'file_size': len(profile_photo), 'version': "88"}
