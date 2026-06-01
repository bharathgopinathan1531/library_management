from pydantic import EmailStr, Field
from pydantic import BaseModel, EmailStr, Field

class MemberCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str = Field(
        min_length=10,
        max_length=10
    )


class MemberResponse(MemberCreate):
    id: int

    class Config:
        from_attributes = True

class BookCreate(BaseModel):
    title: str
    author: str
    category: str
    available_copies: int


class BookResponse(BookCreate):
    id: int

    class Config:
        from_attributes = True
        
class BorrowCreate(BaseModel):
    member_id: int
    book_id: int 
    
class BorrowResponse(BorrowCreate):
    id :int
    
    class Config:
        from_attributes= True           