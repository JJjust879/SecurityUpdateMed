from customtkinter import CTkButton, CTkComboBox
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
from db.dosage_repo import DosageRepo
from db.patient_repo import PatientRepo
from ui.add_medicine_popup import AddMedicinePopup
from ui.change_dosage_popup import ChangeDosagePopup
from utils.helpers import show_messagebox

class PrescriptionTab:
    def __init__(self, tabview, db):
        self.db = db
        self.patient_repo = PatientRepo(db)
        self.dosage_repo = DosageRepo(db)
        self.tab = tabview.add("Medical Prescription")

        self.selected_pid = None
        self.setup_ui()
        self.load_patient_ids()

    # UI Setup
    def setup_ui(self):
        # Search patient section
        self.pid_entry = CTkComboBox(self.tab, width=150, font=("", 14))
        self.pid_entry.place(relx=0.03, rely=0.04)
        self.pid_entry.set("Select Patient ID")

        self.search_btn = CTkButton(
            self.tab, text="Search", text_color="#000000",
            hover_color="#FFFFFF", fg_color="#f5f3e6", width=60,
            command=self.load_prescriptions
        )
        self.search_btn.place(relx=0.26, rely=0.04)
        
        self.tree_columns = {
            "illness": ("Illness", 120),
            "medicine": ("Medicine Name", 140),
            "dosage": ("Dosage", 120),
            "times_per": ("Times per", 120),
            "daysoftheweek": ("Days of the Week", 180),
            "frequency": ("Frequency", 120),
            "date_time": ("Date Time", 180)
        }

        # Prescription list
        self.tree = ttk.Treeview(
            self.tab,
            columns=list(self.tree_columns.keys()),
            show="headings", height=15
        )
        
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("", 12, "bold"))
        style.configure("Treeview", font=("", 12))
        
        for col, (heading, width) in self.tree_columns.items():
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=width)
        self.tree.place(relx=0.03, rely=0.13)

        # Buttons for CRUD operations
        self.add_btn = CTkButton(
            self.tab, text="Add New", width=90, fg_color="#6dc993",
            command=self.add_medicine_popup
        )
        self.add_btn.place(relx=0.03, rely=0.65)

        self.edit_btn = CTkButton(
            self.tab, text="Change Dosage", width=90, fg_color="#e9c46a",
            command=self.change_dosage_popup
        )
        self.edit_btn.place(relx=0.18, rely=0.65)

        self.del_btn = CTkButton(
            self.tab, text="Delete", width=90, fg_color="#e76f51",
            command=self.delete_medicine
        )
        self.del_btn.place(relx=0.35, rely=0.65)

        self.refresh_btn = CTkButton(
            self.tab, text="Refresh", width=90, fg_color="#87CEEB",
            command=self.load_prescriptions
        )
        self.refresh_btn.place(relx=0.5, rely=0.65)
    
    # Data Operations
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
            dosage_repo=self.dosage_repo,
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
