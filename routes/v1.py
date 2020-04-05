import pickle

from fastapi import Body, Header, File, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from models.author import Author
from models.book import Book
from models.user import User
from utils.db_functions import db_insert_personel, db_check_personel, db_get_book_by_isbn, db_get_author, \
    db_get_author_from_id, db_patch_author_name
from utils.helper_functions import upload_image_to_server
from utils import redis_object as re
from utils.security import check_jwt_token

# app_v1 = FastAPI(openapi_prefix='/v1')
app_v1 = APIRouter()
oauth_schema = OAuth2PasswordBearer(tokenUrl='/token')

users = []


@app_v1.post('/login', tags=["User"])  # tagi sa wzkoryzstzwane do oznaczania sekcji w swagger
async def get_user_validation(username: str = Body(...), password: str = Body(...)):
    redis_key = f"{username},{password}"
    result = await re.redis.get(redis_key)
    if result:
        if result == "true":
            return {"is_valid (redis)": True}
        else:
            return {"is_valid (redis)": False}
    else:
        result = await db_check_personel(username, password)
        await re.redis.set(redis_key, str(result), expire=10)
    # return {'user': list(filter(lambda x: x.password == password, users))}
        return {'is_valid (db)': result}


@app_v1.get("/users", tags=["User"])
# async def get_users(jwt: bool = Depends(check_jwt_token)):
async def get_users(jwt: bool = Depends(check_jwt_token)):
    return {'users': users}


@app_v1.get('/books/{isbn}', response_model=Book, response_model_include=['name', 'year'], tags=["Books"])
async def get_book_by_isbn(response: Response, isbn: str):
    print("from book isbn endpoint")
    result = await re.redis.get(isbn)

    if result:
        return pickle.loads(result)
    else:
        book = await db_get_book_by_isbn(isbn)  # calosc jest zgodna z polami w tabeli wiec obiekt zostanie poprawnie utworzony
        print(book)
        if book:
            author = await db_get_author(book['author'])
            print(author)
            if author:
                author_obj = Author(**author)  # tworzymy obiekt autora bo Book w modelu zawiera obiekt Author, a nie str
                book['author'] = author_obj
                # author = Author(name="Adam", books=["book1", "book2"])
                # book = {'isbn': isbn, 'name': 'Przygody Toma', 'author': author, 'year': 2020}
                await re.redis.set(isbn, pickle.dumps(Book(**book)))
                return Book(**book) if book else None
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    # response.status_code = HTTP_404_NOT_FOUND  # tak mozna dodac dowolny status code do odpowiedzi
    # return {'test': 'generowanie status code 404 NOT FOUND'}  # zeby to przeszlo bez bledu to z dekortatora trzeba wylaczyc opcje response_mode oraz response_model_include


# Depends oznacza ze najpierw nalezy uruchomic funkcje od ktorej zalezy
@app_v1.post('/users', status_code=HTTP_201_CREATED, description="Super fajna metoda do wyciagania danych", tags=["User"])
# async def create_user(user: User, x_custom: str = Header(...), jwt: bool = Depends(check_jwt_token)):  # depends przeniesione do middleware
async def create_user(request: Request, response: Response, user: User, x_custom: str = Header(...)):
    #     print(request.headers)
    #     # await asyncio.sleep(1)  # test asynchronicznosci middleware
    # users.append(user)
    # response = JSONResponse({'request body': user, 'x-custom': x_custom})
    print(user)
    response.headers['x-test'] = 'testowo'
    await db_insert_personel(user)
    # return {'request body': user, 'x-custom': x_custom}
    return {'result': 'personel is created'}


@app_v1.get("/authors/{id}/books", tags=["Books"])
async def get_authors_books(id: int, category: str, order: str = "asc"):  # id = path parameter, category and order are query parameters
    print("czy to dziala", id, category, order)
    author = await db_get_author_from_id(id)
    if author is not None:
        books = author["books"]
        if order == "asc":
            books = sorted(books)
        else:
            books = sorted(books, reverse=True)
        return {"books": books}
    else:
        return {"result": "No author with correspoonding id"}
    # return {'query changable parameter': order + category + str(id)}


@app_v1.patch('/authors/{id}/name', tags=["Authors"])
async def patch_author_name(id: int, name: str = Body(..., embed=True)):  # jezeli chcemy pobrac parametr, ktory nie jest obiektem musimy uzyc Body
    await db_patch_author_name(id, name)
    return {"result": f"name is updated to {name}"}


@app_v1.post('/user/author', tags=["Authors"])
async def post_user_and_author(user: User, author: Author, book_store_name: str = Body(..., embed=True)): # jezeli chcemy pobrac parametr, ktory nie jest obiektem musimy uzyc Body
    return {'user': user, 'author': author, "book_store_name": book_store_name}


@app_v1.post('/user/photo', tags=["User"])  # this need to install python multipart library
async def upload_user_photo(response: Response, profile_photo: bytes = File(...)):
    response.headers['x-file-size'] = str(len(profile_photo))
    response.set_cookie(key='cookie-api', value='test-api-cookie')
    await upload_image_to_server(profile_photo)
    return {'file_size': len(profile_photo)}
