import customtkinter
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
from db.dosage_repo import DosageRepo
from db.patient_repo import PatientRepo
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
        self.pid_entry = customtkinter.CTkComboBox(self.tab, width=150, font=("", 14))
        self.pid_entry.place(relx=0.03, rely=0.04)
        self.pid_entry.set("Select Patient ID")

        self.search_btn = customtkinter.CTkButton(
            self.tab, text="Search", text_color="#000000",
            hover_color="#FFFFFF", fg_color="#f5f3e6", width=60,
            command=self.load_prescriptions
        )
        self.search_btn.place(relx=0.26, rely=0.04)

        # Prescription list
        self.tree = ttk.Treeview(
            self.tab,
            columns=("illness", "medicine", "dosage", "times_per",
                     "daysoftheweek", "frequency", "date_time"),
            show="headings", height=15
        )
        self.tree.heading("illness", text="Illness")
        self.tree.heading("medicine", text="Medicine Name")
        self.tree.heading("dosage", text="Dosage")
        self.tree.heading("times_per", text="Times per")
        self.tree.heading("daysoftheweek", text="Days of the Week")
        self.tree.heading("frequency", text="Frequency")
        self.tree.heading("date_time", text="Date Time")

        self.tree.column("illness", width=100)
        self.tree.column("medicine", width=100)
        self.tree.column("dosage", width=80)
        self.tree.column("times_per", width=80)
        self.tree.column("daysoftheweek", width=120)
        self.tree.column("frequency", width=80)
        self.tree.column("date_time", width=150)
        self.tree.place(relx=0.03, rely=0.13)

        # Buttons for CRUD operations
        self.add_btn = customtkinter.CTkButton(
            self.tab, text="Add New", width=90, fg_color="#6dc993",
            command=self.add_medicine_popup
        )
        self.add_btn.place(relx=0.03, rely=0.65)

        self.edit_btn = customtkinter.CTkButton(
            self.tab, text="Change Dosage", width=90, fg_color="#e9c46a",
            command=self.change_dosage_popup
        )
        self.edit_btn.place(relx=0.18, rely=0.65)

        self.del_btn = customtkinter.CTkButton(
            self.tab, text="Delete", width=90, fg_color="#e76f51",
            command=self.delete_medicine
        )
        self.del_btn.place(relx=0.35, rely=0.65)

        self.refresh_btn = customtkinter.CTkButton(
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

    # Popups for ADD and EDIT
    def add_medicine_popup(self):
        if not self.selected_pid:
            show_messagebox("Info", "Please load a patient first.")
            return

        popup = customtkinter.CTkToplevel()
        popup.title("Add New Medicine")
        popup.geometry("350x400")

        customtkinter.CTkLabel(popup, text="Medicine Name:").pack(pady=5)
        med_entry = customtkinter.CTkEntry(popup, width=80)
        med_entry.pack()

        customtkinter.CTkLabel(popup, text="Dosage:").pack(pady=5)
        dosage_entry = customtkinter.CTkEntry(popup, width=200)
        dosage_entry.pack()

        customtkinter.CTkLabel(popup, text="Dosage Type (e.g., mg):").pack(pady=5)
        dtype_entry = customtkinter.CTkEntry(popup, width=200)
        dtype_entry.pack()

        customtkinter.CTkLabel(popup, text="Time:").pack(pady=5)
        time_entry = customtkinter.CTkEntry(popup, width=200)
        time_entry.pack()

        customtkinter.CTkLabel(popup, text="Date:").pack(pady=5)
        date_entry = customtkinter.CTkEntry(popup, width=200)
        date_entry.pack()

        def add_to_db():
            med = med_entry.get().strip()
            dosage = dosage_entry.get().strip()
            dtype = dtype_entry.get().strip()
            time = time_entry.get().strip()
            date = date_entry.get().strip()

            if not all([med, dosage, dtype, time, date]):
                show_messagebox("Error", "Please fill out all fields.")
                return
            
            self.dosage_repo.insert_dosage(
                self.selected_pid, med, dosage, dtype, time, date
            )

            show_messagebox("Success", f"{med} added successfully.")
            popup.destroy()
            self.load_prescriptions()

        customtkinter.CTkButton(popup, text="Add",
                                fg_color="#6dc993", command=add_to_db).pack(pady=10)

    def change_dosage_popup(self):
        selected = self.tree.focus()
        if not selected:
            show_messagebox("Info", "Select a medicine to change dosage.")
            return

        med_name = self.tree.item(selected)["values"][0]

        popup = customtkinter.CTkToplevel()
        popup.title("Change Dosage")
        popup.geometry("300x200")

        customtkinter.CTkLabel(popup, text=f"Medicine: {med_name}").pack(pady=10)
        customtkinter.CTkLabel(popup, text="New Dosage (e.g., 500 mg):").pack()
        dosage_entry = customtkinter.CTkEntry(popup, width=200)
        dosage_entry.pack()

        def update_dosage():
            new_dosage_text = dosage_entry.get().strip()
            if not new_dosage_text:
                show_messagebox("Error", "Dosage cannot be empty.")
                return

            # Split "500 mg" into dosage and dosagetype if possible
            parts = new_dosage_text.split()
            dosage = parts[0]
            dtype = parts[1] if len(parts) > 1 else "mg"

            self.dosage_repo.update_dosage(
                self.selected_pid, med_name, dosage, dtype
            )
            show_messagebox("Success", "Dosage updated successfully.")
            popup.destroy()
            self.load_prescriptions()

        customtkinter.CTkButton(popup, text="Update", fg_color="#e9c46a",
                                command=update_dosage).pack(pady=10)

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
            self.db.execute(
                "DELETE FROM patient_dosage WHERE patientid = ? AND medicine = ?",
                (self.selected_pid, med_name)
            )
            show_messagebox("Success", "Medicine deleted successfully.")
            self.load_prescriptions()
