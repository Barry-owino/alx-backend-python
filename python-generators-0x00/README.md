
This project involves writing a Python script (`seed.py`) that connects to a local MySQL server, creates a database table called `user_data`, and populates it using a CSV file (`user_data.csv`). It prevents duplicate entries and uses UUIDs for user identification.

---

## 📁 Files Included

| File            | Description                                                                 |
|-----------------|-----------------------------------------------------------------------------|
| `seed.py`       | Main script that connects to MySQL, creates the `user_data` table, and inserts data from the CSV. |
| `user_data.csv` | Sample user data to seed the database.                                      |
| `README.md`     | Project documentation.                                                      |

---

## ⚙️ Setup Instructions

1. ✅ Ensure **MySQL Server is running locally** on your machine.

2. ✅ Manually create the database in MySQL:

```sql
CREATE DATABASE ALX_prodev;

✅ Update the MySQL password inside seed.py if needed:

python
Copy
Edit
password='your_mysql_password'
✅ Run the script from your terminal:

bash
Copy
Edit
python3 seed.py
✅ What the Script Does
Connects to the local MySQL server

Connects to the ALX_prodev database

Creates the user_data table (if it doesn't already exist)

Reads data from user_data.csv

Inserts each user into the table using a generated UUID

Skips inserting any user whose email already exists

📤 Sample Output
java
Copy
Edit
✅ Connected to ALX_prodev database.
✅ Table 'user_data' ensured.
✅ Inserted: Alice Johnson (alice@example.com)
⚠️ Skipped duplicate: john@example.com
👨‍💻 Author
Barry Owino

GitHub: Barry-owino
