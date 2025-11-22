import typer
from decom.cli.utils.display import print_info

app = typer.Typer()

@app.command("task-status")
def task_status(bounty_id: str, follow: bool = False):
    """Check status of a task."""
    print_info(f"Task {bounty_id}: RUNNING")

@app.command("logs")
def logs(bounty_id: str, worker_id: str = None, tail: bool = False):
    """View task logs."""
    print_info("Log line 1...")
    print_info("Log line 2...")

@app.command("network-stats")
def network_stats():
    """View network statistics."""
    print_info("Active Workers: 5")
    print_info("Pending Bounties: 2")
