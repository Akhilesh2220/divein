"""
Main CLI entry point
"""
import sys
from .commands.add import add_host
from .commands.delete import delete_host
from .commands.list import list_hosts
from .commands.show import show_hosts  # ← Add this import
from .utils import connect_host

def show_help():
    """Show help message"""
    print("""
DiveIn - SSH Connection Manager

Usage:
  divein add                    - Add a new host interactively
  divein delete <identifier>    - Delete a host by ID or nickname
  divein <identifier>           - Connect to a host directly
  divein list                   - List all saved hosts (brief)
  divein show                   - Show detailed host information
  divein help                   - Show this help message

Examples:
  divein add                    # Add new host
  divein delete 1              # Delete host by ID
  divein delete myserver       # Delete host by nickname
  divein 1                     # Connect to host by ID
  divein myserver              # Connect to host by nickname
  divein user@192.168.1.1      # Connect by connection string
  divein list                  # Show brief host list
  divein show                  # Show detailed host information
    """)

def main():
    """Main CLI entry point"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1]
    
    if command == "add":
        add_host()
    elif command == "delete":
        if len(sys.argv) < 3:
            print("❌ Usage: divein delete <ID or nickname>")
        else:
            delete_host(sys.argv[2])
    elif command == "list":
        list_hosts()
    elif command == "show":  # ← Add this condition
        show_hosts()
    elif command == "help":
        show_help()
    else:
        # Assume it's a connect command
        connect_host(command)

if __name__ == "__main__":
    main()