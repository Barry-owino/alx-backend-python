import asyncio
import aiosqlite
import sqlite3 # Used for initial synchronous setup of the database

# --- Database Setup (synchronous, for initial creation and data insertion) ---
# This function ensures the database and table exist before async operations start.
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
        cursor_setup.execute("INSERT OR IGNORE INTO users (id, name, email, age) VALUES (5, 'Bob White', 'bob@example.com', 55)")
        conn_setup.commit()
    except sqlite3.Error as e:
        print(f"Synchronous database setup error: {e}")
    finally:
        if conn_setup:
            conn_setup.close()

# Run the synchronous database setup once
setup_database()

# --- Asynchronous Database Functions ---

async def async_fetch_users(db_name='users.db'):
    """
    Asynchronously fetches all users from the database.
    """
    print(f"[{asyncio.current_task().get_name()}] Fetching all users from {db_name}...")
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT id, name, email, age FROM users") as cursor:
            users = await cursor.fetchall()
            print(f"[{asyncio.current_task().get_name()}] All users fetched.")
            return users

async def async_fetch_older_users(age_threshold=40, db_name='users.db'):
    """
    Asynchronously fetches users older than a specified age from the database.
    """
    print(f"[{asyncio.current_task().get_name()}] Fetching users older than {age_threshold} from {db_name}...")
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT id, name, email, age FROM users WHERE age > ?", (age_threshold,)) as cursor:
            older_users = await cursor.fetchall()
            print(f"[{asyncio.current_task().get_name()}] Older users fetched.")
            return older_users

async def fetch_concurrently():
    """
    Executes multiple asynchronous database queries concurrently using asyncio.gather().
    """
    print("\n--- Starting concurrent database fetches ---")
    # asyncio.gather runs the coroutines concurrently.
    # It returns results in the order the coroutines were passed.
    
    # Explicitly passing db_name for clarity
    all_users_task = async_fetch_users(db_name='users.db')
    older_users_task = async_fetch_older_users(age_threshold=40, db_name='users.db') # Explicitly passed db_name

    # Assign names to tasks for clearer logging
    all_users_task.__name__ = "FetchAllUsersTask"
    older_users_task.__name__ = "FetchOlderUsersTask"

    results = await asyncio.gather(all_users_task, older_users_task)
    
    all_users_result = results[0]
    older_users_result = results[1]

    print("\n--- Concurrent Fetch Results ---")
    print("All Users:")
    for user in all_users_result:
        print(user)

    print("\nUsers Older Than 40:")
    for user in older_users_result:
        print(user)
    print("--------------------------------")

# --- Run the concurrent fetch ---
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
