from enum import Enum 
from datetime import date
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
    #    {'id':1,'name':'Harrypotter1','genre':'Fantasy'},
    id: int
    name: str
    genre: str
    authors: list[author] = []


