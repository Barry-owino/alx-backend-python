import mysql.connector
from mysql.connector import Error

def paginate_users(page_size, offset):
    """
    Fetch a specific page of users from the database.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Legionnaire@27',
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM user_data LIMIT %s OFFSET %s;"
            cursor.execute(query, (page_size, offset))
            users = cursor.fetchall()

            cursor.close()
            connection.close()

            return users

    except Error as e:
        print(f"❌ Error: {e}")
        return []

def lazy_paginate(page_size):
    """
    Generator that lazily loads paginated data using one loop.
    """
    offset = 0
    while True:
        users = paginate_users(page_size, offset)
        if not users:
            break
        yield users
        offset += page_size

if __name__ == "__main__":
    print("📄 Lazily loading users in pages...\n")
    for page in lazy_paginate(5)
        print("🔹 New Page:")
        for user in page:
            print(f"🧑 {user['name']} | 📧 {user['email']} | 🎂 {user['age']}")
        print("------------")

