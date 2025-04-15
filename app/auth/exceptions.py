from fastapi import HTTPException, status


class PermissionsError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not enough permissions for this action'
        )
