import typer

from commands.init import app as init_app

app = typer.Typer()

app.add_typer(init_app)
# TODO Add commands for: git add <file>, git commit, git status, git diff, git log, git branch,
#  git checkout <branch>, git merge <branch>, git rebase <branch>, git reset, git rm <file>, git stash, git clean

if __name__ == "__main__":
    try:
        app()
    except Exception as e:
        print(str(e))
