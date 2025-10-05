from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    
    # Add the foreign key to the students table
    borrower_id = Column(Integer, ForeignKey("students.id"))
    
    # This relationship links this Book to a Student
    borrower = relationship("Student", back_populates="borrowed_books")

class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    
    # This relationship links this Student to their borrowed Books
    borrowed_books = relationship("Book", back_populates="borrower")