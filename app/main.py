import uvicorn
from fastapi import FastAPI, Depends

from database import Base, engine

from auth.dependencies import get_current_user
from auth.routers.user import router as user_router
from auth.routers.authentication import router as auth_router
from author.router import router as author_router
from book.router import router as book_router


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router, tags=['Users'])
app.include_router(auth_router, tags=['Auth'])
app.include_router(author_router, dependencies=[Depends(get_current_user)], tags=['Authors'])
app.include_router(book_router, tags=['Books'])


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
