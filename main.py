from fastapi import FastAPI, HTTPException
from schemas import genreURLChoices, book





app = FastAPI()


books = [
    {'id':1,'name':'Harrypotter','genre':'Fantasy'},
    {'id':2,'name':'percy jackson','genre':'Children'},
    {'id':3,'name':'game of thrones','genre':'Dark'},
    {'id':4,'name':'James Bond','genre':'Humour'},
    {'id':5,'name':'shining','genre':'Horror'},
]





@app.get('/books')
async def get_books()  -> list[book]:
    return [
        book(**b) for b in books
    ]


@app.get('/about')
async def about()  -> str:
    return "Learning FastAPI"


@app.get('/books/{books_id}')
async def get_books(books_id: int) -> book:
    # Use `next()` to find the book with the matching ID
    book_instance = next((book(**b) for b in books if b['id'] == books_id), None)
    if book_instance is None:
        # Raise an HTTPException if the book is not found
        raise HTTPException(status_code=404, detail="Book not found")
    return book_instance
    


@app.get('/genre/{genre}')
async def get_genre(genre: genreURLChoices) -> list[dict]:
    return [
        book for book in books if book['genre'].lower() == genre.value.lower()
    ]





@app.get('/test')
async def about()  -> str:
    return "An end point to test changes"