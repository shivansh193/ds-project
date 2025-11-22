import typer
from decom.cli.commands import bounty, bidding, worker, wallet, monitoring

app = typer.Typer(help="Decentralized Compute Network CLI")

app.add_typer(bounty.app, name="bounty", help="Manage bounties")
app.add_typer(bidding.app, name="bid", help="Manage bids")
app.add_typer(worker.app, name="worker", help="Manage worker node")
app.add_typer(wallet.app, name="wallet", help="Manage wallet")
app.add_typer(monitoring.app, name="monitor", help="Monitor network and tasks")

if __name__ == "__main__":
    app()
