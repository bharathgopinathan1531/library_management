from fastapi import HTTPException
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas

from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Home API
@app.get("/")
def home():
    return {"message": "Library Management System"}


# Add Book API
@app.post("/books")
def add_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db)
):
    new_book = models.Book(
        title=book.title,
        author=book.author,
        category=book.category,
        available_copies=book.available_copies
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book

# View all books API
@app.get("/books")
def get_books(
    skip: int = 0,
    limi: int = 10,
    db: Session = Depends(get_db)):
    return 
    db.query(models.Book).offset(skip).limit(limit).all()

@app.get("/books/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):

    book = db.query(models.Book).filter(
        models.Book.id == book_id
    ).first()

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return book

@app.put("/books/{book_id}")
def update_book(
    book_id: int,
    updated_book: schemas.BookCreate,
    db: Session = Depends(get_db)
):

    book = db.query(models.Book).filter(
        models.Book.id == book_id
    ).first()

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    book.title = updated_book.title
    book.author = updated_book.author
    book.category = updated_book.category
    book.available_copies = updated_book.available_copies

    db.commit()

    return {"message": "Book updated successfully"}

@app.delete("/books/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db)
):

    book = db.query(models.Book).filter(
        models.Book.id == book_id
    ).first()

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    db.delete(book)
    db.commit()

    return {"message": "Book deleted successfully"}

@app.post("/members")
def add_member(
    member: schemas.MemberCreate,
    db: Session = Depends(get_db)
):

    existing_member = db.query(models.Member).filter(
        models.Member.email == member.email
    ).first()

    if existing_member:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_member = models.Member(
        name=member.name,
        email=member.email,
        phone=member.phone
    )

    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return new_member

@app.get("/members")
def get_members(db: Session = Depends(get_db)):
    return db.query(models.Member).all()

@app.put("/members/{member_id}")
def update_member(
    member_id: int,
    member: schemas.MemberCreate,
    db: Session = Depends(get_db)
):
    db_member = db.query(models.Member).filter(
        models.Member.id == member_id
    ).first()

    if not db_member:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    db_member.name = member.name
    db_member.email = member.email
    db_member.phone = member.phone

    db.commit()

    return {"message": "Member updated successfully"}

@app.delete("/members/{member_id}")
def delete_member(
    member_id: int,
    db: Session = Depends(get_db)
):
    db_member = db.query(models.Member).filter(
        models.Member.id == member_id
    ).first()

    if not db_member:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    db.delete(db_member)
    db.commit()

    return {"message": "Member deleted successfully"}

@app.post("/borrow")
def borrow_book(
    borrow: schemas.BorrowCreate,
    db: Session = Depends(get_db)
):
    member = db.query(models.Member).filter(
        models.Member.id == borrow.member_id
    ).first()

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    book = db.query(models.Book).filter(
        models.Book.id == borrow.book_id
    ).first()

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    if book.available_copies <= 0:
        raise HTTPException(
            status_code=400,
            detail="Book not available"
        )

    new_borrow = models.Borrow(
        member_id=borrow.member_id,
        book_id=borrow.book_id
    )

    book.available_copies -= 1

    db.add(new_borrow)
    db.commit()
    db.refresh(new_borrow)

    return new_borrow

@app.get("/borrowed")
def get_borrowed_books(db: Session = Depends(get_db)):
    return db.query(models.Borrow).all()

@app.post("/return")
def return_book(data: schemas.BorrowCreate, db: Session = Depends(get_db)):

    borrow = db.query(models.Borrow).filter(
        models.Borrow.member_id == data.member_id,
        models.Borrow.book_id == data.book_id
    ).first()

    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow record not found")

    book = db.query(models.Book).filter(
        models.Book.id == data.book_id
    ).first()

    book.available_copies += 1

    db.delete(borrow)
    db.commit()

    return {"message": "Book returned successfully"}

@app.get("/search")
def search_books(
    title: str = None,
    category: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Book)

    if title:
        query = query.filter(
            models.Book.title.contains(title)
        )

    if category:
        query = query.filter(
            models.Book.category.contains(category)
        )

    return query.all()
