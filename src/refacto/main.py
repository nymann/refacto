import typer

from refacto.server import refacto_server

app = typer.Typer()

DEFAULT_PORT = 8080
Host: str = typer.Option(default="localhost")
Port: int = typer.Option(default=DEFAULT_PORT)


@app.command()
def tcp(host: str = Host, port: int = Port) -> None:
    refacto_server.start_tcp(host=host, port=port)  # type: ignore


if __name__ == "__main__":
    app()
