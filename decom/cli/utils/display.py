from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def print_table(title, columns, rows):
    table = Table(title=title)
    for col in columns:
        table.add_column(col)
    for row in rows:
        table.add_row(*row)
    console.print(table)

def print_success(message):
    console.print(f"[bold green]SUCCESS:[/bold green] {message}")

def print_error(message):
    console.print(f"[bold red]ERROR:[/bold red] {message}")

def print_info(message):
    console.print(f"[bold blue]INFO:[/bold blue] {message}")
