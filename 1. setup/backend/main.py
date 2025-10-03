from fastapi import FastAPI, Depends
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

@app.get("/books", response_model=list[bookResponse])
async def list_books(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book))
    books = result.scalars().all()
    return books

@app.post("/books", response_model=bookResponse)
async def create_book(book: bookCreate, db: AsyncSession = Depends(get_db)):
    new_book = Book(title = book.title, author = book.author)
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book