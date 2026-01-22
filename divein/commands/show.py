"""
Show command - Display detailed host information
"""
from rich import print
from rich.panel import Panel
from rich.text import Text
from rich.console import Group
from ..database import load_database, get_database_path

def show_hosts():
    """Show detailed information about all hosts"""
    database = load_database()
    
    print(f"[dim]Database: {get_database_path()}[/dim]")
    
    if not database:
        print("[yellow]No hosts saved yet.[/yellow]")
        print("Use 'divein add' to add your first host.")
        return
    
    # Sort by ID
    for host_id in sorted(database.keys()):
        data = database[host_id]
        
        nickname = data.get("nickname", "")
        username = data["username"]
        host = data["host"]
        port = data["port"]
        ssh_key = data.get("ssh_key", "")
        handshake = data.get("handshake", "")
        password = data.get("password")
        encrypted = data.get("encrypted_password")
        
        # Build Content
        content_lines = []
        content_lines.append(f"[bold]Connection:[/bold] {username}@{host}:{port}")
        
        # Auth info
        if ssh_key:
            auth_info = f"[yellow]SSH Key:[/yellow] {ssh_key}"
        elif encrypted:
            auth_info = "[green]Encrypted Password[/green] (Protected by Master Password)"
        elif password:
             auth_info = f"[red]Plaintext Password:[/red] {password}"
        else:
             auth_info = "[dim]None[/dim]"
        content_lines.append(f"[bold]Authentication:[/bold] {auth_info}")
        
        if handshake:
             content_lines.append(f"[bold]Handshake:[/bold] {handshake}")
             
        content_lines.append(f"\n[dim]Connect with:[/dim] [cyan]divein {host_id}[/cyan]")

        
        panel = Panel(
            "\n".join(content_lines),
            title=f"[bold white]ID: {host_id}[/bold white] {f'({nickname})' if nickname else ''}",
            border_style="blue",
            expand=False
        )
        print(panel)