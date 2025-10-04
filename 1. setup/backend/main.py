from fastapi import FastAPI, Depends, HTTPException, Path
from fastapi.concurrency import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from database import engine, get_db
from models import Base, Book
from schemas import BookResponse, BookCreate, BookUpdate
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)

app = FastAPI(lifespan=lifespan)

# CORS (important for React frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # or ["http://localhost:5173"] if using Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------- API Endpoints -----------------------------

# Root endpoint
@app.get("/")
async def read_root():
    return{"message": "Books API - Module 1"}

# ----------------------------
#     GET
# ----------------------------
@app.get('/books', response_model=List[BookResponse])
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

@app.get('/books/{book_id}', response_model=BookResponse)
async def get_book(
    book_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# ----------------------------
#     POST
# ----------------------------

@app.post("/books", response_model=BookResponse)
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    new_book = Book(title = book.title, author = book.author)
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book


# ----------------------------
#     PUT
# ----------------------------

@app.put('/books/{book_id}', response_model=BookResponse)
async def update_book(
    book_id: int,
    book: BookUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Book).where(Book.id == book_id))
    existing_book = result.scalar_one_or_none()

    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    existing_book.title = book.title
    existing_book.author = book.author
    await db.commit()
    await db.refresh(existing_book)
    return existing_book

# ----------------------------
#     DELETE
# ----------------------------
@app.delete('/books/{book_id}', status_code=204)
async def delete_book(
    book_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Book).where(Book.id == book_id))
    existing_book = result.scalar_one_or_none()

    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    await db.delete(existing_book)
    await db.commit()
    return None