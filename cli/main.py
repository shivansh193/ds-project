import typer
from cli.commands import bounty, worker

app = typer.Typer(help="Decom CLI - Decentralized Compute Network")

app.add_typer(bounty.app, name="bounty", help="Manage bounties")
app.add_typer(worker.app, name="worker", help="Worker operations")

if __name__ == "__main__":
    app()
