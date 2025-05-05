import typer

from commands.init import app as init_app

app = typer.Typer()

app.add_typer(init_app)

if __name__ == "__main__":
    try:
        app()
    except Exception as e:
        print(str(e))
