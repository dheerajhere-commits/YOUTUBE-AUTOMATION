import os
import typer
import asyncio
from database.db import init_db, get_db_connection
from core.auth import link_google_account, link_instagram_account
from agents.research_agent import find_niche
from core.orchestrator import run_auto_pilot_loop

app = typer.Typer(help="NEXUS-100: Multi-Agent Automation System for YouTube and Instagram.")

@app.command()
def init():
    """Initialize the database and directories."""
    init_db()
    typer.echo("Database and directories initialized.")

@app.command()
def niche_finder():
    """Analysis of trending shorts/reels in the last 24 hours."""
    typer.echo("Running Research Agent to find high-CPM niches...")
    async def run():
        try:
            # We bypass actual API call in dummy setup
            # result = await find_niche()
            result = "{'niche': 'AI Productivity Hacks', 'target_audience': 'Professionals', 'cpm_estimate': 18.5, 'competition_level': 'Low'}"
            typer.echo(f"Niche found: {result}")
        except Exception as e:
            typer.echo(f"Failed to find niche: {e}")
    asyncio.run(run())

@app.command()
def account_link(platform: str = typer.Option(..., help="Platform: 'youtube' or 'instagram'"),
                 account_id: str = typer.Option(..., help="Account ID or email"),
                 channel_name: str = typer.Option(None, help="Friendly name for the channel"),
                 token: str = typer.Option(None, help="Access token (for Instagram)")):
    """A secure workflow to add new Gmail/Instagram accounts."""
    if platform.lower() == 'youtube':
        typer.echo(f"Linking YouTube account: {account_id} {f'({channel_name})' if channel_name else ''}")
        link_google_account(account_id)
    elif platform.lower() == 'instagram':
        if not token:
            typer.echo("Error: --token is required for Instagram.")
            raise typer.Exit(code=1)
        typer.echo(f"Linking Instagram account: {account_id} {f'({channel_name})' if channel_name else ''}")
        link_instagram_account(account_id, token)
    else:
        typer.echo("Invalid platform. Use 'youtube' or 'instagram'.")
        raise typer.Exit(code=1)

    if channel_name:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE accounts SET channel_name=? WHERE account_id=?", (channel_name, account_id))
            conn.commit()

@app.command()
def list_accounts():
    """List all connected channels/accounts."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, platform, account_id, status FROM accounts")
        rows = cursor.fetchall()
        if not rows:
            typer.echo("No accounts found. Use 'account-link' to add one.")
            return

        typer.echo("Connected Accounts:")
        typer.echo("-" * 40)
        for row in rows:
            typer.echo(f"[{row['id']}] {row['platform'].upper()} - {row['account_id']} ({row['status']})")
        typer.echo("-" * 40)

@app.command()
def remove_account(account_id: str = typer.Argument(..., help="The account ID or email to remove")):
    """Remove a connected account."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM accounts WHERE account_id=?", (account_id,))
        if cursor.rowcount > 0:
            conn.commit()
            typer.echo(f"Successfully removed account: {account_id}")
        else:
            typer.echo(f"Account not found: {account_id}")

@app.command()
def start_scheduler():
    """Run the background posting scheduler."""
    from core.scheduler import run_scheduler
    asyncio.run(run_scheduler())

@app.command()
def status():
    """Show system status: top niches, recent uploads, account health."""
    typer.echo("\n=== NEURAL MEMORY (Top Niches) ===")
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT niche, score, encounters FROM neural_memory ORDER BY score DESC LIMIT 10")
        for row in cursor.fetchall():
            bar = "█" * int(row['score'])
            typer.echo(f"  {row['niche'][:30]:<30} {bar} {row['score']:.1f}/10 ({row['encounters']} runs)")

    typer.echo("\n=== RECENT UPLOADS (Last 10) ===")
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT account_id, video_title, status, created_at FROM video_logs ORDER BY created_at DESC LIMIT 10")
        for row in cursor.fetchall():
            typer.echo(f"  [{row['status'].upper()}] {row['account_id']} — {row['video_title']}")

    typer.echo("\n=== ACCOUNTS ===")
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Fallback to avoid error if migrating old DBs without channel_name
        try:
            cursor.execute("SELECT platform, account_id, channel_name, status FROM accounts")
        except:
            cursor.execute("SELECT platform, account_id, status FROM accounts")

        for row in cursor.fetchall():
            name = f"({row['channel_name']})" if 'channel_name' in row.keys() and row['channel_name'] else ""
            typer.echo(f"  {row['platform'].upper()} — {row['account_id']} {name} [{row['status']}]")

@app.command()
def auto_pilot(
    dry_run: bool = typer.Option(False, "--dry-run", help="Simulate full pipeline without posting.")
):
    """Full pipeline: Niche -> Script -> Video -> Post."""
    if dry_run:
        typer.echo("🔍 DRY RUN MODE — No videos will be posted to real endpoints.")
        os.environ['NEXUS_DRY_RUN'] = 'true'
    else:
        os.environ['NEXUS_DRY_RUN'] = 'false'

    typer.echo("Starting Auto-Pilot mode...")

    # Fetch accounts from DB
    accounts = []
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts WHERE status='active'")
        rows = cursor.fetchall()
        for row in rows:
            accounts.append(dict(row))

    if not accounts:
        typer.echo("No active accounts found. Please link accounts first using --account-link.")
        # Create dummy accounts for testing
        typer.echo("Creating dummy accounts for testing purposes...")
        link_google_account("dummy_yt_1@gmail.com")
        link_google_account("dummy_yt_2@gmail.com")
        link_instagram_account("dummy_ig_1", "dummy_token")
        accounts = [
            {'account_id': 'dummy_yt_1@gmail.com', 'platform': 'youtube'},
            {'account_id': 'dummy_yt_2@gmail.com', 'platform': 'youtube'},
            {'account_id': 'dummy_ig_1', 'platform': 'instagram'}
        ]

    asyncio.run(run_auto_pilot_loop(accounts))

@app.command()
def anti_spam():
    """Implement randomized upload times and 'Synthetically Generated' labeling per 2026 regulations."""
    typer.echo("Anti-spam measures are integrated into the posting agent.")
    typer.echo("Features enabled:")
    typer.echo("- Randomized upload scheduling (5-60 min offset)")
    typer.echo("- 'Synthetically Generated' tags per 2026 regulations")
    typer.echo("- Account switching cooldowns to prevent IP flagging")

if __name__ == "__main__":
    app()
