"""
Delete command - Remove SSH hosts
"""
from ..database import load_database, save_database

def delete_host(identifier):
    """Delete a host by ID or nickname"""
    database = load_database()
    
    # Try to delete by numeric ID first
    if identifier.isdigit():
        host_id = int(identifier)
        if host_id in database:
            host_data = database[host_id]
            nickname = host_data.get("nickname", "")
            username = host_data["username"]
            host = host_data["host"]
            display_name = f"{nickname}: {username}@{host}" if nickname else f"{host}@{username}"
            
            del database[host_id]
            if save_database(database):
                print(f"✅ Host '{display_name}' (ID: {host_id}) deleted successfully!")
                return True
            else:
                print("❌ Failed to delete host!")
                return False
        else:
            print(f"❌ Host ID '{identifier}' not found!")
            return False
    else:
        # Try to delete by nickname
        for host_id, data in database.items():
            if data.get("nickname") == identifier:
                display_name = f"{identifier}: {data['username']}@{data['host']}"
                del database[host_id]
                if save_database(database):
                    print(f"✅ Host '{display_name}' (ID: {host_id}) deleted successfully!")
                    return True
                else:
                    print("❌ Failed to delete host!")
                    return False
        
        print(f"❌ Host '{identifier}' not found!")
        return False