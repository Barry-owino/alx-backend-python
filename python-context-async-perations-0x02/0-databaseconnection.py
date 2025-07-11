import sqlite3

# --- Class-based Context Manager for Database Connection ---
class DatabaseConnection:
    """
    A class-based context manager to handle opening and closing SQLite database connections automatically.
    """
    def __init__(self, db_name='users.db'):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """
        Called when entering the 'with' statement block.
        Opens the database connection and returns it.
        """
        print(f"--- Context Manager: Opening connection to {self.db_name} ---")
        self.conn = sqlite3.connect(self.db_name)
        # By default, SQLite connections are in autocommit mode.
        # For explicit transaction control within a context, you might set isolation_level=None
        # but for simple queries, the default is fine.
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Called when exiting the 'with' statement block.
        Closes the database connection. Handles exceptions if they occur within the block.
        """
        if self.conn:
            self.conn.close()
            print(f"--- Context Manager: Closing connection to {self.db_name} ---")
        
        # If an exception occurred within the 'with' block, exc_type, exc_val, exc_tb will be non-None.
        # Returning False here would re-raise the exception after __exit__ completes.
        # Returning True would suppress the exception.
        # For general database operations, it's usually better to let exceptions propagate.
        if exc_type:
            print(f"--- Context Manager: An exception occurred: {exc_type.__name__}: {exc_val} ---")
            return False # Re-raise the exception
        return True # Indicate that no exception occurred or it was handled (if returning True)


# --- Database Setup (for demonstration purposes) ---
# This part creates a dummy SQLite database and a 'users' table
# to make the example runnable.
def setup_database(db_name='users.db'):
    try:
        conn_setup = sqlite3.connect(db_name)
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

# Run the database setup once
setup_database()

# --- Demonstration of Usage with the Context Manager ---

print("--- Demonstrating DatabaseConnection Context Manager for SELECT ---")
# Use the context manager with the 'with' statement
try:
    with DatabaseConnection('users.db') as conn:
        # 'conn' here is the database connection object returned by __enter__
        cursor = conn.cursor()
        print("Executing query within context manager: SELECT * FROM users")
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print("Results from query:")
        for row in results:
            print(row)
except Exception as e:
    print(f"An error occurred while using the context manager: {e}")

print("\n--- Demonstrating DatabaseConnection Context Manager with an INSERT ---")
try:
    with DatabaseConnection('users.db') as conn:
        cursor = conn.cursor()
        new_user_email = "new_user@example.com"
        print(f"Attempting to insert a new user: {new_user_email}")
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("New User", new_user_email))
        conn.commit() # Commit changes explicitly for INSERT/UPDATE/DELETE
        print(f"User '{new_user_email}' inserted successfully.")
except sqlite3.IntegrityError:
    print(f"User '{new_user_email}' already exists (email must be unique).")
except Exception as e:
    print(f"An error occurred during INSERT: {e}")

print("\n--- Verifying the new user (if inserted) ---")
try:
    with DatabaseConnection('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", ("new_user@example.com",))
        new_user = cursor.fetchone()
        if new_user:
            print(f"Verified new user: {new_user}")
        else:
            print("New user not found (might have already existed or failed to insert).")
except Exception as e:
    print(f"An error occurred during verification: {e}")


print("\n--- Demonstrating DatabaseConnection Context Manager with a simulated error ---")
try:
    with DatabaseConnection('users.db') as conn:
        cursor = conn.cursor()
        print("Executing a faulty query within context manager to simulate error:")
        cursor.execute("SELECT * FROM non_existent_table") # This will cause an error
        results = cursor.fetchall()
        print("Results (should not be reached if error occurs):", results)
except Exception as e:
    print(f"Caught expected error from context manager usage: {e}")


