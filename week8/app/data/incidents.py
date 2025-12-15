import pandas as pd
from app.data.db import connect_database
import sqlite3

def insert_incident(conn, date, incident_type, severity, status, description, reported_by=None):
    """Insert a new cyber incident (Create)."""
    cursor = conn.cursor()
    query = """
    INSERT INTO cyber_incidents 
    (date, incident_type, severity, status, description, reported_by)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, (date, incident_type, severity, status, description, reported_by))
    conn.commit()
    return cursor.lastrowid

def get_all_incidents(conn):
    """Retrieve all incidents (Read)."""
    df = pd.read_sql_query("SELECT * FROM cyber_incidents ORDER BY id DESC", conn)
    return df

def update_incident_status(conn, incident_id, new_status):
    """Update the status of an incident (Update)."""
    cursor = conn.cursor()
    #update statement
    query = "UPDATE cyber_incidents SET status = ? WHERE id = ?"
    cursor.execute(query, (new_status, incident_id))
    conn.commit()
    return cursor.rowcount

def delete_incident(conn, incident_id):
    """Delete an incident from the database (Delete)."""
    cursor = conn.cursor()
    #delete statement
    query = "DELETE FROM cyber_incidents WHERE id = ?"
    cursor.execute(query, (incident_id,))
    conn.commit()
    return cursor.rowcount

def get_incidents_by_type_count(conn):
    """Analytical Query 1: Count incidents by type."""
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df