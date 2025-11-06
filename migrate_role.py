import sqlite3

# This python file adds "role" column in the users table

con = sqlite3.connect("db.db")
cur = con.cursor()

# Check current columns on 'users'
cur.execute("PRAGMA table_info(users);")
cols = {c[1] for c in cur.fetchall()}

# Add role column if it does not exist
if "role" not in cols:
    cur.execute("ALTER TABLE users ADD COLUMN role TEXT NOT NULL DEFAULT 'staff'")
    print("Added role column (default 'staff')")

con.commit()
con.close()
print("Done.")