from customtkinter import CTkToplevel, CTkLabel, CTkEntry, CTkFrame, CTkButton, CTkComboBox
from utils.helpers import show_messagebox


class ChangeDosagePopup(CTkToplevel):
    def __init__(self, parent, selected_pid, med_name, dosage_repo, refresh_callback):
        """
        parent: parent window (the tab or main window)
        selected_pid: patient ID
        med_name: medicine name to update
        dosage_repo: repository class handling DB updates
        refresh_callback: function to refresh prescription list after update
        """
        super().__init__(parent)

        self.selected_pid = selected_pid
        self.med_name = med_name
        self.dosage_repo = dosage_repo
        self.refresh_callback = refresh_callback

        self.title("Change Dosage")
        self.geometry("320x220")

        self.setup_ui()

    def setup_ui(self):
        # --- Header ---
        CTkLabel(
            self,
            text=f"Medicine: {self.med_name}",
            font=("", 14, "bold")
        ).pack(pady=(10, 5))

        # --- Dosage input row ---
        CTkLabel(self, text="New Dosage:").pack()

        dosage_frame = CTkFrame(self, fg_color="transparent")
        dosage_frame.pack(pady=5)

        # Numeric dosage entry
        self.dosage_entry = CTkEntry(dosage_frame, width=100, justify="center")
        self.dosage_entry.pack(side="left", padx=(0, 5))

        # Dropdown for dosage type
        self.dtype_box = CTkComboBox(
            dosage_frame,
            width=80,
            values=["mg", "g", "mcg", "capsule", "tablet"],
            state="readonly"
        )
        self.dtype_box.set("mg")  # default selection
        self.dtype_box.pack(side="left")

        # --- Action button ---
        CTkButton(
            self,
            text="Update",
            fg_color="#e9c46a",
            command=self.update_dosage
        ).pack(pady=20)

    # --- Logic ---
    def update_dosage(self):
        new_dosage = self.dosage_entry.get().strip()
        dtype = self.dtype_box.get().strip()

        if not new_dosage:
            show_messagebox("Error", "Please enter a dosage amount.", icon="error")
            return

        if not new_dosage.isdigit():
            show_messagebox("Error", "Dosage must be a number.")
            return

        # Update database
        self.dosage_repo.update_dosage(
            self.selected_pid,
            self.med_name,
            new_dosage,
            dtype
        )

        show_messagebox("Success", f"Dosage updated to {new_dosage}{dtype}.")
        self.destroy()

        if callable(self.refresh_callback):
            self.refresh_callback()
