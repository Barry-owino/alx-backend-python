import sqlite3
import functools

def with_db_connection(func):
    """
    Decorator that opens a database connection, passes it to the decorated function,
    and ensures the connection is closed afterward, even if errors occur.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect('users.db')
            # Pass the connection as the first argument to the decorated function
            result = func(conn, *args, **kwargs)
            return result
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            # Optionally re-raise the exception if you want it to propagate
            raise
        finally:
            if conn:
                conn.close()
                # print("Database connection closed.") # For debugging/logging
    return wrapper

# --- Database Setup (for demonstration purposes) ---
# This part creates a dummy SQLite database and a 'users' table
# to make the example runnable.
try:
    conn_setup = sqlite3.connect('users.db')
    cursor_setup = conn_setup.cursor()
    cursor_setup.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')
    # Insert sample data, ignoring if already exists
    cursor_setup.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (1, 'John Doe', 'john@example.com')")
    cursor_setup.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (2, 'Jane Smith', 'jane@example.com')")
    cursor_setup.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (3, 'Peter Jones', 'peter@example.com')")
    conn_setup.commit()
except sqlite3.Error as e:
    print(f"Database setup error: {e}")
finally:
    if conn_setup:
        conn_setup.close()

# --- Decorated Function ---

@with_db_connection
def get_user_by_id(conn, user_id):
    """
    Fetches a user from the database by their ID using the provided connection.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# --- Demonstration of Usage ---

print("--- Fetching user by ID with automatic connection handling ---")
user = get_user_by_id(user_id=1)
print(f"Fetched User by ID 1: {user}")

print("\n--- Fetching another user by ID ---")
user2 = get_user_by_id(user_id=2)
print(f"Fetched User by ID 2: {user2}")

print("\n--- Attempting to fetch a non-existent user ---")
user_non_existent = get_user_by_id(user_id=99)
print(f"Fetched User by ID 99: {user_non_existent}")

