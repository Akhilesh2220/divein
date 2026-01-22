"""
List command - Show all saved hosts with interactive connection
"""
import typer
from rich import print
from rich.table import Table
from ..database import load_database
from ..utils import connect_host
from .delete import delete_host

def print_table():
    """Helper to print the hosts table"""
    database = load_database()
    
    if not database:
        print("[yellow]No hosts saved yet.[/yellow]")
        print("Use 'divein add' to add your first host.")
        return False
    
    table = Table(title="Saved Hosts")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Nickname", style="magenta")
    table.add_column("User@Host:Port", style="green")
    
    # Sort by ID
    for host_id in sorted(database.keys()):
        data = database[host_id]
        username = data["username"]
        host = data["host"]
        port = data["port"]
        nickname = data.get("nickname", "")
        
        connection_str = f"{username}@{host}:{port}"
        
        table.add_row(str(host_id), nickname, connection_str)
    
    print(table)
    return True

def list_hosts():
    """List all saved hosts with interactive connection"""
    import click
    import sys
    
    # Interactive connection loop
    while True:
        has_hosts = print_table()
        if not has_hosts:
            break
            
        sys.stdout.write("\nConnect (ID/Nickname), Delete ('rm <ID>'), or 'q' to exit: ")
        sys.stdout.flush()
        
        cmd_buffer = []
        should_break = False
        
        while True:
            char = click.getchar()
            
            # Hotkey: 'q' to exit immediately if buffer is empty
            if (char == 'q' or char == 'Q') and not cmd_buffer:
                print("\n")
                should_break = True
                break
                
            # Hotkeys for digits? No, strictly requested 'q'. 
            # Numbers like '1' require enter because '10' exists.
            
            # Handle Enter
            if char == '\r' or char == '\n':
                print("\n")
                break
            
            # Handle Backspace
            if char == '\x7f':
                if cmd_buffer:
                    cmd_buffer.pop()
                    sys.stdout.write('\b \b')
                    sys.stdout.flush()
            # Handle printable
            elif char.isprintable():
                cmd_buffer.append(char)
                sys.stdout.write(char)
                sys.stdout.flush()
        
        if should_break:
            break
            
        choice = "".join(cmd_buffer).strip()
        
        if not choice:
            continue
            
        if choice.lower() in ['exit', 'quit']:
            break

        try:
            # Handle Deletion
            if choice.startswith("rm ") or choice.startswith("delete ") or choice.startswith("del "):
                try:
                    target = choice.split(" ", 1)[1]
                    if delete_host(target):
                        # Refresh table by looping again
                        print("\n")
                        continue
                except IndexError:
                    print("[red]Please specify an ID to delete (e.g., 'rm 1')[/red]")
                    continue

            # Try to connect
            if connect_host(choice):
                break
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"[bold red]Error: {e}[bold red]")