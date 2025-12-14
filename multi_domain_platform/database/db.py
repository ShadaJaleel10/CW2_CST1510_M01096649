import sqlite3
import hashlib
import os

DATABASE_PATH = "platform.db"

class SimpleHasher:
    @staticmethod
    def hash_password(plain: str) -> str:
        return hashlib.sha256(plain.encode("utf-8")).hexdigest()

def initialize_database():
    """Connects to the database and creates all necessary tables and demo data."""

    full_path = os.path.join(os.path.dirname(__file__), DATABASE_PATH)
    
    conn = sqlite3.connect(full_path)
    cur = conn.cursor()

    # 1. users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)
    #Demo User: username='alice', password='mypassword', role='admin'
    test_password_hash = SimpleHasher.hash_password("mypassword")
    cur.execute(
        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        ("alice", test_password_hash, "admin")
    )
    cur.execute(
        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        ("bob", SimpleHasher.hash_password("bobpass"), "user")
    )
    
    #security incidents table (cybersecurity)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS security_incidents (
            incident_id INTEGER PRIMARY KEY,
            incident_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            status TEXT NOT NULL,
            description TEXT
        )
    """)
    # Insert Demo Data
    cur.execute("INSERT OR IGNORE INTO security_incidents VALUES (1, 'DDoS', 'critical', 'Open', 'Sustained attack from multiple IPs targeting web service.')")
    cur.execute("INSERT OR IGNORE INTO security_incidents VALUES (2, 'Phishing', 'medium', 'Closed', 'Employee reported suspicious email; contained to one mailbox.')")
    cur.execute("INSERT OR IGNORE INTO security_incidents VALUES (3, 'Malware', 'high', 'Investigating', 'Ransomware detected on the internal file server.')")
    
    # 3. Dataset Table (Data Science)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS datasets (
            dataset_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            size_bytes INTEGER NOT NULL,
            rows INTEGER NOT NULL,
            source TEXT
        )
    """)
    # Insert Demo Data
    cur.execute("INSERT OR IGNORE INTO datasets VALUES (101, 'Financial Transactions 2024', 5368709120, 15000000, 'ERP System')") # 5GB
    cur.execute("INSERT OR IGNORE INTO datasets VALUES (102, 'Customer Survey Q3', 104857600, 5000, 'Marketing API')") # 100MB
    
    # 4. IT tickets Table (IT Operations)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets (
            ticket_id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL,
            assigned_to TEXT
        )
    """)
    # Insert Demo Data
    cur.execute("INSERT OR IGNORE INTO it_tickets VALUES (501, 'Password Reset Failed', 'high', 'Open', 'Jane Doe')")
    cur.execute("INSERT OR IGNORE INTO it_tickets VALUES (502, 'New Monitor Request', 'low', 'In Progress', 'John Smith')")
    cur.execute("INSERT OR IGNORE INTO it_tickets VALUES (503, 'VPN Connection Intermittent', 'critical', 'Open', 'Jane Doe')")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_database()
    print(f"Database setup complete. File created/updated at: {os.path.join(os.path.dirname(__file__), DATABASE_PATH)}")