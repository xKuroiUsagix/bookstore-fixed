from sqlalchemy import String, Integer, Column, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from database import Base


class Book(Base):
    __tablename__ = 'Books'

    id = Column(Integer, primary_key=True)
    title = Column(String(128), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'))
    pub_date = Column(DateTime, nullable=False, default=func.now())

    author = relationship('Author', back_populates='books')
