import bcrypt
from app.data.db import connect_database, DATA_DIR
from app.data.users import get_user_by_username, insert_user

def register_user(username, password, role='user'):
    """Register new user with password hashing[cite: 201, 202]."""
    # ... (Implementation provided in your document [cite: 337, 338, 339, 340])
    # Use the implementation from the document for a complete example.
    # It first checks if the user exists, then hashes the password, then inserts.
    # Note: If you use the provided document's implementation in your notebook, 
    # you can just call the functions from the imported app.data modules.
    conn = connect_database()
    cursor = conn.cursor()
    
    # Check if user already exists [cite: 338]
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False, f"Username '{username}' already exists."
    
    # Hash the password [cite: 203, 339]
    password_hash = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')
    conn.close() # Close the connection used for the check

    # Insert into database using the function in app.data.users [cite: 208]
    insert_user(username, password_hash, role)
    return True, f"User '{username}' registered successfully."


def login_user(username, password):
    """Authenticate user[cite: 211]."""
    user = get_user_by_username(username) # Uses the data layer function [cite: 212]
    
    if not user:
        return False, "User not found." 
    
    # Verify password (user[2] is password_hash column) [cite: 214, 215, 343]
    stored_hash = user[2]
    
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')): 
        return True, f"Login successful!" 
    
    return False, "Incorrect password." 

# Migration function uses the complete example from the document [cite: 332]
def migrate_users_from_file(conn, filepath=DATA_DIR / "users.txt"):
    """
    Migrate users from users.txt to the database.
    (Implementation is copied directly from your document's complete example for completeness)
    """
    if not filepath.exists():
        print(f"File not found: {filepath}")
        print(" No users to migrate.")
        return 0

    cursor = conn.cursor()
    migrated_count = 0
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split(',')
            
            # This is simplified from the document's logic to handle both 2 and 3 parts
            if len(parts) >= 2:
                username = parts[0]
                password_hash = parts[1]
                role = parts[2] if len(parts) > 2 else 'user' # Fallback to 'user' if role isn't present [cite: 334]
            else:
                continue

            try:
                # INSERT OR IGNORE prevents inserting a user that already exists [cite: 334]
                cursor.execute(
                    "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                    (username, password_hash, role)
                )
                
                if cursor.rowcount > 0:
                    migrated_count += 1
            except sqlite3.Error as e:
                print(f"Error migrating user {username}: {e}")
                
    conn.commit()
    print(f"Migrated {migrated_count} users from {filepath.name}")
    return migrated_count

