from fastapi import HTTPException, status


class AuthorNotFoundError(HTTPException):
    def __init__(self, author_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Author with id {author_id} not found'
        )
