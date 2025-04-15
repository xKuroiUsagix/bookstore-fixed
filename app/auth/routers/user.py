from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from database import get_db

from ..utils import get_password_hash
from ..schemas import UserCreateRequest, UserResponse
from ..models import User
from ..dependencies import get_current_user


router = APIRouter(prefix='/users')


@router.post('', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreateRequest, db: Session = Depends(get_db)):
    if user_data.password != user_data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='password and confirm_password do not match'
        )
    
    user_in_db = db.query(User).filter(or_(User.username == user_data.username, 
                                           User.email == user_data.email)).first()
    if user_in_db is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with provided username or email already exists'
        )
    
    user = User(
        username=user_data.username,
        email=user_data.email,
        password=get_password_hash(user_data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.get('', response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get('/me', response_model=UserResponse)
def get_user(current_user: UserResponse = Depends(get_current_user)):
    return current_user


@router.delete('/me', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(current_user: UserResponse = Depends(get_current_user), db: Session = Depends(get_db)):
    db.delete(current_user)
    db.commit()
