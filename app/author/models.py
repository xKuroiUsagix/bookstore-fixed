from sqlalchemy import Text, ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    user_username = Column(String, ForeignKey('users.username'))
    bio = Column(Text, nullable=True)

    user = relationship('User', back_populates='author', foreign_keys=[user_username])
    books = relationship('Book', back_populates='author')
