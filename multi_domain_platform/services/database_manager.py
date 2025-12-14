import sqlite3
from typing import Any, Iterable, Optional 
import os 

class DatabaseManager:
    """Handles SQLite database connections and queries."""

    def __init__(self, db_path: str):
        self._db_path= db_path

    def connect(self) -> sqlite3.Connection:
        """Establishes and returns a new database connection."""
        conn = sqlite3.connect(self._db_path, check_same_thread=False)
        conn.row_factory= sqlite3.Row
        return conn

    def close(self, conn: sqlite3.Connection) -> None:
        """Closes the provided connection."""
        conn.close()

    def execute_query(self, sql: str, params: Iterable[Any]= ()) -> sqlite3.Cursor:
        """Execute a write query (INSERT, UPDATE, DELETE)."""
        conn = self.connect() 
        try:
            cur= conn.cursor()
            cur.execute(sql, tuple(params))
            conn.commit()
            return cur
        finally:
            self.close(conn)

    def fetch_one(self, sql: str, params: Iterable[Any]= ()) -> Optional[sqlite3.Row]:
        """Execute a read query that expects a single row."""
        conn= self.connect()
        try:
            cur= conn.cursor()
            cur.execute(sql, tuple(params))
            return cur.fetchone()
        finally:
            self.close(conn)

    def fetch_all(self, sql: str, params: Iterable[Any]= ()) -> list[sqlite3.Row]:
        """Execute a read query that expects multiple rows."""
        conn= self.connect()
        try:
            cur= conn.cursor()
            cur.execute(sql, tuple(params))
            return cur.fetchall()
        finally:
            self.close(conn)