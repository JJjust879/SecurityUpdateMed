from customtkinter import CTkButton, CTkComboBox
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
from db.dosage_repo import DosageRepo
from db.patient_repo import PatientRepo
from ui.add_medicine_popup import AddMedicinePopup
from ui.change_dosage_popup import ChangeDosagePopup
from utils.helpers import show_messagebox


# --- Helper Functions ---
def create_search_section(tab, on_search_callback):
    """Create search controls for selecting patient."""
    pid_entry = CTkComboBox(tab, width=150, font=("", 14))
    pid_entry.place(relx=0.03, rely=0.04)
    pid_entry.set("Select Patient ID")

    search_btn = CTkButton(
        tab, text="Search", text_color="#000000",
        hover_color="#FFFFFF", fg_color="#f5f3e6", width=60,
        command=on_search_callback
    )
    search_btn.place(relx=0.26, rely=0.04)
    return pid_entry


def create_treeview(tab):
    """Create and configure the Treeview for prescriptions."""
    columns = {
        "illness": ("Illness", 120),
        "medicine": ("Medicine Name", 140),
        "dosage": ("Dosage", 120),
        "times_per": ("Times per", 120),
        "daysoftheweek": ("Days of the Week", 180),
        "frequency": ("Frequency", 120),
        "date_time": ("Date Time", 180)
    }

    tree = ttk.Treeview(tab, columns=list(columns.keys()), show="headings", height=15)
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("", 12, "bold"))
    style.configure("Treeview", font=("", 12))

    for col, (heading, width) in columns.items():
        tree.heading(col, text=heading)
        tree.column(col, width=width)

    tree.place(relx=0.03, rely=0.13)
    return tree


class PrescriptionTab:
    def __init__(self, tabview, db):
        self.db = db
        self.patient_repo = PatientRepo(db)
        self.dosage_repo = DosageRepo(db)
        self.tab = tabview.add("Medical Prescription")
        self.selected_pid = None

        # Build UI
        self.pid_entry = create_search_section(self.tab, self.load_prescriptions)
        self.tree = create_treeview(self.tab)
        
        buttons = [
            ("Add New", 0.03, "#6dc993", self.add_medicine_popup),
            ("Change Dosage", 0.18, "#e9c46a", self.change_dosage_popup),
            ("Delete", 0.35, "#e76f51", self.delete_medicine),
            ("Refresh", 0.5, "#87CEEB", self.load_prescriptions)
        ]
        for text, relx, color, cmd in buttons:
            CTkButton(self.tab, text=text, width=90, fg_color=color, command=cmd).place(relx=relx, rely=0.65)

        # Load data
        self.load_patient_ids()

    # --- Data Operations ---
    def load_patient_ids(self):
        patient_ids = self.patient_repo.get_all_patient_ids()
        self.pid_entry.configure(values=patient_ids)

    def load_prescriptions(self):
        pid = self.pid_entry.get()
        if not pid:
            show_messagebox("Info", "Please select a Patient ID first.")
            return

        self.selected_pid = pid
        dosages = self.dosage_repo.get_dosages_by_patient(pid)
        self.tree.delete(*self.tree.get_children())

        for dosage in dosages:
            self.tree.insert("", "end", values=dosage.to_tuple())

    def add_medicine_popup(self):
        if not self.selected_pid:
            show_messagebox("Info", "Please load a patient first.")
            return

        AddMedicinePopup(
            parent=self.tab,
            selected_pid=self.selected_pid,
            db=self.db,
            refresh_callback=self.load_prescriptions
        )

    def change_dosage_popup(self):
        selected = self.tree.focus()
        if not selected:
            show_messagebox("Info", "Select a medicine to change dosage.")
            return

        med_name = self.tree.item(selected)["values"][1]
        ChangeDosagePopup(
            parent=self.tab,
            selected_pid=self.selected_pid,
            med_name=med_name,
            db=self.db,
            refresh_callback=self.load_prescriptions
        )

    def delete_medicine(self):
        selected = self.tree.focus()
        if not selected:
            show_messagebox("Info", "Select a medicine to delete.")
            return

        med_name = self.tree.item(selected)["values"][0]
        confirm = CTkMessagebox(
            title="Confirm Delete",
            message=f"Delete {med_name} from this patient's record?",
            icon="warning",
            option_1="Yes", option_2="No"
        )

        if confirm.get() == "Yes":
            self.dosage_repo.delete_dosage(self.selected_pid, med_name)
            show_messagebox("Success", "Medicine deleted successfully.")
            self.load_prescriptions()
