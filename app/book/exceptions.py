from fastapi import HTTPException, status


class BookNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='This book does not exist'
        )


class BookAlreadyExistsError(HTTPException):
    def __init__(self, title: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Book with title {title} already exists'
        )


class NotAuthorError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only book's author allowed to change its data"
        )
