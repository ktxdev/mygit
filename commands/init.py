import os
import typer

app = typer.Typer()


@app.command()
def init():  # TODO (1) Add an argument for the directory if you want to initialize elsewhere
    """
    Initializes a new mygit repository
    """
    repo_dir = os.getcwd()
    if os.path.exists(os.path.join(repo_dir, ".mygit")):
        raise ValueError("Repository already initialized")

    os.makedirs(os.path.join(repo_dir, ".mygit"))
    print("Initialized empty mygit repository.")
