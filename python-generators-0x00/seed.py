import csv
import uuid
import mysql.connector
from mysql.connector import Error

def connect_to_prodev():
    """Connect to the existing ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Legionnaire@27',
            database='ALX_prodev'
        )
        if connection.is_connected():
            print("✅ Connected to ALX_prodev database.")
            return connection
    except Error as e:
        print(f"❌ Error: {e}")
        return None

def create_table(connection):
    """Create the user_data table if it doesn't exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(3, 0) NOT NULL,
                INDEX(email)
            );
        """)
        connection.commit()
        print("✅ Table 'user_data' ensured.")
    except Error as e:
        print(f"❌ Failed to create table: {e}")

def insert_data(connection, data):
    """Insert one row of data if email doesn't already exist."""
    try:
        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM user_data WHERE email = %s"
        cursor.execute(query, (data['email'],))
        exists = cursor.fetchone()[0]

        if exists == 0:
            insert_query = """
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s);
            """
            cursor.execute(insert_query, (
                str(uuid.uuid4()),  # Generate UUID
                data['name'],
                data['email'],
                data['age']
            ))
            connection.commit()
            print(f"✅ Inserted: {data['name']} ({data['email']})")
        else:
            print(f"⚠️ Skipped duplicate: {data['email']}")

    except Error as e:
        print(f"❌ Error inserting data: {e}")

def seed_from_csv(connection, file_path='user_data.csv'):
    """Read data from CSV and insert into the database."""
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                insert_data(connection, row)
    except FileNotFoundError:
        print("❌ CSV file not found.")
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")

if __name__ == "__main__":
    conn = connect_to_prodev()
    if conn:
        create_table(conn)
        seed_from_csv(conn)
        conn.close()

