import sqlite3
import bcrypt

class UserRepo:
    def __init__(self, db):
        self.db = db
        self.create_user_table()

    def create_user_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
        """
        self.db.execute(query)

    def add_user(self, username: str, password: str) -> bool:
        """Add a new user with hashed password. Returns True if successful, False if username exists."""
        try:
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            self.db.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            return True
        except sqlite3.IntegrityError:
            return False  # username already exists

    def get_user(self, username: str):
        """Return user tuple (id, username, password_hash) or None."""
        user = self.db.fetch_one(
            "SELECT * FROM users WHERE username=?", (username,)
        )
        
        if not user:
            return None
        return user

    def verify_user(self, username: str, password: str) -> bool:
        """Check if username and password match."""
        user = self.get_user(username)
        if user:
            stored_hash = user[2]  # index 2 = password_hash
            return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
        return False
