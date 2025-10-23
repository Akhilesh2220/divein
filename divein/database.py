"""
Database operations for storing hosts
"""
import json
import os
from pathlib import Path

# Database location
DB_DIR = Path.home() / ".divein"
DB_FILE = DB_DIR / "database.json"

def ensure_db_dir():
    """Create database directory if it doesn't exist"""
    DB_DIR.mkdir(exist_ok=True)

def load_database():
    """Load hosts from JSON database file"""
    ensure_db_dir()
    
    if DB_FILE.exists():
        try:
            with open(DB_FILE, 'r') as f:
                data = json.load(f)
                # Convert keys to integers for proper sorting
                return {int(k): v for k, v in data.items()}
        except Exception as e:
            print(f"❌ Error loading database: {e}")
            return {}
    return {}

def save_database(data):
    """Save hosts to JSON database file"""
    try:
        ensure_db_dir()
        with open(DB_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"❌ Error saving database: {e}")
        return False

def get_next_id(database):
    """Get the next available ID"""
    if not database:
        return 1
    return max(database.keys()) + 1

def get_database_path():
    """Return the path to the database file"""
    return str(DB_FILE)