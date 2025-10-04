from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str

class BookUpdate(BaseModel):
    title: str
    author: str

class BookResponse(BookCreate):
    id: int

    class Config:
        from_attributes = True  # ✅ Pydantic v2 fix for orm_mode
