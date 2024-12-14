from enum import Enum 
from datetime import date
from typing import List, Optional
from pydantic import BaseModel, validator, field_validator


class genreURLChoices(Enum):
    FANTASY = "fantasy"
    CHILDREN = "children"
    DARK = "dark"
    HUMOUR = "humour"
    HORROR = "horror"
 

class genreChoices(Enum):
    FANTASY = "Fantasy"
    CHILDREN = "Children"
    DARK = "Dark"
    HUMOUR = "Humour"
    HORROR = "Horror"
 


class author(BaseModel):
    title: str
    writer: str
    release_date: date


class book(BaseModel):
    id: int
    name: str
    genre: genreChoices
    authors: list[author] = []


class bookbase(BaseModel):
    name: str
    genre: genreChoices
    authors: Optional[list[author]] = []  # Make authors optional with a default


class bookcreate(bookbase):
    @field_validator ('genre', mode="before" )
    def title_case_genre(cls, value):
        return value.title()


class bookwithID(bookbase):
    id: int
