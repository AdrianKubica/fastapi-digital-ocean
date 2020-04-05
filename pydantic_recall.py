import datetime
from typing import Dict, List
from pydantic import BaseModel


class Book(BaseModel):
    name: str
    price: float = 10.0
    year: datetime.datetime


book1 = {'name': 'book1', 'price': 11, 'year': datetime.datetime.now()}
book_obj = Book(**book1)
print(book_obj.year)