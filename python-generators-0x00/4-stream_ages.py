import mysql.connector
from mysql.connector import Error

def stream_user_ages():
    """
    Generator that yields one user age at a time from the database.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Legionnaire@27'
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT age FROM user_data;")

            for (age,) in cursor:
                yield age

            cursor.close()
            connection.close()

    except Error as e:
        print(f"❌ Error: {e}")


def calculate_average_age():
    """
    Uses the generator to calculate the average user age.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        print("No users found.")
    else:
        average = total_age / count
        print(f"Average age of users: {average:.2f}")


if __name__ == "__main__":
    calculate_average_age()

