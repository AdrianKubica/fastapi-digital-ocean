from fastapi import Query
from pydantic import BaseModel
import enum


class Role(str, enum.Enum): # tutaj wazne jest to dziedziczenie po str inaczej nie bedzie decode poprawnego na string
    admin: str = 'admin'
    personnel: str = "personnel"


class User(BaseModel):
    name: str
    password: str
    mail: str = Query(None, regex='^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$')
    role: Role
