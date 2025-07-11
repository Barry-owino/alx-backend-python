import sqlite3
import functools
from datetime import datetime

def log_queries(func):
    """
    Decorator that logs the SQL query before executing the decorated function.
    It assumes the SQL query is passed as the first positional argument or
    as a keyword argument named 'query'.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = None
        # Attempt to find the query string from positional arguments
        if args and isinstance(args[0], str):
            query = args[0]
        # Attempt to find the query string from keyword arguments
        elif 'query' in kwargs and isinstance(kwargs['query'], str):
            query = kwargs['query']

        if query:
            print(f"--- DATABASE QUERY LOG ---")
            print(f"Executing query: {query}")
            print(f"--------------------------")
        else:
            print("--- DATABASE QUERY LOG ---")
            print("Warning: No string-type 'query' argument found to log.")
            print("--------------------------")

        return func(*args, **kwargs)
    return wrapper

# --- Database Setup (for demonstration purposes) ---
# This part creates a dummy SQLite database and a 'users' table
# to make the example runnable.
try:
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')
    # Insert sample data, ignoring if already exists
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (1, 'John Doe', 'john@example.com')")
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (2, 'Jane Smith', 'jane@example.com')")
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (3, 'Peter Jones', 'peter@example.com')")
    conn.commit()
except sqlite3.Error as e:
    print(f"Database setup error: {e}")
finally:
    if conn:
        conn.close()

# --- Decorated Functions ---

@log_queries
def fetch_all_users(query):
    """
    Fetches all users from the database.
    The query is expected as the first positional argument.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except sqlite3.Error as e:
        print(f"Database query error: {e}")
        return []
    finally:
        conn.close()

@log_queries
def fetch_user_by_email(query_str, email_param):
    """
    Fetches a user by email.
    The query is expected as the first positional argument.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query_str, (email_param,))
        result = cursor.fetchone()
        return result
    except sqlite3.Error as e:
        print(f"Database query error: {e}")
        return None
    finally:
        conn.close()

@log_queries
def update_user_name(query, new_name, user_id):
    """
    Updates a user's name.
    The query is expected as a keyword argument.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, (new_name, user_id))
        conn.commit()
        print(f"User ID {user_id} name updated to {new_name}.")
        return cursor.rowcount
    except sqlite3.Error as e:
        print(f"Database update error: {e}")
        return 0
    finally:
        conn.close()

@log_queries
def example_function_without_query(arg1, arg2):
    """
    An example function that doesn't have a 'query' argument.
    The decorator will log a warning for this.
    """
    print(f"Inside example_function_without_query with args: {arg1}, {arg2}")
    return arg1 + arg2

# --- Demonstration of Usage ---

print("--- Fetching all users ---")
users = fetch_all_users("SELECT * FROM users")
print("Fetched Users:")
for user in users:
    print(user)

print("\n--- Fetching user by email ---")
jane_user = fetch_user_by_email("SELECT * FROM users WHERE email = ?", "jane@example.com")
print(f"Fetched Jane: {jane_user}")

print("\n--- Updating a user's name ---")
update_user_name(query="UPDATE users SET name = ? WHERE id = ?", new_name="Jonathan Doe", user_id=1)

print("\n--- Re-fetching updated user ---")
updated_john = fetch_user_by_email("SELECT * FROM users WHERE id = ?", 1)
print(f"Fetched updated user 1: {updated_john}")

print("\n--- Calling a function without a query argument ---")
result_no_query = example_function_without_query(100, 200)
print(f"Result from example_function_without_query: {result_no_query}")

