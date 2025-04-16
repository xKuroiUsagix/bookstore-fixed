import typer

from sqlalchemy import or_
from passlib.context import CryptContext
from pydantic import ValidationError

from author.models import Author
from book.models import Book
from auth.models import User
from auth.constants import ROLE_CHOICES
from auth.schemas import UserCreateRequest

from database import get_db


app = typer.Typer()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@app.command('create-superuser')
def create_superuser():
    db = next(get_db())

    while True:
        username = typer.prompt('Username')
        email = typer.prompt('Email')
        password = typer.prompt('Password', hide_input=True)
        confirm_password = typer.prompt('Confirm Password', hide_input=True)

        if db.query(User).filter(or_(User.username == username, User.email == email)).first():
            typer.secho('Provided username and/or email already in use', fg=typer.colors.RED)
            continue
        if password != confirm_password:
            typer.secho('password and confirm_password do not match', fg=typer.colors.RED)
            continue
        
        try:
            user_data = UserCreateRequest(
                username=username, 
                email=email, 
                password=password, 
                confirm_password=confirm_password
            )
            break
        except ValidationError as e:
            typer.secho('Provided data was not validated. See info below.', fg=typer.colors.RED)
            print(e.errors())

    user = User()
    user.username = user_data.username
    user.email = user_data.email
    user.password = pwd_context.hash(user_data.password)
    user.role = ROLE_CHOICES.ADMIN

    db.add(user)
    db.commit()

    typer.secho('User created succsessfully', fg=typer.colors.GREEN)
