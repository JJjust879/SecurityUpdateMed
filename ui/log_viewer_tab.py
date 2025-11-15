import customtkinter
from pathlib import Path
import os

class LogViewerTab(customtkinter.CTkFrame):
    def __init__(self, master, log_path="security_log.txt"):
        super().__init__(master, fg_color="#87CEEB")
        self.log_path = Path(log_path)

        # Title
        title = customtkinter.CTkLabel(self, text="Security Log Viewer",
                                       font=("Arial", 20, "bold"))
        title.pack(pady=(10, 6))

        # --- header bar with buttons so they never get hidden ---
        header = customtkinter.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(0, 6))

        self.refresh_btn = customtkinter.CTkButton(header, text="Refresh Log",
                                                   command=self.load_log)
        self.refresh_btn.pack(side="left")

        self.open_btn = customtkinter.CTkButton(header, text="Open in Editor",
                                                command=self.open_in_editor)
        self.open_btn.pack(side="left", padx=10)

        # Log textbox (with some padding so buttons stay visible)
        self.textbox = customtkinter.CTkTextbox(self, width=700, height=400)
        self.textbox.pack(fill="both", expand=True, padx=20, pady=(0, 12))

        self.load_log()

    def load_log(self):
        """Load and display the contents of security_log.txt"""
        if not self.log_path.exists():
            self.textbox.delete("1.0", "end")
            self.textbox.insert("1.0", "No logs found yet.")
            return

        with self.log_path.open("r", encoding="utf-8") as f:
            contents = f.read()

        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", contents)

    def open_in_editor(self):
        """Open the log file with the default editor (optional helper)."""
        if self.log_path.exists():
            os.startfile(self.log_path)  # works on Windows # nosec B606 - safe: fixed path
