import mysql.connector
from mysql.connector import Error

def stream_users():
    """Generator that yields rows one by one from user_data table."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Legionnaire@27',
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data;")

            for row in cursor:
                yield row  # 🔁 Yield one row at a time

            cursor.close()
            connection.close()

    except Error as e:
        print(f"❌ Error while streaming users: {e}")

