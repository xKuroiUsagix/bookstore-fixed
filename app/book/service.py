from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from auth.models import User
from auth.exceptions import PermissionsError
from auth.constants import ROLE_CHOICES
from author.models import Author
from author.exceptions import AuthorNotFoundError

from .models import Book
from .schemas import BookCreateRequest, BookUpadateRequest
from .exceptions import BookAlreadyExistsError, BookNotFoundError, NotAuthorError


class BookService:
    def list(self, db: Session) -> list[Book]:
        return db.query(Book).all()

    def get(self, db: Session, id: int) -> Book:
        book = db.query(Book).get(id)
        if book is None:
            raise BookNotFoundError
        return book

    def create(self, db: Session, book_data: BookCreateRequest, current_user: User) -> Book:
        if book_data.author_id != current_user.author.id and current_user.role != ROLE_CHOICES.ADMIN:
            raise PermissionsError
        
        book = Book(**book_data.model_dump())

        try:
            db.add(book)
            db.commit()
            db.refresh(book)
        except IntegrityError as e:
            db.rollback()
            raise BookAlreadyExistsError(book_data.title)

        return book

    def update(self, db: Session, id: int, book_data: BookUpadateRequest, current_user: User) -> Book:
        book = db.query(Book).get(id)
        if book is None:
            raise BookNotFoundError

        if book_data.author_id is not None:
            author = db.query(Author).get(book_data.author_id)
            if author is None:
                raise AuthorNotFoundError(book_data.author_id)
            if author.user_username != current_user.username and current_user.role != ROLE_CHOICES.ADMIN:
                raise NotAuthorError
            
            book.author_id = book_data.author_id
    
        if book_data.title is not None:
            book.title = book_data.title
        if book_data.description is not None:
            book.description = book_data.description
        
        try:
            db.commit()
            db.refresh(book)
        except IntegrityError as e:
            db.rollback()
            raise BookAlreadyExistsError(book_data.title)
        
        return book
    
    def delete(self, db: Session, id: int) -> None:
        book = db.query(Book).get(id)
        if book is None:
            raise BookNotFoundError

        db.delete(book)
        db.commit()


book_service = BookService()
