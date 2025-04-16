from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from auth.dependencies import IsAdmin, IsAdminOrAuthor, get_current_user
from auth.models import User
from auth.constants import ROLE_CHOICES

from database import get_db

from .schemas import AuthorResponse, AuthorCreateRequest, AuthorUpdateRequest
from .models import Author
from .service import author_service


router = APIRouter(prefix='/authors')


@router.post('', response_model=AuthorResponse, status_code=status.HTTP_201_CREATED)
def create_author(
    author_data: AuthorCreateRequest, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return author_service.create(db, author_data, current_user)


@router.get('', response_model=List[AuthorResponse])
def list_authors(db: Session = Depends(get_db)):
    return author_service.list(db)


@router.get('/{author_id}', response_model=AuthorResponse)
def get_author(author_id: int, db: Session = Depends(get_db)):
    return author_service.get(db, author_id)


@router.patch('/{author_id}', response_model=AuthorResponse)
def update_author_partially(
    author_id: int,
    author_data: AuthorUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(IsAdminOrAuthor())
):
    return author_service.update(db, author_id, author_data, current_user)


@router.delete('/{author_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, db: Session = Depends(get_db), _: bool = Depends(IsAdmin())):
    author_service.delete(author_id)
