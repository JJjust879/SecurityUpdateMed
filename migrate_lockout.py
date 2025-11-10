# This python file creates two new columns in the users table
# failed_attempts and locked_util
import sqlite3

# Open the database file and get a cursor (the thing that runs SQL commands)
con = sqlite3.connect("db.db")
cur = con.cursor()

# Store all column names from users table
# so that we can check whether
# failed_attempts and locked_util columns exist or not
cur.execute("PRAGMA table_info(users);")
cols = {c[1] for c in cur.fetchall()}

# If failed_attempts column does not exist in users table
# create this column
if "failed_attempts" not in cols:
    # initial value is set to 0
    cur.execute("ALTER TABLE users ADD COLUMN failed_attempts INTEGER NOT NULL DEFAULT 0")
    print("Added failed_attempts")

# If locked_util column does not exist in users table
# create this column
if "locked_until" not in cols:
    # store epoch seconds (integer). NULL means "not locked"
    cur.execute("ALTER TABLE users ADD COLUMN locked_until INTEGER")
    print("Added locked_until")

# Save the changes to the file and close the connection
con.commit()
con.close()
print("Done.")