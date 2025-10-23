"""
Show command - Display detailed host information
"""
from ..database import load_database, get_database_path

def show_hosts():
    """Show detailed information about all hosts"""
    database = load_database()
    
    print(f"📁 Database: {get_database_path()}")
    print("=" * 60)
    
    if not database:
        print("📭 No hosts saved yet.")
        print("Use 'divein add' to add your first host.")
        return
    
    print("\n🔍 Detailed Host Information")
    print("=" * 60)
    
    # Sort by ID
    for host_id in sorted(database.keys()):
        data = database[host_id]
        show_host_details(host_id, data)
        print("-" * 60)

def show_host_details(host_id, data):
    """Display detailed information for a single host"""
    nickname = data.get("nickname", "")
    username = data["username"]
    host = data["host"]
    password = data["password"]
    port = data["port"]
    ssh_key = data.get("ssh_key", "")
    handshake = data.get("handshake", "")
    
    # Display header
    if nickname:
        print(f"🆔 ID: {host_id} | {nickname}")
        print(f"🔗 Connection: {username}@{host}:{port}")
    else:
        print(f"🆔 ID: {host_id} | {username}@{host}:{port}")
    
    # Authentication details
    if ssh_key:
        print(f"🔑 Authentication: SSH Key")
        print(f"   Key Path: {ssh_key}")
    else:
        print(f"🔑 Authentication: Password")
        if password:
            print(f"   Password: {password}")
        else:
            print(f"   Password: (not set)")
    
    # Additional details
    print(f"🌐 Port: {port}")
    
    if handshake:
        print(f"🤝 Handshake: {handshake}")
    else:
        print(f"🤝 Handshake: (default)")
    
    # Connection commands
    print(f"💻 Connect using:")
    print(f"   divein {host_id}")
    if nickname:
        print(f"   divein {nickname}")
    print(f"   divein {username}@{host}")