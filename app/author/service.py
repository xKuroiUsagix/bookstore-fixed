from sqlalchemy.orm import Session

from auth.exceptions import UserNotFoundError, PermissionsError
from auth.models import User
from auth.constants import ROLE_CHOICES

from .models import Author
from .schemas import AuthorCreateRequest, AuthorUpdateRequest
from .exceptions import AlreadyAuthorError, AuthorNotFoundError


class AuthorService:
    def list(self, db: Session):
        return db.query(Author).all()

    def get(self, db: Session, id: int):
        author = db.query(Author).get(id)
        if author is None:
            raise AuthorNotFoundError(id)

        return author

    def create(self, db: Session, author_data: AuthorCreateRequest, current_user: User):
        author = db.query(Author).filter(Author.user_username == author_data.user_username).first()
        if author:
            raise AlreadyAuthorError

        user = db.query(User).filter(User.username == author_data.user_username).first()
        if user is None:
            raise UserNotFoundError

        if current_user.username != author_data.user_username and current_user.role != ROLE_CHOICES.ADMIN:
            raise PermissionsError
        
        author = Author(**author_data.model_dump())
        user.role = ROLE_CHOICES.AUTHOR

        db.add(author)
        db.commit()
        db.refresh(author)
        db.refresh(user)

        return author

    def update(self, db: Session, id: int, author_data: AuthorUpdateRequest, curret_user: User):
        author = db.query(Author).get(id)
        if author is None:
            raise AuthorNotFoundError(id)
        if curret_user.username != author.user_username and curret_user.role != ROLE_CHOICES.ADMIN:
            raise PermissionError
        
        if author_data.bio is not None:
            author.bio = author_data.bio
        
        db.commit()
        db.refresh(author)

        return author
    
    def delete(self, id: int, db: Session):
        author = db.query(Author).get(id)
        if author is None:
            raise AuthorNotFoundError(id)
        
        db.delete(author)


author_service = AuthorService()
