from fastapi import FastAPI, HTTPException
from schemas import genreURLChoices, book, bookbase, bookcreate, bookwithID





app = FastAPI()


books = [
    {'id': 1, 'name': 'Harry Potter', 'genre': 'Fantasy', },
    {'id': 2, 'name': 'Percy Jackson', 'genre': 'Children', },
    {'id': 3, 'name': 'Game of Thrones', 'genre': 'Dark', },
    {'id': 4, 'name': 'James Bond', 'genre': 'Humour', },
    {'id': 5, 'name': 'Shining', 'genre': 'Horror', },
]





@app.get('/books')
async def get_books(genre:genreURLChoices | None = None)  -> list[bookwithID]:
    if genre:
        return [
            book(**b) for b in books if b['genre'].lower() == genre.value.lower()
        ]
    
    return [
        book(**b) for b in books
    ]




@app.get('/books/{books_id}')
async def get_books(books_id: int) -> bookwithID:
    # Use `next()` to find the book with the matching ID
    book_instance = next((bookwithID(**b) for b in books if b['id'] == books_id), None)
    if book_instance is None:
        # Raise an HTTPException if the book is not found
        raise HTTPException(status_code=404, detail="Book not found")
    return book_instance
    


@app.get('/genre/{genre}')
async def get_genre(genre: genreURLChoices,) -> list[dict]:
    return [
        book for book in books if book['genre'].lower() == genre.value.lower()
    ]




@app.get('/about')
async def about()  -> str:
    return "Learning FastAPI"


@app.get('/test')
async def test()  -> str:
    return "An end point to test changes"






@app.post("/books")
async def create_book(book_data: bookcreate) -> bookwithID:
    id = books[-1]['id']+1
    new_book = bookwithID(id=id, **book_data.model_dump()).model_dump()
    books.append(new_book)
    return new_book


    
