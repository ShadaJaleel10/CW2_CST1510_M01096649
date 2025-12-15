import pandas as pd
import sqlite3
from app.data.db import connect_database, DB_PATH
from app.data.schema import create_all_tables
from app.services.user_service import register_user, login_user, migrate_users_from_file
from app.data.incidents import (
    insert_incident, 
    get_all_incidents, 
    update_incident_status, 
    delete_incident, 
    get_incidents_by_type_count
) 
from app.data.datasets import (
    load_all_csv_data,
    get_datasets_by_category,
    get_tickets_by_priority
)

def setup_database_complete():
    """Complete database setup: Connect, Create tables, Migrate users, Load CSV data."""
    print("\n" + "="*60)
    print("STARTING COMPLETE DATABASE SETUP")
    print("="*60)
    
    #Connect
    print("\n[1/5] Connecting to database...")
    conn = connect_database()
    print(" Connected")
    
    #create tables
    print("\n[2/5] Creating database tables...")
    create_all_tables(conn)
    
    #Migration
    print("\n[3/5] Migrating users from users.txt...")
    user_count = migrate_users_from_file(conn)
    print(f" Migrated {user_count} users")
    
    #CSV data
    print("\n[4/5] Loading CSV data...")
    total_rows = load_all_csv_data(conn)
    
    print("\n[5/5] Verifying database setup...")
    cursor = conn.cursor()
    tables = ['users', 'cyber_incidents', 'datasets_metadata', 'it_tickets']
    print("\n  Database Summary:")
    print(f"{'Table':<25} {'Row Count':<15}")
    print("-" * 40)
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table:<25} {count:<15}")

    conn.close()
    print("\n" + "="*60)
    print(" DATABASE SETUP COMPLETE!")
    print("="*60)
    print(f"\n  Database location: {DB_PATH.resolve()}")
    

def main():
    """Demonstrate all functionality: Auth, Full CRUD, and Analytical Reports."""
    setup_database_complete() 

    conn = connect_database()
    print("\n" + "=" * 60)
    print("Week 8: CRUD & Authentication Demo")
    print("=" * 60)
    
    success, msg = register_user("alice", "SecurePass123!", "analyst")
    print(f"Register: {msg}")
    success, msg = login_user("alice", "SecurePass123!")
    print(f"Login: {msg}")
    
    incident_id = insert_incident(
        conn,
        "2024-11-05",
        "Phishing",
        "High",
        "Open",
        "Suspicious email detected - Demo",
        "alice"
    )
    print(f"Created incident #{incident_id}")

    #read
    df_all = get_all_incidents(conn)
    print(f"Total incidents: {len(df_all)}")
    
    #update
    rows_updated = update_incident_status(conn, incident_id, "Resolved")
    print(f"Updated incident #{incident_id} status to Resolved. Rows affected: {rows_updated}")
    
    #delete
    rows_deleted = delete_incident(conn, incident_id)
    print(f"Deleted incident #{incident_id}. Rows affected: {rows_deleted}")
    
    df_after_delete = get_all_incidents(conn)
    print(f"Total incidents after deletion: {len(df_after_delete)}")

    print("\n" + "="*60)
    print("WEEK 8: ANALYTICAL REPORTS")
    print("="*60)

    #Cyber Incidents 
    df_by_type = get_incidents_by_type_count(conn)
    print("\n[Report 1] Cyber Incidents by Type:")
    print(df_by_type)

    #Datasets Metadata
    df_datasets = get_datasets_by_category(conn)
    print("\n[Report 2] Datasets by Category (Count and Avg Size):")
    print(df_datasets)
    
    #IT Tickets
    df_tickets = get_tickets_by_priority(conn)
    print("\n[Report 3] IT Tickets by Priority and Status:")
    print(df_tickets)

    conn.close()

if __name__ == "__main__":
    main()