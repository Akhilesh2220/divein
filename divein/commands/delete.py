"""
Delete command - Remove SSH hosts
"""
import typer
from rich import print
from ..database import load_database, save_database

def parse_identifiers(identifier_str: str, database: dict) -> set:
    """
    Parse a string containing IDs, ranges (x-y), and nicknames.
    Returns a set of Host IDs (integers) to delete.
    """
    targets = set()
    parts = [p.strip() for p in identifier_str.split(",")]
    
    for part in parts:
        if not part:
            continue
            
        # Check for Range (e.g., 4-7)
        if "-" in part and part.replace("-", "").isdigit():
            try:
                start, end = map(int, part.split("-"))
                if start > end:
                    start, end = end, start
                # Add all IDs in range that exist
                for i in range(start, end + 1):
                    if i in database:
                        targets.add(i)
                continue
            except ValueError:
                pass # Fallback to normal processing if split failed
        
        # Check for ID
        if part.isdigit():
            hid = int(part)
            if hid in database:
                targets.add(hid)
            continue
            
        # Check for Nickname
        found_nick = False
        for hid, data in database.items():
            if data.get("nickname") == part:
                targets.add(hid)
                found_nick = True
        
        # If not found, ignore? or warn? 
        # For bulk ops, better to ignore invalid and process valid, 
        # but displaying a warning for typo is helpful.
    
    return targets

def reindex_database(database: dict) -> dict:
    """
    Re-assign IDs to be sequential starting from 1.
    Returns a new database dict.
    """
    new_db = {}
    # Sort by old ID to maintain relative order
    sorted_keys = sorted(database.keys())
    
    for new_id, old_id in enumerate(sorted_keys, 1):
        new_db[new_id] = database[old_id]
        
    return new_db

def delete_host(identifier_str: str):
    """
    Delete hosts by ID, nickname, list, or range.
    Examples: '1', 'snow', '1,2,3', '4-7'
    """
    database = load_database()
    
    targets = parse_identifiers(identifier_str, database)
    
    if not targets:
        print(f"[bold red]No matching hosts found for '{identifier_str}'[/bold red]")
        return False
    
    # Show confirmation summary
    print(f"\n[bold red]The following hosts will be DELETED:[/bold red]")
    print(f"[dim](IDs will be re-ordered afterwards)[/dim]")
    print("=" * 40)
    
    for hid in sorted(targets):
        data = database[hid]
        nickname = data.get("nickname", "")
        username = data["username"]
        host = data["host"]
        display = f"{nickname} ({username}@{host})" if nickname else f"{username}@{host}"
        print(f"  [bold]{hid}[/bold]: {display}")
        
    print("=" * 40)
    
    confirm = typer.confirm("Proceed with deletion?", default=False)
    
    if not confirm:
        print("[yellow]Deletion cancelled.[/yellow]")
        return False
        
    # Perform Deletion
    for hid in targets:
        del database[hid]
        
    # Re-index
    database = reindex_database(database)
    
    if save_database(database):
        print(f"[bold green]Successfully deleted {len(targets)} host(s) and re-indexed database![/bold green]")
        return True
    else:
        print("[bold red]Failed to save database![/bold red]")
        return False