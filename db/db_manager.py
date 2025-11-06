import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        # Connects to the file (db.db)
        self.con = sqlite3.connect(db_name)
        # A cursor, which is the object you use to run SQL statements
        self.cur = self.con.cursor()

    # Returns one or more matching rows
    def fetch_all(self, query, params=()):
        self.cur.execute(query, params)
        return self.cur.fetchall()

    # Returns one row
    def fetch_one(self, query, params=()):
        self.cur.execute(query, params)
        return self.cur.fetchone()

    # For write operations (INSERT/UPDATE/DELETE/CREATE, etc.).
    # After executing,
    # it calls commit() to save the change to the database file.
    def execute(self, query, params=()):
        self.cur.execute(query, params)
        self.con.commit()

    # Closes the database connection when you’re done.
    def close(self):
        self.con.close()
