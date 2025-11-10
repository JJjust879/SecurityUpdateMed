# utils/logger.py
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("security_log.txt")  # this will be created in your project folder

def log_event(event: str, username: str | None = None):
    """
    Append a simple, timestamped security event to a text file.
    Examples:
      log_event("LOGIN_SUCCESS", "alice")
      log_event("LOGIN_FAILED", "bob")
      log_event("ACCOUNT_LOCKED", "bob")
      log_event("ACCOUNT_CREATED", "newuser")
    """
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user = username or "-"
    line = f"{ts} | {event} | user={user}\n"
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line)
