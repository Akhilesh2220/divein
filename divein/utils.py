"""
Utility functions
"""
import subprocess
from .database import load_database

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
        print(f"❌ Host '{identifier}' not found!")
        return False
    
    # Prepare SSH command
    username = host_data["username"]
    host = host_data["host"]
    port = host_data["port"]
    password = host_data["password"]
    ssh_key = host_data["ssh_key"]
    
    ssh_command = ["ssh"]
    
    # Add SSH key if provided (MUTUALLY EXCLUSIVE with password)
    if ssh_key:
        ssh_command.extend(["-i", ssh_key])
        # Don't use password when SSH key is provided
        auth_type = "SSH Key"
    else:
        # Using password authentication
        auth_type = "Password"
    
    # Add port
    ssh_command.extend(["-p", str(port)])
    
    # Add connection string
    ssh_command.append(f"{username}@{host}")
    
    nickname = host_data.get("nickname", "")
    display_name = f"{nickname}: {username}@{host}" if nickname else f"{username}@{host}"
    
    print(f"🔗 Connecting to {display_name} (ID: {host_id}, Auth: {auth_type})...")
    
    # Actually execute SSH command
    try:
        subprocess.run(ssh_command)
        return True
    except KeyboardInterrupt:
        print("\n👋 Connection closed.")
        return True
    except Exception as e:
        print(f"❌ SSH connection failed: {e}")
        return False