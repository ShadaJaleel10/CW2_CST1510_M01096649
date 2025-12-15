import sqlite3
from pathlib import Path
import os
import inspect
#directory path
CURRENT_DIR = Path(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
ROOT_DIR = CURRENT_DIR.parent.parent 
DATA_DIR = ROOT_DIR / "DATA"

DB_PATH = DATA_DIR / "intelligence_platform.db"

def connect_database(db_path=DB_PATH):
    """
    Connect to the SQLite database.
    """
    # Create DATA folder
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"DEBUG: Data Directory resolved to: {DATA_DIR.resolve()}")
    
    conn = sqlite3.connect(str(db_path))
    return conn
