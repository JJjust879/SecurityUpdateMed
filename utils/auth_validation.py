import re

def validate_username(username: str) -> str | None:
    """Return an error message if invalid, else None."""
    if len(username) < 4:
        return "Username must be at least 4 characters long."
    if " " in username:
        return "Username cannot contain spaces."
    if not re.match(r"^[A-Za-z0-9_.-]+$", username):
        return "Username can only contain letters, numbers, underscores, dots, and hyphens."
    return None

def validate_password(password: str) -> str | None:
    """Return an error message if invalid, else None."""
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return "Password must contain at least one lowercase letter."
    if not re.search(r"[0-9]", password):
        return "Password must contain at least one number."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "Password must contain at least one special character (!@#$%^&*, etc.)."
    return None
