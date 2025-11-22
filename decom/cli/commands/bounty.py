import typer
from decom.cli.utils.display import print_success, print_error, print_table

app = typer.Typer()

@app.command("raise")
def raise_bounty(file_path: str, budget: float, timeout: int = 3600, redundancy: int = 3):
    """Raise a new bounty for a compute task."""
    # Placeholder for logic
    print_success(f"Bounty raised for {file_path} with budget {budget}")

@app.command("list")
def list_bounties(status: str = "active", mine: bool = False):
    """List available bounties."""
    # Placeholder for logic
    rows = [
        ("1", "task.py", "100", "active"),
        ("2", "calc.py", "50", "pending"),
    ]
    print_table("Bounties", ["ID", "File", "Budget", "Status"], rows)

@app.command("cancel")
def cancel_bounty(bounty_id: str):
    """Cancel an active bounty."""
    print_success(f"Bounty {bounty_id} cancelled")

@app.command("details")
def bounty_details(bounty_id: str):
    """Show details of a specific bounty."""
    print_success(f"Details for bounty {bounty_id}")
