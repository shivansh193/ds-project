import typer
from decom.cli.utils.display import print_success, print_info

app = typer.Typer()

@app.command("create")
def create_wallet():
    """Create a new wallet."""
    print_success("Wallet created: 0x123...abc")

@app.command("balance")
def wallet_balance():
    """Check wallet balance."""
    print_info("Balance: 1000 DECOM")

@app.command("deposit")
def deposit(amount: float):
    """Deposit funds."""
    print_success(f"Deposited {amount}")

@app.command("withdraw")
def withdraw(amount: float, address: str):
    """Withdraw funds."""
    print_success(f"Withdrew {amount} to {address}")
