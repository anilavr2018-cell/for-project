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
import subprocess
from datetime import date as dt_date
import typer
from rich import print

app = typer.Typer(
    name="trackit",
    help="📊 TrackIt - Local commit tracking and work performance audit tool."
)

def fetch_git_commits(target_date: str = "today", file_path: str = None):
    """Helper function to execute git log and parse commits into Python dictionaries."""
    
    # Resolve 'today' to YYYY-MM-DD
    if target_date == "today":
        target_date = dt_date.today().strftime("%Y-%m-%d")

    since_str = f"{target_date} 00:00:00"
    until_str = f"{target_date} 23:59:59"

    # Construct the git command
    cmd = [
        "git", "log",
        f"--since={since_str}",
        f"--until={until_str}",
        "--pretty=format:%h|%an|%ad|%s",
        "--date=format:%I:%M %p"
    ]

    # If a specific file path is requested, append it
    if file_path:
        cmd.extend(["--", file_path])

    try:
        # Run git log command in the background
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        raw_output = result.stdout.strip()

        if not raw_output:
            return target_date, []

        commits = []
        for line in raw_output.split("\n"):
            parts = line.split("|", 3)
            if len(parts) == 4:
                commits.append({
                    "hash": parts[0],
                    "author": parts[1],
                    "time": parts[2],
                    "message": parts[3]
                })
        return target_date, commits

    except subprocess.CalledProcessError:
        print("[bold red]Error:[/] Current directory is not a valid Git repository or Git is not installed.")
        raise typer.Exit(code=1)


@app.command()
def summary(
    date: str = typer.Option("today", "--date", "-d", help="Target date (YYYY-MM-DD or 'today')")
):
    """
    Show overall real commit summary for a specific date.
    """
    resolved_date, commits = fetch_git_commits(target_date=date)

    print(f"\n[bold green]📊 Daily Work Audit for:[/] [yellow]{resolved_date}[/yellow]")
    print("-" * 50)

    if not commits:
        print("[dim]No commits found on this date.[/dim]\n")
        return

    print(f"[bold]Total Commits:[/]      {len(commits)}\n")
    print("[bold]Commit History:[/")
    for c in commits:
        print(f"  • [yellow]{c['time']}[/] [[cyan]{c['hash']}[/]] {c['message']} [dim]({c['author']})[/dim]")
    print()


@app.command()
def analyze(
    file: str = typer.Option(..., "--file", "-f", help="Path to the file you want to track"),
    date: str = typer.Option("today", "--date", "-d", help="Target date (YYYY-MM-DD or 'today')")
):
    """
    Analyze commit history for a specific file on a given date.
    """
    resolved_date, commits = fetch_git_commits(target_date=date, file_path=file)

    print(f"\n[bold blue]🔍 Analyzing File:[/] [bold]{file}[/] on [yellow]{resolved_date}[/yellow]")
    print("-" * 50)

    if not commits:
        print(f"[dim]No commits found for file '{file}' on this date.[/dim]\n")
        return

    print(f"[bold]Total File Commits:[/] {len(commits)}\n")
    for c in commits:
        print(f"  • [yellow]{c['time']}[/] [[cyan]{c['hash']}[/]] {c['message']}")
    print()


if __name__ == "__main__":
    app()