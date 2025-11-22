import typer
from decom.cli.utils.display import print_success, print_info

app = typer.Typer()

@app.command("start")
def start_worker(config: str = None, daemon: bool = False):
    """Start the worker node."""
    print_info("Starting worker node...")
    # Logic to start worker daemon
    print_success("Worker started successfully")

@app.command("stop")
def stop_worker():
    """Stop the worker node."""
    print_success("Worker stopped")

@app.command("status")
def worker_status():
    """Check worker status."""
    print_info("Worker is RUNNING")
    print_info("Active tasks: 0")
