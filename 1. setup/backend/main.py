from fastapi import FastAPI, Depends, HTTPException, Path
from fastapi.concurrency import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from database import engine, get_db
from models import Base, Book
from schemas import bookResponse, bookCreate

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def read_root():
    return{"message": "Books API - Module 1"}

@app.get('/books', response_model=List[bookResponse])
async def list_books(
    author: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(Book)
    if author:
        query = query.where(Book.author == author)
    result = await db.execute(query)
    books = result.scalars().all()
    return books

@app.get('/books/{book_id}', response_model=bookResponse)
async def get_book(
    book_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return book

@app.post("/books", response_model=bookResponse)
async def create_book(book: bookCreate, db: AsyncSession = Depends(get_db)):
    new_book = Book(title = book.title, author = book.author)
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book