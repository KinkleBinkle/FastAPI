from pydantic import BaseModel, EmailStr

class bookCreate(BaseModel):
    title: str
    author: str

class bookResponse(bookCreate):
    id: int

    class Config:
        orm_mode = True