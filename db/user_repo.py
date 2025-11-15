import sqlite3
import bcrypt
import time


class UserRepo:
    def __init__(self, db):
        self.db = db
        self.create_user_table()

    # Make sure the "users" table exists in the database
    def create_user_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'staff',
            failed_attempts INTEGER NOT NULL DEFAULT 0,
            locked_until INTEGER
        )
        """
        self.db.execute(query)

    # Takes a plain password,
    # and then hashes it using bcrypt,
    # and then saves it.
    # So that password is not stored in plain text
    def add_user(self, username: str, password: str, role: str = "staff") -> bool:
        """
        Add a new user with hashed password and role.
        Returns True if successful, False if username exists.
        """
        try:
            password_hash = bcrypt.hashpw(
                password.encode('utf-8'),
                bcrypt.gensalt(rounds=12)  # cost factor (12 is a safe, common default)
            )

            self.db.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, password_hash, role)
            )
            return True

        except sqlite3.IntegrityError:
            # username already exists
            return False

        except sqlite3.Error as e:
            # Any other database error (file missing, corrupted, etc.)
            print(f"Database error while adding user: {e}")
            return False

    # Finds a specific user by username
    def get_user(self, username: str):
        """Return user tuple (id, username, password_hash) or None."""
        user = self.db.fetch_one(
            "SELECT * FROM users WHERE username=?", (username,)
        )

        if not user:
            return None
        return user

    # Gets the user,
    # then checks if the password matches the hash.

    def verify_user(self, username: str, password: str) -> bool:
        """
        Check if username and password match.
        Returns False on mismatch or any database/crypto error (fails safely).
        """
        try:
            # Look up this username in the database
            user = self.get_user(username)
            if not user:
                # If no record found → invalid username
                return False

            # Extract the stored password hash (index 2 in the row)
            stored_hash = user[2]

            # Defensive: sometimes data might come back as text instead of bytes
            if isinstance(stored_hash, str):
                stored_hash = stored_hash.encode("utf-8")

            # bcrypt.checkpw() compares the entered password with the stored hash
            return bcrypt.checkpw(password.encode("utf-8"), stored_hash)

        except sqlite3.Error as e:
            # Database-related problems (file missing, corrupt, etc.)
            print(f"Database error in verify_user: {e}")
            return False

        except Exception as e:
            # Any other unexpected error (keeps the app from crashing)
            print(f"Unexpected error in verify_user: {e}")
            return False


    # Lockout configurations - Start
    # After 5 wrong passwords, lock the account
    LOCK_THRESHOLD = 5

    # Stay locked for 5 minutes
    LOCK_DURATION_SEC = 5 * 60

    # Returns the current time as integer
    def _now(self) -> int:
        return int(time.time())  # epoch seconds

    # Read the user's current lock state from DB and returns them.
    # They will be returned as a tuple
    # (failed_attempts, locked_until)
    def get_lock_state(self, username: str):
        row = self.db.fetch_one(
            "SELECT failed_attempts, locked_until FROM users WHERE username = ?",
            (username,)
        )

        if row is None:
            return 0, None  # user not found => no lock state

        return row[0], row[1]

    # Decides if the user can login now or not
    # Returns (allowed: bool, seconds_remaining: int).
    # If locked, allowed=False and seconds_remaining > 0.
    # If not locked, allowed=True and seconds_remaining = 0
    def can_attempt_login(self, username: str) -> tuple[bool, int]:
        # Call get_lock_state() function
        # It returns the value of
        # failed_attempts and locked_until of a user, from the database
        failed, locked_until = self.get_lock_state(username)

        # Get the current time in integer
        now = self._now()

        # If current time (now) has NOT reached the unlock time (locked_until) yet
        # Meaning the account is still locked
        if locked_until is not None and locked_until > now:
            # Return (False, seconds remaining)
            return False, locked_until - now

        # If current time (now) has reached the unlock time (locked_until)
        # Meaning the account is not or no longer locked
        # Return (True, 0 second remaining)
        return True, 0

    # This function is called
    # whenever the user enters a wrong password.
    def record_failed_login(self, username: str):

        # Get the value of failed_attempts of a user from the database
        # and store it in the failed variable
        failed, _ = self.get_lock_state(username)

        # Add 1
        failed += 1

        # If the user reached the max allowed failed logins
        if failed >= self.LOCK_THRESHOLD:

            # Lock this account for x seconds (LOCK_DURATION_SEC)
            # starting from now (current time) (_now())
            # Not actually locking it in this function,
            # just creating a value for the locked_until column in the table
            new_locked_until = self._now() + self.LOCK_DURATION_SEC

            # Update the value of failed_attempts and locked_until in the database
            self.db.execute(
                "UPDATE users SET failed_attempts = ?, locked_until = ? WHERE username = ?",
                (failed, new_locked_until, username),
            )

        # If the user has not reached the max allowed failed logins
        else:
            # Only update failed_attempt column
            self.db.execute(
                "UPDATE users SET failed_attempts = ? WHERE username = ?",
                (failed, username),
            )

    # This function is called when the user logs in with correct password
    def record_successful_login(self, username: str):
        # Reset the value of failed_attempts to 0
        # Reset the value of locked_until to NULL
        # Update it in the table
        self.db.execute(
            "UPDATE users SET failed_attempts = 0, locked_until = NULL WHERE username = ?",
            (username,),
        )
    # Lockout configurations - End

    # Get the value of "role" column of a row
    # In other words, get the user's role
    def get_user_role(self, username: str) -> str | None:
        """Return the role string for this username, or None if not found."""
        row = self.db.fetch_one("SELECT role FROM users WHERE username = ?", (username,))
        return row[0] if row else None

