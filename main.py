from fastapi import FastAPI, HTTPException
from enum import Enum 

class genreURLChoices(Enum):
    FANTASY = "fantasy"
    CHILDREN = "children"
    DARK = "dark"
    HUMOUR = "humour"
    HORROR = "horror"



app = FastAPI()

books = [
    {'id':1,'name':'Harrypotter1','genre':'Fantasy'},
    {'id':2,'name':'blackbeauty','genre':'Children'},
    {'id':3,'name':'13reasons why','genre':'Dark'},
    {'id':4,'name':'almighty','genre':'Humour'},
    {'id':5,'name':'shining','genre':'Horror'},
]


@app.get('/books')
async def get_books()  -> list[dict]:
    return books


@app.get('/about')
async def about()  -> str:
    return "Learning FastAPI"

@app.get('/books/{books_id}')
async def get_books(books_id: int)  -> dict :

    book = next( (book for book in books if book['id']==books_id),None)
    if book is None:
        # status code 404
        raise HTTPException(status_code=404,detail="book not found")
    
    return book

    


@app.get('/genre/{genre}')
async def get_genre(genre: genreURLChoices) -> list[dict]:
    return [
        book for book in books if book['genre'].lower() == genre.value.lower()
    ]