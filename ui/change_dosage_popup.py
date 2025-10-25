from customtkinter import CTkToplevel, CTkLabel, CTkEntry, CTkFrame, CTkButton, CTkComboBox
from db.dosage_repo import DosageRepo
from db.medicine_repo import MedicineRepo
from utils.helpers import show_messagebox


# --- Validation Helpers ---
def validate_dosage_input(dosage_str):
    """Ensure dosage input is not empty and numeric."""
    if not dosage_str:
        return "Please enter a dosage amount."
    if not dosage_str.isdigit():
        return "Dosage must be a number."
    return None


def validate_dosage_in_range(medicine_repo, med_name, dosage_value):
    """Ensure dosage value is within medicine's allowed range."""
    dosage_range = medicine_repo.get_min_max_dosage(med_name)
    if not dosage_range:
        return f"Medicine '{med_name}' not found in database."

    min_dosage, max_dosage = dosage_range
    if not (min_dosage <= dosage_value <= max_dosage):
        return f"Dosage for '{med_name}' must be between {min_dosage} and {max_dosage}."
    return None


class ChangeDosagePopup(CTkToplevel):
    def __init__(self, parent, selected_pid, med_name, db, refresh_callback):
        super().__init__(parent)

        self.selected_pid = selected_pid
        self.med_name = med_name
        self.dosage_repo = DosageRepo(db)
        self.medicine_repo = MedicineRepo(db)
        self.refresh_callback = refresh_callback

        self.title("Change Dosage")
        self.geometry("320x220")
        self.setup_ui()

    def setup_ui(self):
        # Header
        CTkLabel(
            self, text=f"Medicine: {self.med_name}", font=("", 14, "bold")
        ).pack(pady=(10, 5))

        # Dosage input
        CTkLabel(self, text="New Dosage:").pack()
        dosage_frame = CTkFrame(self, fg_color="transparent")
        dosage_frame.pack(pady=5)

        self.dosage_entry = CTkEntry(dosage_frame, width=100, justify="center")
        self.dosage_entry.pack(side="left", padx=(0, 5))

        self.dtype_box = CTkComboBox(
            dosage_frame,
            width=80,
            values=["mg", "g", "mcg", "capsule", "tablet"],
            state="readonly"
        )
        self.dtype_box.set("mg")
        self.dtype_box.pack(side="left")

        CTkButton(
            self,
            text="Update",
            fg_color="#e9c46a",
            command=self.update_dosage
        ).pack(pady=20)

    def update_dosage(self):
        new_dosage = self.dosage_entry.get().strip()
        dtype = self.dtype_box.get().strip()

        # --- Validate Input ---
        err = validate_dosage_input(new_dosage)
        if err:
            show_messagebox("Error", err)
            return

        dosage_value = float(new_dosage)
        err = validate_dosage_in_range(self.medicine_repo, self.med_name, dosage_value)
        if err:
            show_messagebox("Error", err)
            return

        # --- Update Database ---
        self.dosage_repo.update_dosage(self.selected_pid, self.med_name, new_dosage, dtype)

        show_messagebox("Success", f"Dosage updated to {new_dosage}{dtype}.")
        self.destroy()

        if callable(self.refresh_callback):
            self.refresh_callback()
