from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from database import get_db

from auth.models import User
from auth.dependencies import IsAdminOrAuthor, IsAdmin, get_current_user

from .schemas import BookCreateRequest, BookResponse, BookUpadateRequest
from .service import book_service


router = APIRouter(prefix='/books')


@router.post('', response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(
    book_data: BookCreateRequest, 
    db: Session = Depends(get_db), 
    _: bool = Depends(IsAdminOrAuthor())
):
    return book_service.create(db, book_data)


@router.get('', response_model=List[BookResponse])
def list_books(db: Session = Depends(get_db)):
    return book_service.list(db)


@router.get('/{book_id}', response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    return book_service.get(db, book_id)


@router.put('/{book_id}', response_model=BookResponse)
def update_book(
    book_id: int, 
    book_data: BookCreateRequest, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(IsAdminOrAuthor())
):
    return book_service.update(db, book_id, book_data, current_user)


@router.patch('/{book_id}', response_model=BookResponse)
def update_book_partially(
    book_id: int,
    book_data: BookUpadateRequest, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(IsAdminOrAuthor())
):
    return book_service.update(db, book_id, book_data, current_user)


@router.delete('/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int, 
    db: Session = Depends(get_db), 
    _: bool = Depends(IsAdmin())
):
    book_service.delete(db, book_id)
