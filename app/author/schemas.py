from pydantic import BaseModel


class AuthorCreateRequest(BaseModel):
    user_username: str
    bio: str | None = None

class AuthorResponse(AuthorCreateRequest):
    id: int

class AuthorUpdateRequest(BaseModel):
    bio: str | None = None
