# ui/auth_frame.py
import customtkinter
from tkinter import messagebox
from db.user_repo import UserRepo
from utils.auth_validation import validate_username, validate_password

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

        if self.user_repo.verify_user(username, password):
            messagebox.showinfo("Success", f"Welcome, {username}!")
            self.on_login_success()
        else:
            messagebox.showerror("Error", "Invalid username or password.")


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
            messagebox.showinfo("Success", "Account created successfully! Please log in.")
            self.show_login()
        else:
            messagebox.showerror("Error", "Username already exists. Try a different one.")
