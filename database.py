import sqlite3

# Connect to your database
conn = sqlite3.connect("cdr_pipeline.db")
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables:", cursor.fetchall())

# Preview first 5 rows of the correct table
cursor.execute("SELECT * FROM CDR_Transformed LIMIT 5;")
for row in cursor.fetchall():
    print(row)

conn.close()
