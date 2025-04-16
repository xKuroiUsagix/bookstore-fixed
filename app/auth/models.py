from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship

from author.models import Author

from database import Base

from .constants import ROLE_CHOICES


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(128), nullable=False, unique=True)
    email = Column(String(256), nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default=ROLE_CHOICES.READER)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=True)

    author = relationship('Author', back_populates='user', uselist=False, foreign_keys=[Author.user_username], cascade='all, delete-orphan')
