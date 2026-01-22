"""
Utility functions
"""
import subprocess
import shutil
import typer
from rich import print
from .database import load_database
from .crypto import decrypt_password

def connect_host(identifier):
    """Connect to a host using SSH by ID or nickname"""
    database = load_database()
    
    # Find the host
    host_data = None
    host_id = None
    
    # Try to find by numeric ID first
    if identifier.isdigit():
        host_id = int(identifier)
        if host_id in database:
            host_data = database[host_id]
    
    # If not found by ID, try by nickname
    if not host_data:
        for id_num, data in database.items():
            if data.get("nickname") == identifier:
                host_data = data
                host_id = id_num
                break
    
    # If still not found, try by connection string
    if not host_data:
        for id_num, data in database.items():
            if f"{data['username']}@{data['host']}" == identifier:
                host_data = data
                host_id = id_num
                break
    
    if not host_data:
        print(f"[bold red]Host '{identifier}' not found![/bold red]")
        return False
    
    # Prepare SSH command
    username = host_data["username"]
    host = host_data["host"]
    port = host_data["port"]
    password = host_data.get("password")
    encrypted_password = host_data.get("encrypted_password")
    encryption_salt = host_data.get("encryption_salt")
    ssh_key = host_data.get("ssh_key")
    
    ssh_command = ["ssh"]
    auth_type = "Password" 
    
    # Add SSH key if provided (MUTUALLY EXCLUSIVE with password)
    if ssh_key:
        ssh_command.extend(["-i", ssh_key])
        # Don't use password when SSH key is provided
        auth_type = "SSH Key"
    elif encrypted_password and encryption_salt:
        auth_type = "Encrypted Password"
        # Decrypt password
        try:
             print(f"[yellow]This host is encrypted.[/yellow]")
             master_password = typer.prompt("Enter Master Password", hide_input=True)
             password = decrypt_password(encrypted_password, encryption_salt, master_password)
             print("[green]Decrypted successfully![/green]")
        except Exception:
             print("[bold red]Failed to decrypt! Wrong master password?[/bold red]")
             return False

    elif password:
         auth_type = "Plain Password"
         # Warn user
         print("[red]Using insecure plaintext password[/red]")

    
    # Add port
    ssh_command.extend(["-p", str(port)])
    
    # Add connection string
    ssh_command.append(f"{username}@{host}")
    
    nickname = host_data.get("nickname", "")
    display_name = f"{nickname}: {username}@{host}" if nickname else f"{username}@{host}"
    
    display_name = f"{nickname}: {username}@{host}" if nickname else f"{username}@{host}"
    
    print(f"Connecting to [bold cyan]{display_name}[/bold cyan] (ID: {host_id}, Auth: {auth_type})...")

    # If we have a password (either plain or decrypted), we use pexpect to automate the login.
    if (password) and not ssh_key:
        try:
            import pexpect
            import struct
            import fcntl
            import termios
            import sys
            
            # Spawn the ssh command
            # We join the arguments into a single string for spawn, or pass list. List is safer.
            # pexpect.spawn(command, args)
            child = pexpect.spawn("ssh", ssh_command[1:], encoding='utf-8')
            
            # Expect either a password prompt OR a fingerprint confirmation
            # We look for common patterns.
            index = child.expect([
                r"(?i)password:", 
                r"(?i)continue connecting \(yes/no\)?",
                pexpect.EOF,
                pexpect.TIMEOUT
            ], timeout=10)
            
            if index == 1:
                # Fingerprint confirmation
                print("[yellow]New host fingerprint detected. Accepting...[/yellow]")
                child.sendline("yes")
                # Wait for password prompt again
                index = child.expect([r"(?i)password:", pexpect.EOF, pexpect.TIMEOUT], timeout=10)
                
            if index == 0:
                # Password prompt detected
                print("[dim]Sending password...[/dim]")
                child.sendline(password)
            elif index == 2:
                print("[red]Connection closed unexpectedly.[/red]")
                print(child.before)
                return False
            elif index == 3:
                print("[red]Connection timed out waiting for prompt.[/red]")
                return False

            # If we successfully sent the password (or didn't need to?), hand over control
            # Resize the child window to match parent
            def get_terminal_size():
                s = struct.unpack('HH', fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ, '1234'))
                return s[0], s[1]
                
            try:
                rows, cols = get_terminal_size()
                child.setwinsize(rows, cols)
            except:
                pass

            # Hand over control to user
            child.interact()
            return True

        except ImportError:
            print("[red]Error: pexpect not found. Please reinstall divein.[/red]")
            return False
        except Exception as e:
            print(f"[bold red]SSH automation failed: {e}[/bold red]")
            return False

    # Fallback/Standard execution for SSH Key or if pexpect fails logic (though we return above)
    try:
        subprocess.run(ssh_command)
        return True
    except KeyboardInterrupt:
        print("\nConnection closed.")
        return True
    except Exception as e:
        print(f"[bold red]SSH connection failed: {e}[/bold red]")
        return False