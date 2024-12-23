from enum import Enum
from datetime import date
from typing import List, Optional
from pydantic import BaseModel, field_validator
from sqlmodel import SQLModel, Field, Relationship


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

# The base model for authors without the ID and book association.
class authorbase(SQLModel):
    title: str
    writer: str
    release_date: date

# The author model, which includes the ID and the foreign key to book.
class author(authorbase, table=True):
    id: int = Field(default=None, primary_key=True)
    book_id: Optional[int] = Field(default=None, foreign_key="book.id")  # Foreign key to the book table
    book: "book" = Relationship(back_populates="authors")  # Relationship with the book




# The base model for books without the authors association.
class bookbase(SQLModel):
    name: str
    genre: genreChoices


# The book model, which includes the ID and the relationship to authors.
class book(bookbase, table=True):
    id: int = Field(default=None, primary_key=True)
    authors: List[author] = Relationship(back_populates="book") # Relationship with authors


# Model to handle book creation, including authors as an optional field.
class bookcreate(bookbase):
    authors: Optional[List[authorbase]] = None

    @field_validator('genre', mode="before")
    def title_case_genre(cls, value):
        return value.title()



class AuthorResponse(BaseModel):
    id: int
    title: str
    writer: str
    release_date: date

    class Config:
        from_attributes = True


class BookResponse(BaseModel):
    id: int
    name: str
    genre: str
    authors: Optional[List[AuthorResponse]] = []

    class Config:
        from_attributes = True
