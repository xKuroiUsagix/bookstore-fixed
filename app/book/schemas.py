from pydantic import BaseModel, NaiveDatetime


class BookCreateRequest(BaseModel):
    author_id: int
    title: str
    description: str | None = None


class BookUpadateRequest(BaseModel):
    author_id: int | None = None
    title: str | None = None
    description: str | None = None


class BookResponse(BookCreateRequest):
    id: int
    pub_date: NaiveDatetime
