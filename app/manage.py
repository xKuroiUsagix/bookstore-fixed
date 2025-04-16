import typer

from auth.commands import create_superuser


app = typer.Typer()
app.add_typer(create_superuser.app)

if __name__ == "__main__":
    app()
