from pydantic import BaseModel
from typing import List, Optional

# ----------------------------
# Book Schemas
# ----------------------------

class BookBase(BaseModel):
    title: str
    author: str

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

# This schema is for responding with a Book's details.
# It does NOT include the 'borrower' to avoid recursion.
class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True

# ----------------------------
# Student Schemas
# ----------------------------

class StudentBase(BaseModel):
    name: str
    age: int

class StudentCreate(StudentBase):
    pass

class StudentUpdate(StudentBase):
    name: Optional[str] = None
    age: Optional[int] = None

# This is the key schema for your endpoint.
# It includes a list of BookResponse objects.
class StudentResponse(StudentBase):
    id: int
    borrowed_books: List[BookResponse] = []

    class Config:
        from_attributes = True

# Optional: If you ever need a Book response that INCLUDES the student details
class BookResponseWithBorrower(BookResponse):
    # We need to forward-declare StudentBase to avoid circular import issues
    # if schemas are in the same file. Pydantic handles this.
    borrower: Optional[StudentBase] = None