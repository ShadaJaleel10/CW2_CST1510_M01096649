import pandas as pd
from app.data.db import DATA_DIR
import sqlite3

def load_csv_to_table(conn, csv_filename, table_name):
    """Load a CSV file into a database table using pandas."""
    csv_path = DATA_DIR / csv_filename
    
    if not csv_path.exists():
        print(f"CSV File not found: {csv_path}")
        return 0

    try:
        #read CSV file
        df = pd.read_csv(csv_path)

        #insert data
        rows_loaded = df.to_sql(
            name=table_name, 
            con=conn, 
            if_exists='append', 
            index=False
        )
        
        if rows_loaded > 0:
             print(f"Loaded {rows_loaded} rows from {csv_filename} into {table_name}.")
        else:
             print(f"No rows loaded from {csv_filename} (file may be empty or headers are incorrect).")
        return rows_loaded
    except pd.errors.EmptyDataError:
        print(f"Error loading {csv_filename} to {table_name}: No columns to parse from file (Empty File)")
        return 0
    except Exception as e:
        print(f"Error loading {csv_filename} to {table_name}: {e}")
        return 0

def load_all_csv_data(conn):
    """Loads all three domain CSVs into their respective tables."""
    total_rows = 0
    total_rows += load_csv_to_table(conn, "cyber_incidents.csv", "cyber_incidents")
    total_rows += load_csv_to_table(conn, "datasets_metadata.csv", "datasets_metadata")
    total_rows += load_csv_to_table(conn, "it_tickets.csv", "it_tickets")
    return total_rows

# --- ANALYTICAL QUERIES (Report 2 and 3) ---

def get_datasets_by_category(conn):
    """Analytical Query 2: Count and average size of datasets grouped by category."""
    query = """
    SELECT category, COUNT(*) as count, AVG(file_size_mb) as avg_size_mb
    FROM datasets_metadata
    GROUP BY category
    ORDER BY count DESC
    """
    return pd.read_sql_query(query, conn)

def get_tickets_by_priority(conn):
    """Analytical Query 3: Count of IT tickets grouped by priority and status."""
    query = """
    SELECT priority, status, COUNT(*) as count
    FROM it_tickets
    GROUP BY priority, status
    ORDER BY CASE priority
        WHEN 'Critical' THEN 1
        WHEN 'High' THEN 2
        WHEN 'Medium' THEN 3
        WHEN 'Low' THEN 4
        ELSE 5 END, status
    """
    return pd.read_sql_query(query, conn)