import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()

    def fetch_all(self, query, params=()):
        self.cur.execute(query, params)
        return self.cur.fetchall()

    def fetch_one(self, query, params=()):
        self.cur.execute(query, params)
        return self.cur.fetchone()

    def execute(self, query, params=()):
        self.cur.execute(query, params)
        self.con.commit()

    def close(self):
        self.con.close()
