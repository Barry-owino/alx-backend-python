import sqlite3

# --- Class-based Context Manager for Query Execution ---
class ExecuteQuery:
    """
    A class-based context manager that handles opening/closing a database connection,
    executes a specified query with parameters, and returns the results.
    """
    def __init__(self, db_name='users.db', query="", params=()):
        self.db_name = db_name
        self.query = query
        self.params = params
        self.conn = None
        self.results = None

    def __enter__(self):
        """
        Opens the database connection, executes the query, and stores the results.
        """
        print(f"--- ExecuteQuery Context Manager: Opening connection to {self.db_name} ---")
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        print(f"--- ExecuteQuery Context Manager: Executing query: '{self.query}' with params: {self.params} ---")
        cursor.execute(self.query, self.params)
        
        # For SELECT queries, fetch results. For DML, commit.
        if self.query.strip().upper().startswith("SELECT"):
            self.results = cursor.fetchall()
        else:
            self.conn.commit() # Commit changes for INSERT/UPDATE/DELETE
            self.results = cursor.rowcount # For DML, return rowcount
        return self.results # Return the query results

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Closes the database connection. Handles exceptions.
        """
        if self.conn:
            self.conn.close()
            print(f"--- ExecuteQuery Context Manager: Closing connection to {self.db_name} ---")
        
        if exc_type:
            # An exception occurred within the 'with' block
            print(f"--- ExecuteQuery Context Manager: An exception occurred: {exc_type.__name__}: {exc_val} ---")
            return False # Re-raise the exception
        return True # Indicate that no exception occurred or it was handled


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
                email TEXT UNIQUE NOT NULL,
                age INTEGER
            )
        ''')
        # Insert sample data, ignoring if already exists
        cursor_setup.execute("INSERT OR IGNORE INTO users (id, name, email, age) VALUES (1, 'John Doe', 'john@example.com', 30)")
        cursor_setup.execute("INSERT OR IGNORE INTO users (id, name, email, age) VALUES (2, 'Jane Smith', 'jane@example.com', 22)")
        cursor_setup.execute("INSERT OR IGNORE INTO users (id, name, email, age) VALUES (3, 'Peter Jones', 'peter@example.com', 45)")
        cursor_setup.execute("INSERT OR IGNORE INTO users (id, name, email, age) VALUES (4, 'Alice Brown', 'alice@example.com', 28)")
        conn_setup.commit()
    except sqlite3.Error as e:
        print(f"Database setup error: {e}")
    finally:
        if conn_setup:
            conn_setup.close()

# Run the database setup once
setup_database()

# --- Demonstration of Usage with ExecuteQuery Context Manager ---

print("--- Demonstrating ExecuteQuery Context Manager for SELECT ---")
try:
    query_to_execute = "SELECT * FROM users WHERE age > ?"
    param_value = 25
    with ExecuteQuery(query=query_to_execute, params=(param_value,)) as users_over_25:
        print(f"Users older than {param_value}:")
        if users_over_25:
            for user_row in users_over_25:
                print(user_row)
        else:
            print("No users found matching the criteria.")
except Exception as e:
    print(f"An error occurred using ExecuteQuery: {e}")

print("\n--- Demonstrating ExecuteQuery Context Manager with an UPDATE ---")
try:
    update_query = "UPDATE users SET age = ? WHERE id = ?"
    update_params = (31, 1) # Update John Doe's age to 31
    with ExecuteQuery(query=update_query, params=update_params) as row_count:
        print(f"Rows updated: {row_count}")
    
    # Verify the update by fetching the user again
    print("\n--- Verifying the update ---")
    with ExecuteQuery(query="SELECT * FROM users WHERE id = ?", params=(1,)) as updated_user:
        print(f"Updated user 1 details: {updated_user}")

except Exception as e:
    print(f"An error occurred using ExecuteQuery for update: {e}")

print("\n--- Demonstrating ExecuteQuery Context Manager with a simulated error ---")
try:
    faulty_query = "SELECT * FROM non_existent_table"
    with ExecuteQuery(query=faulty_query) as results:
        print("Results (should not be reached if error occurs):", results)
except Exception as e:
    print(f"Caught expected error from ExecuteQuery usage: {e}")

