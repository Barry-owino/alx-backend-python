import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    """
    Generator that yields batches of users from the user_data table.
    Each yield returns a list of up to 'batch_size' user dictionaries.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Legionnaire@27' 
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data;")

            batch = []
            for row in cursor:
                batch.append(row)
                if len(batch) == batch_size:
                    yield batch
                    batch = []
            if batch:
                yield batch

            cursor.close()
            connection.close()

    except Error as e:
        print(f"❌ Error: {e}")


def batch_processing(batch_size):
    """
    Generator that yields users over age 25 from each batch.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                yield user

