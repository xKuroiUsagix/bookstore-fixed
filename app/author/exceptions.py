from fastapi import HTTPException, status


class AuthorNotFoundError(HTTPException):
    def __init__(self, author_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Author with id {author_id} not found'
        )


class AlreadyAuthorError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='This user is already an author'
        )
