from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship

from database import Base

from .constants import ROLE_CHOICES


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(128), nullable=False, unique=True)
    email = Column(String(256), nullable=False, unique=True)
    password = Column(String(64), nullable=False)
    role = Column(String, nullable=False, default=ROLE_CHOICES.READER)

    author = relationship('Author', back_populates='user', uselist=False, cascade='all, delete-orphan')
