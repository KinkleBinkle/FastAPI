from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List

from database import get_db
from models import Student, Book
from schemas import StudentResponse, StudentCreate, StudentUpdate

router = APIRouter()

@router.get('/{student_id}/books')
async def get_borrowed_books(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).where(Book.borrower_id == student_id))
    books = result.scalars().all()
    return books

@router.get('/', response_model=List[StudentResponse])
async def list_students(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Student).options(selectinload(Student.borrowed_books))
    )
    students = result.scalars().all()
    return students

@router.get('/{student_id}', response_model=StudentResponse)
async def get_student(
    student_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(
            select(Student).options(selectinload(Student.borrowed_books)).where(Student.id == student_id)
        )
        student = result.scalar_one_or_none()
        if student is None:
            raise HTTPException(status_code=404, detail="Student not found")
        return student
    except Exception as e:
        import traceback
        print("Error fetching student:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=StudentResponse)
async def create_student(student: StudentCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_student = Student(name=student.name, age=student.age)
        db.add(new_student)
        await db.commit()
        # Eagerly reload with borrowed_books for correct response serialization
        result = await db.execute(
            select(Student).options(selectinload(Student.borrowed_books)).where(Student.id == new_student.id)
        )
        student_with_books = result.scalar_one()
        return student_with_books
    except Exception as e:
        import traceback
        print("Error creating student:", e)
        traceback.print_exc()
        # Return error details for debugging (remove in production)
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{student_id}", response_model=StudentResponse)
async def update_student(
        student_id: int,
        student_update: StudentUpdate,
        db: AsyncSession = Depends(get_db)
    ):

    result = await db.execute(select(Student).where(Student.id == student_id))
    existing_student = result.scalar_one_or_none()

    if not existing_student:
        raise HTTPException(status=404, detail="Student not found")
    
    if student_update.name:
        existing_student.name = student_update.name
    if student_update.age:
        existing_student.age = student_update.age

    await db.commit()
    await db.refresh(existing_student)

    result = await db.execute(
        select(Student)
        .options(selectinload(Student.borrowed_books))
        .where(Student.id == student_id)
    )

    update_student = result.scalar_one()
    return update_student  


@router.delete("/{student_id}", status_code=204)
async def delete_student(
    student_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Student).where(Student.id == student_id))
    existing_student = result.scalar_one_or_none()

    if not existing_student:
        raise HTTPException(status=404, detail="Student not found")
    
    await db.delete(existing_student)
    await db.commit()
    return None