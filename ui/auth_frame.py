# ui/auth_frame.py
import customtkinter
from tkinter import messagebox
from db.user_repo import UserRepo
from utils.auth_validation import validate_username, validate_password

# For login activity log
from utils.logger import log_event

class AuthFrame(customtkinter.CTkFrame):
    def __init__(self, master, db, on_login_success):
        super().__init__(master, fg_color="#87CEEB")
        self.user_repo = UserRepo(db)
        self.on_login_success = on_login_success

        # Nested frames for switching
        self.login_frame = LoginFrame(self, self.user_repo, self.show_register, 
                                      self.on_login_success)
        self.register_frame = RegisterFrame(self, self.user_repo, self.show_login)

        self.login_frame.pack(fill="both", expand=True)

    def show_register(self):
        self.login_frame.pack_forget()
        self.register_frame.pack(fill="both", expand=True)

    def show_login(self):
        self.register_frame.pack_forget()
        self.login_frame.pack(fill="both", expand=True)


# ------------------ LOGIN FRAME ------------------

class LoginFrame(customtkinter.CTkFrame):
    def __init__(self, master, user_repo, show_register, on_login_success):
        super().__init__(master, fg_color="#87CEEB")
        self.user_repo = user_repo
        self.show_register = show_register
        self.on_login_success = on_login_success

        title = customtkinter.CTkLabel(self, text="VitalCare Login", font=("Arial", 24, "bold"))
        title.pack(pady=30)

        self.username_entry = customtkinter.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=10, ipadx=50, ipady=5)

        self.password_entry = customtkinter.CTkEntry(self, placeholder_text="Password", show="•")
        self.password_entry.pack(pady=10, ipadx=50, ipady=5)

        login_btn = customtkinter.CTkButton(self, text="Login", command=self.login_user)
        login_btn.pack(pady=20)

        register_link = customtkinter.CTkButton(
            self, text="Create an account", fg_color="transparent",
            text_color="#0047AB", hover_color="#E0FFFF", command=self.show_register
        )
        register_link.pack(pady=5)

    def login_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Missing Info", "Please enter both username and password.")
            return

        # Before checking the password,
        # verify if this user is currently locked from logging in or not
        allowed, wait_s = self.user_repo.can_attempt_login(username)

        # If they are locked, display the message accordingly
        if not allowed:

            # Record the lock getting locked
            log_event("ACCOUNT_LOCKED", username)

            # Convert seconds to minutes
            mins = wait_s // 60

            # Remaining seconds after minutes
            secs = wait_s % 60

            # Display message
            messagebox.showerror("Locked", f"Too many failed attempts.\nTry again in {mins}m {secs}s.")
            return

        # If they are not locked and the user logs in correctly
        if self.user_repo.verify_user(username, password):
            # Reset the two columns (failed_attempts, locked_until)
            # for this user in the users table to default values.
            self.user_repo.record_successful_login(username)

            # Get this user's role and pass it forward
            role = self.user_repo.get_user_role(username) or "staff"

            # Log user successful login
            log_event("LOGIN_SUCCESS", username)
            # Doing that will make the app
            # write a line shown below in the security_log.txt file:
            # 2025-11-05 03:27:10 | LOGIN_SUCCESS | user=alex

            # Display a message
            messagebox.showinfo("Success", f"Welcome, {username}!")
            self.on_login_success(username, role)

        # If they are not locked but the user logs in incorrectly
        else:
            # Record the user trying to login with an account that does not exist
            if not self.user_repo.get_user(username):
                log_event("LOGIN_FAILED_UNKNOWN_USER", username)

            # Record the user failure to login
            else:
                log_event("LOGIN_FAILED", username)

            # Increase failed attempts by one
            # And maybe lock it if it reached max allowed login
            self.user_repo.record_failed_login(username)
            failed, _ = self.user_repo.get_lock_state(username)
            remaining = max(self.user_repo.LOCK_THRESHOLD - failed, 0)

            # Do something when remaining is equal to 0

            # Display message accordingly
            extra = f"\nAttempts left before lock: {remaining}" if remaining > 0 else ""
            messagebox.showerror("Error", f"Invalid username or password.{extra}")



# ------------------ REGISTER FRAME ------------------

class RegisterFrame(customtkinter.CTkFrame):
    def __init__(self, master, user_repo, show_login):
        super().__init__(master, fg_color="#87CEEB")
        self.user_repo = user_repo
        self.show_login = show_login

        title = customtkinter.CTkLabel(self, text="Create Account", font=("Arial", 24, "bold"))
        title.pack(pady=30)

        self.username_entry = customtkinter.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=10, ipadx=50, ipady=5)

        self.password_entry = customtkinter.CTkEntry(self, placeholder_text="Password", show="•")
        self.password_entry.pack(pady=10, ipadx=50, ipady=5)

        self.confirm_entry = customtkinter.CTkEntry(self, placeholder_text="Confirm Password", show="•")
        self.confirm_entry.pack(pady=10, ipadx=50, ipady=5)

        hint_label = customtkinter.CTkLabel(
            self,
            text="Password must be ≥8 chars, with uppercase, number, and symbol.",
            font=("Arial", 12), text_color="#0047AB"
        )
        hint_label.pack(pady=(5, 15))

        register_btn = customtkinter.CTkButton(self, text="Register", command=self.register_user)
        register_btn.pack(pady=20)

        login_link = customtkinter.CTkButton(
            self, text="Back to Login", fg_color="transparent",
            text_color="#0047AB", hover_color="#E0FFFF",
            command=self.show_login
        )
        login_link.pack(pady=5)

    def register_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm = self.confirm_entry.get().strip()

        # --- Validate inputs ---
        if not username or not password or not confirm:
            messagebox.showwarning("Missing Info", "Please fill in all fields.")
            return

        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        # Optional: Use validators if available
        username_error = validate_username(username)
        if username_error:
            messagebox.showerror("Invalid Username", username_error)
            return

        password_error = validate_password(password)
        if password_error:
            messagebox.showerror("Invalid Password", password_error)
            return

        # --- Add user ---
        success = self.user_repo.add_user(username, password)
        if success:
            # Record user successful account creation
            log_event("ACCOUNT_CREATED", username)

            messagebox.showinfo("Success", "Account created successfully! Please log in.")
            self.show_login()
        else:
            messagebox.showerror("Error", "Username already exists. Try a different one.")
