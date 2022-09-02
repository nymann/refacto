import typer

app = typer.Typer()


@app.command()
def welcome(name: str) -> None:
    typer.echo(f"Welcome {name}!")


if __name__ == "__main__":
    app()
