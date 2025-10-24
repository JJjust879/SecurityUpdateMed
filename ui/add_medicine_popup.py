from customtkinter import (
    CTkToplevel, CTkLabel, CTkEntry, CTkFrame, 
    CTkButton, CTkComboBox, CTkCheckBox, StringVar
)
from tkcalendar import DateEntry
from db.dosage_repo import DosageRepo
from db.medicine_repo import MedicineRepo
from models.dosage import Dosage
from utils.helpers import show_messagebox

class AddMedicinePopup(CTkToplevel):
    def __init__(self, parent, selected_pid, db, refresh_callback):
        """
        parent: parent window (the tab or main window)
        selected_pid: patient ID to link the medicine to
        refresh_callback: function to refresh the prescription list after adding
        """
        super().__init__(parent)

        self.selected_pid = selected_pid
        self.dosage_repo = DosageRepo(db)
        self.medicine_repo = MedicineRepo(db)
        self.refresh_callback = refresh_callback

        self.title("Add New Prescription")
        self.geometry("450x450")

        self.setup_ui()

    # --- UI Setup ---
    def setup_ui(self):
        container = CTkFrame(self, fg_color="transparent")
        container.pack(padx=20, pady=15, fill="both", expand=True)
        container.columnconfigure(1, weight=1)

        # --- Illness ---
        CTkLabel(container, text="Illness:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.illness_entry = CTkEntry(container, width=200)
        self.illness_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        # --- Medicine name ---
        CTkLabel(container, text="Medicine Name:").grid(row=1, column=0, sticky="w", pady=5)
        self.med_box = CTkComboBox(
            container,
            width=220,
            values=self.medicine_repo.get_all_medicine_names(),
            state="readonly",
            command=self.on_medicine_selected
        )
        self.med_box.grid(row=1, column=1, pady=5)

        # --- Dosage (numeric + unit) ---
        CTkLabel(container, text="Dosage:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        dosage_frame = CTkFrame(container, fg_color="transparent")
        dosage_frame.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        self.dosage_entry = CTkEntry(dosage_frame, width=80, justify="center")
        self.dosage_entry.pack(side="left", padx=(0, 5))

        self.dtype_box = CTkComboBox(
            dosage_frame,
            width=100,
            values=["mg", "g", "mcg", "capsule", "tablet"],
            state="readonly"
        )
        self.dtype_box.set("mg")
        self.dtype_box.pack(side="left")

        # --- Times per ---
        CTkLabel(container, text="Times per:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.timesper_box = CTkComboBox(
            container,
            width=200,
            values=["Day", "Week"],
            state="readonly",
            command=self.on_timesper_change  # triggers toggle
        )
        self.timesper_box.set("Day")
        self.timesper_box.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        # --- Days of week checkboxes (hidden by default) ---
        self.days_frame = CTkFrame(container, fg_color="transparent")
        self.days_frame.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        self.days_frame.grid_remove()  # hide initially

        self.days_vars = {}
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        for i, day in enumerate(days):
            var = StringVar(value="0")
            chk = CTkCheckBox(self.days_frame, text=day, variable=var, onvalue="1", offvalue="0")
            chk.grid(row=i // 3, column=i % 3, padx=5, pady=3, sticky="w")
            self.days_vars[day] = var

        # --- Frequency ---
        CTkLabel(container, text="Frequency:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.frequency_entry = CTkEntry(container, width=200)
        self.frequency_entry.grid(row=5, column=1, sticky="w", padx=5, pady=5)

        # --- Time ---
        CTkLabel(container, text="Time:").grid(row=6, column=0, sticky="e", padx=5, pady=5)
        self.time_entry = CTkEntry(container, width=200)
        self.time_entry.grid(row=6, column=1, sticky="w", padx=5, pady=5)

        # --- Date ---
        CTkLabel(container, text="Date:").grid(row=7, column=0, sticky="e", padx=5, pady=5)
        self.date_picker = DateEntry(
            container,
            width=17,
            background="#6dc993",
            foreground="white",
            font=("Arial", 14),
            borderwidth=2,
            date_pattern="mm/dd/yyyy"
        )
        self.date_picker.grid(row=7, column=1, sticky="w", padx=5, pady=5)

        # --- Add button ---
        CTkButton(self, text="Add", fg_color="#6dc993", command=self.add_to_db).pack(pady=15)

    def on_medicine_selected(self, selected_med_name):
        """Auto-fill dosage info when a medicine is selected"""
        med_info = self.medicine_repo.get_medicine_by_name(selected_med_name)
        if med_info:
            default_dosage, default_dtype = med_info[2], med_info[5]

            self.dosage_entry.delete(0, "end")
            self.dosage_entry.insert(0, str(default_dosage))
            self.dtype_box.set(default_dtype)
    
    # --- Logic ---
    def on_timesper_change(self, value):
        """Show or hide the days of week checkboxes when 'Week' is selected."""
        if value == "Week":
            self.days_frame.grid()
        else:
            self.days_frame.grid_remove()

    def add_to_db(self):
        illness = self.illness_entry.get().strip()
        med = self.med_entry.get().strip()
        dosage = self.dosage_entry.get().strip()
        dosage_type = self.dtype_box.get().strip()
        times_per = self.timesper_box.get().strip()
        frequency = self.frequency_entry.get().strip()
        time = self.time_entry.get().strip()
        date = self.date_picker.get_date().strftime("%m/%d/%Y")

        if not all([illness, med, dosage, dosage_type, time, date]):
            show_messagebox("Error", "Please fill out all fields.")
            return

        if not dosage.isdigit():
            show_messagebox("Error", "Dosage must be a numeric value.")
            return
        
        dosage_range = self.medicine_repo.get_min_max_dosage(med)
        if not dosage_range:
            show_messagebox("Error", f"Medicine '{med}' not found in database.")
            return
        
        min_dosage, max_dosage = dosage_range
        dosage_value = float(dosage)
        if not (min_dosage <= dosage_value <= max_dosage):
            show_messagebox(
                "Error",
                f"Dosage for '{med}' must be between {min_dosage} and {max_dosage}."
            )
            return

        # Collect selected days if applicable
        if times_per == "Week":
            selected_days = [day for day, var in self.days_vars.items() if var.get() == "1"]
            days_str = " ".join(selected_days) if selected_days else "N/A"
        else:
            days_str = "N/A"

        new_dosage = Dosage(
            illness=illness,
            medication=med,
            dosage=dosage,
            dosage_type=dosage_type,
            times_per=times_per,
            days_of_week=days_str,
            frequency=frequency,
            time=time,
            date=date
        )

        self.dosage_repo.insert_dosage(self.selected_pid, new_dosage)
        show_messagebox("Success", f"{med} added successfully.")
        self.destroy()

        if callable(self.refresh_callback):
            self.refresh_callback()
