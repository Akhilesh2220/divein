"""
Add command - Add new SSH hosts
"""
import typer
from rich import print
from ..database import load_database, save_database, get_next_id
from ..crypto import encrypt_password

def add_host():
    """Add a new host interactively"""
    print("\n[bold green]Add New SSH Host[/bold green]")
    print("=" * 40)
    
    # Get host details
    nickname = typer.prompt("Nickname", default="", show_default=False)
    username = typer.prompt("Username")
    host = typer.prompt("Host/IP")
    
    # SSH Key or Password (mutually exclusive)
    ssh_key = typer.prompt("SSH Key path (optional, press Enter for password auth)", default="", show_default=False)
    
    password = ""
    encrypted_data = None
    encryption_salt = None
    
    if ssh_key:
        # Using SSH key - no password needed
        print("[yellow]Using SSH key authentication[/yellow]")
    else:
        # Using password authentication
        password = typer.prompt("Password", hide_input=True)
        
        # Always Ask for Master Password to encrypt
        if password:
             print("[yellow]Encrypting password...[/yellow]")
             master_password = typer.prompt("Enter Master Password for encryption", hide_input=True)
             # Encrypt
             crypto_result = encrypt_password(password, master_password)
             encrypted_data = crypto_result["encrypted_data"]
             encryption_salt = crypto_result["salt"]
             password = "" # Clear plaintext
             print("[bold green]Password encrypted![/bold green]")
    
    # Optional fields with defaults
    port = typer.prompt("Port", default=22, type=int)
    handshake = typer.prompt("Handshake method", default="", show_default=False)
    
    # Load existing database
    database = load_database()
    
    # Get next available ID
    host_id = get_next_id(database)
    
    # Prepare host data
    host_data = {
        "nickname": nickname,
        "username": username,
        "host": host,
        "password": password,
        "encrypted_password": encrypted_data,
        "encryption_salt": encryption_salt,
        "port": port,
        "ssh_key": ssh_key,
        "handshake": handshake
    }
    
    # Save to database with numeric ID
    database[host_id] = host_data
    
    if save_database(database):
        display_name = f"{nickname}: {username}@{host}" if nickname else f"{username}@{host}"
        auth_type = "SSH Key" if ssh_key else ("Encrypted Password" if encrypted_data else "Password")
        print(f"[bold green]Host '{display_name}' added successfully![/bold green] (ID: {host_id}, Auth: {auth_type})")
        return True
    else:
        print("[bold red]Failed to save host![/bold red]")
        return False