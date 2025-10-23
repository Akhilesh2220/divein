"""
List command - Show all saved hosts with interactive connection
"""
from ..database import load_database, get_database_path
from ..utils import connect_host

def list_hosts():
    """List all saved hosts with interactive connection"""
    database = load_database()
    
    if not database:
        print("No hosts saved yet.")
        print("Use 'divein add' to add your first host.")
        return
    
    print("\nSaved Hosts")
    print("=" * 40)
    
    # Sort by ID
    for host_id in sorted(database.keys()):
        data = database[host_id]
        username = data["username"]
        host = data["host"]
        nickname = data.get("nickname", "")
        
        # Create display name
        if nickname:
            display_name = f"{nickname}"
        else:
            display_name = f"{username}@{host}"
        
        print(f"{host_id}. {display_name}")
    
    print("\n" + "=" * 40)
    
    # Interactive connection loop
    while True:
        try:
            choice = input("\nConnect to: ").strip()
            
            if choice.lower() in ['exit', 'quit']:
                print("Exiting...")
                break
            
            if choice.lower() in ['back', '']:
                break
            
            # Try to connect
            connect_host(choice)
            # After connection closes, break out of the loop
            break
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")