from enum import Enum 
from datetime import date
from typing import List, Optional
from pydantic import BaseModel


class genreURLChoices(Enum):
    FANTASY = "fantasy"
    CHILDREN = "children"
    DARK = "dark"
    HUMOUR = "humour"
    HORROR = "horror"
 

class author(BaseModel):
    title: str
    writer: str
    release_date: date


class book(BaseModel):
    id: int
    name: str
    genre: str
    authors: list[author] = []


class bookbase(BaseModel):
    name: str
    genre: str
    authors: Optional[list[author]] = []  # Make authors optional with a default


class bookcreate(bookbase):
    pass


class bookwithID(bookbase):
    id: int
