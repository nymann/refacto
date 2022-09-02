import typer

from refacto.server import server

app = typer.Typer()

Host: str = typer.Option(default="localhost")
Port: int = typer.Option(default=8080)


@app.command()
def tcp(host: str = Host, port: int = Port) -> None:
    server.start_tcp(host=host, port=port)


if __name__ == "__main__":
    app()
