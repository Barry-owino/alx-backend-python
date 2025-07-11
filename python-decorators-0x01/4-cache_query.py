import sqlite3
import functools
import time

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

def transactional(func):
    """
    Decorator that manages database transactions.
    It assumes the decorated function receives a 'conn' (connection) object
    as its first argument. If the function executes successfully, the transaction
    is committed; otherwise, it is rolled back.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs): # 'conn' is expected as the first arg
        try:
            result = func(conn, *args, **kwargs)
            conn.commit() # Commit changes if function executes successfully
            print("Transaction committed successfully.")
            return result
        except Exception as e:
            if conn:
                conn.rollback() # Rollback changes if an error occurs
                print(f"Transaction rolled back due to error: {e}")
            raise # Re-raise the original exception
    return wrapper

def retry_on_failure(retries=3, delay=2):
    """
    Decorator that retries the decorated function a certain number of times
    if it raises an exception.
    :param retries: The maximum number of times to retry the function.
    :param delay: The delay in seconds between retries.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(retries + 1): # +1 to include the initial attempt
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i < retries:
                        print(f"Attempt {i + 1}/{retries + 1} failed: {e}. Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print(f"All {retries + 1} attempts failed. Last error: {e}")
                        raise # Re-raise the last exception if all retries are exhausted
        return wrapper
    return decorator

# Global cache dictionary for query results
query_cache = {}

def cache_query(func):
    """
    Decorator that caches query results based on the SQL query string.
    It assumes the SQL query is passed as a keyword argument named 'query'.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        query = kwargs.get('query') # Get query from kwargs

        if query in query_cache:
            print(f"--- CACHE HIT --- Returning cached result for query: {query}")
            return query_cache[query]
        
        print(f"--- CACHE MISS --- Executing query: {query}")
        result = func(conn, *args, **kwargs)
        query_cache[query] = result # Store result in cache
        return result
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

# --- Decorated Functions ---

@with_db_connection
def get_user_by_id(conn, user_id):
    """
    Fetches a user from the database by their ID using the provided connection.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """
    Updates a user's email. This function is wrapped in a transaction.
    """
    cursor = conn.cursor()
    print(f"Attempting to update user ID {user_id} email to {new_email}...")
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    if cursor.rowcount == 0:
        raise ValueError(f"User with ID {user_id} not found or email is already {new_email}.")
    print(f"Successfully executed UPDATE for user ID {user_id}.")


@with_db_connection
@transactional
def create_user_and_fail(conn, name, email, should_fail=True):
    """
    Attempts to create a new user and demonstrates a rollback if should_fail is True.
    """
    cursor = conn.cursor()
    print(f"Attempting to insert user: {name} ({email})...")
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    print(f"Successfully executed INSERT for user: {name}.")
    
    if should_fail:
        print("Simulating an error to trigger rollback...")
        raise ValueError("Simulated error during transaction!")
    else:
        print("No simulated error, transaction should commit.")

# Global counter for simulating transient errors
_simulate_fetch_error_count = 0

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """
    Attempts to fetch all users, simulating a transient error for demonstration.
    """
    global _simulate_fetch_error_count
    _simulate_fetch_error_count += 1

    if _simulate_fetch_error_count <= 2: # Simulate failure for the first 2 attempts
        print(f"Simulating a transient database error on attempt {_simulate_fetch_error_count}...")
        raise sqlite3.OperationalError("Database is temporarily unavailable.")
    
    print(f"Attempt {_simulate_fetch_error_count} succeeded. Fetching users...")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """
    Fetches users from the database, with results being cached.
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# --- Demonstration of Usage ---

print("--- Fetching user by ID with automatic connection handling ---")
user = get_user_by_id(user_id=1)
print(f"Fetched User by ID 1: {user}")

print("\n--- Updating user's email (successful transaction) ---")
try:
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
    print("Email update operation completed.")
except Exception as e:
    print(f"Email update operation failed: {e}")

print("\n--- Verify updated email ---")
user_updated = get_user_by_id(user_id=1)
print(f"User ID 1 after update: {user_updated}")

print("\n--- Attempting to update non-existent user's email (transactional rollback expected) ---")
try:
    update_user_email(user_id=999, new_email='nonexistent@example.com')
    print("Email update operation completed (unexpectedly).")
except Exception as e:
    print(f"Email update operation failed as expected: {e}")

print("\n--- Verify non-existent user was not created/affected ---")
user_non_existent = get_user_by_id(user_id=999)
print(f"User ID 999 after failed update attempt: {user_non_existent}")

print("\n--- Demonstrating transactional rollback with simulated error ---")
try:
    create_user_and_fail(name="Ephemeral User", email="ephemeral@example.com", should_fail=True)
    print("User creation operation completed (unexpectedly).")
except Exception as e:
    print(f"User creation operation failed as expected: {e}")

print("\n--- Verify Ephemeral User was NOT created (due to rollback) ---")
ephemeral_user = get_user_by_id(user_id=4) # Assuming ID 4 would be next if committed
print(f"Ephemeral User after rollback: {ephemeral_user}") # Should be None if rolled back

print("\n--- Demonstrating transactional commit without error ---")
try:
    create_user_and_fail(name="Persistent User", email="persistent@example.com", should_fail=False)
    print("Persistent User creation operation completed successfully.")
except Exception as e:
    print(f"Persistent User creation operation failed: {e}")

print("\n--- Verify Persistent User WAS created (due to commit) ---")
persistent_user = get_user_by_id(user_id=4) # Assuming ID 4 would be next if committed
print(f"Persistent User after commit: {persistent_user}") # Should show the user if committed

print("\n--- Attempting to fetch users with automatic retry on failure ---")
try:
    users_with_retry = fetch_users_with_retry()
    print("\nFetched Users with Retry (after successful retry):")
    for user_r in users_with_retry:
        print(user_r)
except Exception as e:
    print(f"Failed to fetch users after all retries: {e}")

# Reset the error count for potential re-runs or further tests
_simulate_fetch_error_count = 0

print("\n--- Attempting fetch with retry, simulating enough failures to exhaust retries ---")
try:
    # Set global counter to simulate failures for all 3 retries + initial attempt
    _simulate_fetch_error_count = 0 # Reset for this test
    # This call will fail 3 times and then the 4th attempt (initial + 3 retries) will also fail,
    # causing the decorator to re-raise the last exception.
    fetch_users_with_retry()
except Exception as e:
    print(f"Successfully caught expected failure after all retries: {e}")

print("\n--- Demonstrating query caching ---")
print("First call to fetch_users_with_cache:")
# First call will execute the query and cache the result
users_cached_first = fetch_users_with_cache(query="SELECT * FROM users")
print("Result from first call:", users_cached_first)

print("\nSecond call to fetch_users_with_cache (should use cache):")
# Second call will use the cached result without executing the query
users_cached_second = fetch_users_with_cache(query="SELECT * FROM users")
print("Result from second call:", users_cached_second)

print("\nThird call with a different query (should not use cache for the new query):")
# Call with a different query, which should result in a cache miss
users_cached_different = fetch_users_with_cache(query="SELECT * FROM users WHERE id = 1")
print("Result from third call:", users_cached_different)

