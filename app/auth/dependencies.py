import jwt
from jwt.exceptions import InvalidTokenError

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status

from database import get_db
from settings import settings

from .schemas import TokenData
from .utils import oauth2_scheme
from .models import User
from .constants import ROLE_CHOICES
from .exceptions import PermissionsError


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username = payload.get('sub')
        
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == token_data.username).first()

    if user is None:
        raise credentials_exception
    return user


class PermissionBase:
    def __init__(self):
        self.allowed_roles = [role.value for role in ROLE_CHOICES]
    
    def __call__(self, user: User = Depends(get_current_user)):
        if user.role in self.allowed_roles:
            return True
        raise PermissionsError


class IsAdminOrAuthor(PermissionBase):
    def __init__(self):
        self.allowed_roles = [ROLE_CHOICES.ADMIN, ROLE_CHOICES.AUTHOR]


class IsAdmin(PermissionBase):
    def __init__(self):
        self.allowed_roles = [ROLE_CHOICES.ADMIN]
