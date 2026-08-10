import typer
from rich import print

# Initialize Typer CLI App
app = typer.Typer(
    name="trackit",
    help="📊 TrackIt - Local commit tracking and work performance audit tool."
)

@app.command()
def summary(
    date: str = typer.Option("today", "--date", "-d", help="Target date (YYYY-MM-DD or 'today')")
):
    """
    Show overall commit summary and estimated time spent for a specific date.
    """
    print(f"\n[bold green]📊 Daily Work Audit for:[/] [yellow]{date}[/yellow]")
    print("-" * 45)
    
    # Placeholder data (we will connect Git log parser in the next step)
    print("[bold]Total Commits:[/]      6")
    print("[bold]Est. Active Time:[/]   3 hours 15 minutes")
    print("[bold]Files Touched:[/]      2 (main.py, utils.py)\n")


@app.command()
def analyze(
    file: str = typer.Option(..., "--file", "-f", help="Path to the file you want to track"),
    date: str = typer.Option("today", "--date", "-d", help="Target date (YYYY-MM-DD or 'today')")
):
    """
    Analyze commit history and estimated time for a specific file on a given date.
    """
    print(f"\n[bold blue]🔍 Analyzing File:[/] [bold]{file}[/] on [yellow]{date}[/yellow]")
    print("-" * 45)
    
    # Placeholder timeline
    print(f"• 09:15 AM - {file} [dim](Est. 30m)[/] - Initial structure setup")
    print(f"• 10:00 AM - {file} [dim](Est. 45m)[/] - Fixed validation bug\n")


if __name__ == "__main__":
    app()
