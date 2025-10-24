import sqlite3

# Connect to your database
conn = sqlite3.connect("db.db")
cur = conn.cursor()

# List all tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cur.fetchall()
print("Tables: ", tables)

for table_name in tables:
    table = table_name[0]
    print(f"\nData in table '{table}':")
    
    cur.execute(f"SELECT * FROM pragma_table_info('{table}');")

    # Print column names nicely
    for col in cur.fetchall():
        print(f"{col[1]} ({col[2]})", end=" | ")
    print()
    
    for row in cur.execute(f"SELECT * FROM {table};"):
        print(row)

conn.close()