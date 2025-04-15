from enum import Enum


class ROLE_CHOICES(str, Enum):
    ADMIN = 'admin'
    AUTHOR = 'author'
    READER = 'reader'
