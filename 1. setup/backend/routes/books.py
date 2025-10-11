from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from database import get_db
from models import Book, Student
from schemas import BookResponse, BookCreate, BookUpdate, BorrowRequest

router = APIRouter()

# ----------------------------
#     GET
# ----------------------------
@router.get('/', response_model=List[BookResponse])
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

@router.get('/{book_id}', response_model=BookResponse)
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

@router.post("/", response_model=BookResponse)
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    new_book = Book(title = book.title, author = book.author)
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book

@router.post('/borrow')
async def borrow_book(request: BorrowRequest, db: AsyncSession = Depends(get_db)):

    # Check if student exists
    student_result = await db.execute(select(Student).where(Student.id == request.student_id))
    student = student_result.scalar_one_or_none()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if book exists
    book_result = await db.execute(select(Book).where(Book.id == request.book_id))
    book = book_result.scalar_one_or_none()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    book.borrower_id = student.id
    await db.commit()
    await db.refresh(book)

    return {"message": f"{student.name} borrowed {book.title} successfully"}



# ----------------------------
#     PUT
# ----------------------------

@router.put('/{book_id}', response_model=BookResponse)
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
@router.delete('/{book_id}', status_code=204)
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