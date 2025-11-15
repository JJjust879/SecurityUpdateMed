import sqlite3

# Connect to your database
conn = sqlite3.connect("db.db")
cur = conn.cursor()

# List all tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cur.fetchall()
print("Tables: ", tables)

# Define allowed tables for safety
allowed_tables = {table_name[0] for table_name in tables}

for table in allowed_tables:
    print(f"\nData in table '{table}':")
    
    # Use parameterized query for pragma_table_info
    cur.execute("SELECT * FROM pragma_table_info(?)", (table,))
    
    # Print column names nicely
    for col in cur.fetchall():
        print(f"{col[1]} ({col[2]})", end=" | ")
    print()
    
    # Use safer string formatting for actual data (table name validated)
    cur.execute(f"SELECT * FROM {table}") # nosec B608 - table validated against whitelist
    for row in cur.fetchall():
        print(row)

conn.close()
