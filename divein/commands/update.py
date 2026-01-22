"""
Update command - Edit existing SSH hosts
"""
import typer
from rich import print
from ..database import load_database, save_database
from ..crypto import encrypt_password

def update_host(identifier: str):
    """Update an existing host interactively"""
    database = load_database()
    
    # helper to find host id
    host_id = None
    if identifier.isdigit() and int(identifier) in database:
        host_id = int(identifier)
    else:
        for hid, data in database.items():
            if data.get("nickname") == identifier:
                host_id = hid
                break
    
    if not host_id:
        print(f"[bold red]Host '{identifier}' not found![/bold red]")
        return False
    
    current_data = database[host_id]
    print(f"\n[bold green]Updating Host {host_id}[/bold green] (Press Enter to keep current value)")
    print("=" * 50)
    
    # Update fields with defaults
    new_nickname = typer.prompt("Nickname", default=current_data.get("nickname", ""))
    new_username = typer.prompt("Username", default=current_data.get("username", ""))
    new_host = typer.prompt("Host/IP", default=current_data.get("host", ""))
    new_port = typer.prompt("Port", default=current_data.get("port", 22), type=int)
    
    # Auth update logic
    current_ssh_key = current_data.get("ssh_key", "")
    new_ssh_key = typer.prompt("SSH Key path", default=current_ssh_key, show_default=True)
    
    new_password = ""
    new_encrypted_data = current_data.get("encrypted_password")
    new_encryption_salt = current_data.get("encryption_salt")
    
    if new_ssh_key:
        print("[yellow]Using SSH key authentication[/yellow]")
        # Clear passwords if switching to key
        if new_ssh_key != current_ssh_key:
             new_encrypted_data = None
             new_encryption_salt = None
    else:
        # Password auth
        # We only prompt for password if they want to CHANGE it or if it was empty/key-based before
        has_existing_pass = (new_encrypted_data is not None)
        prompt_text = "New Password (leave empty to keep existing)" if has_existing_pass else "Password"
        
        pass_input = typer.prompt(prompt_text, hide_input=True, default="", show_default=False)
        
        if pass_input:
             # User entered a new password
             print("[yellow]Encrypting new password...[/yellow]")
             master_password = typer.prompt("Enter Master Password for encryption", hide_input=True)
             crypto_result = encrypt_password(pass_input, master_password)
             new_encrypted_data = crypto_result["encrypted_data"]
             new_encryption_salt = crypto_result["salt"]
             print("[bold green]Password updated and encrypted![/bold green]")
        elif not has_existing_pass:
             # No existing pass and no new pass?
             print("[red]Warning: No password or SSH key provided.[/red]")
    
    new_handshake = typer.prompt("Handshake method", default=current_data.get("handshake", ""))
    
    # Construct update
    updated_host = {
        "nickname": new_nickname,
        "username": new_username,
        "host": new_host,
        "port": new_port,
        "password": "", # Always empty
        "encrypted_password": new_encrypted_data,
        "encryption_salt": new_encryption_salt,
        "ssh_key": new_ssh_key,
        "handshake": new_handshake
    }
    
    database[host_id] = updated_host
    
    if save_database(database):
        print(f"[bold green]Host '{new_nickname or host_id}' updated successfully![/bold green]")
        return True
    else:
        print("[bold red]Failed to save host![/bold red]")
        return False
