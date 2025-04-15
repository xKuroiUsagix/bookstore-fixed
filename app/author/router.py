from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from auth.dependencies import IsAdmin
from auth.models import User
from auth.constants import ROLE_CHOICES

from database import get_db

from .schemas import AuthorResponse, AuthorCreateRequest
from .models import Author


router = APIRouter(prefix='/authors')


@router.post('', response_model=AuthorResponse, status_code=status.HTTP_201_CREATED)
def create_author(
    author_data: AuthorCreateRequest, 
    db: Session = Depends(get_db), 
    _: bool = Depends(IsAdmin())
):
    author = db.query(Author).filter(Author.user_username == author_data.user_username).first()
    if author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='This user is already an author'
        )

    user = db.query(User).filter(User.username == author_data.user_username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='This username does not exist'
        )
    
    author = Author(**author_data.model_dump())
    user.role = ROLE_CHOICES.AUTHOR

    db.add(author)
    db.commit()
    db.refresh(author)
    db.refresh(user)

    return author


@router.get('', response_model=List[AuthorResponse])
def list_authors(db: Session = Depends(get_db)):
    return db.query(Author).all()
