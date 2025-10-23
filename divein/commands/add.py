"""
Add command - Add new SSH hosts
"""
from ..database import load_database, save_database, get_next_id

def add_host():
    """Add a new host interactively"""
    print("\n🚀 Add New SSH Host")
    print("=" * 40)
    
    # Get host details
    nickname = input("Nickname (optional): ").strip()
    username = input("Username: ").strip()
    host = input("Host/IP: ").strip()
    
    # SSH Key or Password (mutually exclusive)
    ssh_key = input("SSH Key path (optional, press Enter for password auth): ").strip()
    
    if ssh_key:
        # Using SSH key - no password needed
        password = ""
        print("🔑 Using SSH key authentication")
    else:
        # Using password authentication
        password = input("Password: ").strip()
    
    # Optional fields with defaults
    port_input = input("Port (default 22): ").strip()
    port = int(port_input) if port_input.isdigit() else 22
    
    handshake = input("Handshake method (optional): ").strip()
    
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
        "port": port,
        "ssh_key": ssh_key,
        "handshake": handshake
    }
    
    # Save to database with numeric ID
    database[host_id] = host_data
    
    if save_database(database):
        display_name = f"{nickname}: {username}@{host}" if nickname else f"{username}@{host}"
        auth_type = "SSH Key" if ssh_key else "Password"
        print(f"✅ Host '{display_name}' added successfully! (ID: {host_id}, Auth: {auth_type})")
        return True
    else:
        print("❌ Failed to save host!")
        return False