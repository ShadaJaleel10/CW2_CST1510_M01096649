import sqlite3

conn = sqlite3.connect("database/platform.db")
cur = conn.cursor()

# Create users table
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

# Create security_incidents table
cur.execute("""
CREATE TABLE IF NOT EXISTS security_incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    status TEXT NOT NULL,
    description TEXT
)
""")

conn.commit()
conn.close()

print("Schema created: database/platform.db")

