from pydantic import BaseModel, Field
from fastapi import Query

from models.author import Author
from utils.const import BOOK_ISBN_DESCRIPTION


class Book(BaseModel):
    isbn: str = Field(None, description=BOOK_ISBN_DESCRIPTION)
    name: str
    author: Author
    year: int = Field(None, gt=1900, lt=2100)

