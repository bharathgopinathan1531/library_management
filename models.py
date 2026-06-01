from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy import ForeignKey


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    category = Column(String)
    available_copies = Column(Integer)
    
class Member(Base):
     __tablename__ = "members"

     id = Column(Integer, primary_key=True, index=True)
     name = Column(String)
     email = Column(String, unique=True)
     phone = Column(String)   
     
class Borrow(Base):
     __tablename__ = "borrow_records"

     id = Column(Integer, primary_key=True, index=True)
     member_id = Column(Integer, ForeignKey("members.id"))
     book_id = Column(Integer, ForeignKey("books.id"))