from fastapi import FastAPI, HTTPException, Path, Query, Depends
from models import genreURLChoices, book, bookcreate, author
from typing import Annotated
from sqlmodel import Session, select
from contextlib import asynccontextmanager
from db import init_db, get_session

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield



app = FastAPI(lifespan=lifespan)







@app.get('/books')
async def get_books(genre: genreURLChoices | None = None, 
                    q: Annotated[str | None, Query(max_length=10)] = None,
                    session: Session = Depends(get_session)) -> list[book]:
    
    book_list = session.exec(select(book)).all()

    if genre:
        book_list = [b for b in book_list if b.genre.value.lower() == genre.value.lower()]

    if q:
        book_list = [b for b in book_list if q.lower() in b.name.lower()]

    return book_list


# @app.post("/books")
# async def create_book(book_data: bookcreate, session: Session = Depends(get_session)) -> book:
#     new_book = book(name=book_data.name, genre=book_data.genre)

#     if book_data.authors:
#         for author_data in book_data.authors:
#             author_instance = author(
#                 title=author_data.title,
#                 writer=author_data.writer,
#                 release_date=author_data.release_date,
#                 book=new_book  # Automatically associate the author with the new book
#             )
#             session.add(author_instance)

#     session.add(new_book)
#     session.commit()
#     session.refresh(new_book)

#     return new_book
@app.post("/books")
async def create_book(book_data: bookcreate, session: Session = Depends(get_session)) -> book:
    # Create a new book instance (without an ID)
    new_book = book(name=book_data.name, genre=book_data.genre)

    # If authors are provided, associate them with the book
    if book_data.authors:
        for author_data in book_data.authors:
            author_instance = author(
                title=author_data.title,
                writer=author_data.writer,
                release_date=author_data.release_date,
                book=new_book  # Automatically associate the author with the new book
            )
            session.add(author_instance)

    # Add the book to the session (do this after authors to ensure all are saved properly)
    session.add(new_book)
    
    # Commit to save the book and its authors to the database
    session.commit()
    
    # Refresh the new book to get its assigned ID
    session.refresh(new_book)  

    # Fetch the authors and load them explicitly with the book
    session.refresh(new_book)  # Ensure relationships are refreshed

    # Manually reload the authors relationship if needed
    new_book.authors = session.exec(select(author).where(author.book_id == new_book.id)).all()

    return new_book







@app.get('/books/{books_id}')
async def get_books(books_id: Annotated[int, Path(title="The book--ID")], 
                    session: Session = Depends(get_session)) -> book:
    # Query the book by its ID using session
    db_book = session.query(book).filter(book.id == books_id).first()

    if db_book is None:
        # Raise an HTTPException if the book is not found
        raise HTTPException(status_code=404, detail="Book not found")
    
    return db_book

    


@app.get('/genre/{genre}')
async def get_genre(genre: genreURLChoices,session: Session = Depends(get_session)) -> list[dict]:
    book_list = session.exec(select(book)).all()

    
    return [
        book for book in book_list if book['genre'].lower() == genre.value.lower()
    ]




@app.get('/about')
async def about()  -> str:
    return "Learning FastAPI"


@app.get('/test')
async def test()  -> str:
    return "An end point to test changes"





# @app.post("/books")
# async def create_book(book_data: bookcreate, session: Session = Depends(get_session)) -> book:
#     # Create a new book instance (without an ID)
#     new_book = book(name=book_data.name, genre=book_data.genre)

#     # If authors are provided, associate them with the book
#     if book_data.authors:
#         for author_data in book_data.authors:
#             author_instance = author(
#                 title=author_data.title,
#                 writer=author_data.writer,
#                 release_date=author_data.release_date,
#                 book=new_book  # Automatically associate the author with the new book
#             )
#             session.add(author_instance)

#     # Add the book to the session (do this after authors to ensure all are saved properly)
#     session.add(new_book)
    
#     # Commit to save the book and its authors to the database
#     session.commit() 
    
#     # Refresh the new book to get its assigned ID
#     session.refresh(new_book)  

#     return new_book
