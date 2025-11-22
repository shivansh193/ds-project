import typer
from decom.cli.utils.display import print_success, print_table

app = typer.Typer()

@app.command("place")
def place_bid(bounty_id: str, price: float, eta: int):
    """Place a bid on a bounty."""
    print_success(f"Bid placed on {bounty_id} for {price} (ETA: {eta}m)")

@app.command("list")
def list_bids(bounty_id: str = None, mine: bool = False):
    """List bids for a bounty."""
    rows = [
        ("1", "worker_1", "90", "30m"),
        ("2", "worker_2", "95", "25m"),
    ]
    print_table("Bids", ["ID", "Worker", "Price", "ETA"], rows)

@app.command("accept")
def accept_bid(bid_id: str):
    """Accept a bid."""
    print_success(f"Bid {bid_id} accepted")

@app.command("reject")
def reject_bid(bid_id: str):
    """Reject a bid."""
    print_success(f"Bid {bid_id} rejected")
