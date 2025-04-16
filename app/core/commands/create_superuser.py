import typer

from passlib.context import CryptContext

from author.models import Author
from book.models import Book
from auth.models import User
from auth.constants import ROLE_CHOICES

from database import get_db


cli = typer.Typer()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@cli.command()
def create_superuser(
    username: str = typer.Argument(..., help='The username for the new user.'),
    email: str = typer.Argument(..., help='The email address for the new user.'),
    password: str = typer.Option(..., prompt=True, hide_input=True, help='The password for the new user.')
):
    # This is just temporary solution. It has really bad implementation
    hashed_password = pwd_context.hash(password)
    db = next(get_db())
    
    user = User()
    user.username = username
    user.email = email
    user.password = hashed_password
    user.role = ROLE_CHOICES.ADMIN

    db.add(user)
    db.commit()

    print('User was created succsessfully')


if __name__ == '__main__':
    cli()
