from customtkinter import CTkButton, CTkComboBox, CTkLabel, CTkFrame
from db.patient_repo import PatientRepo
from models.patient import Patient
from utils.helpers import load_image, show_messagebox


class PatientProfileTab:
    def __init__(self, tabview, db):
        self.patient_repo = PatientRepo(db)
        self.tab = tabview.add("Patient Profile")
        self.setup_ui()
        self.load_patient_ids()

    def setup_ui(self):
        # Search bar
        self.findp = CTkComboBox(self.tab, width=160, font=("", 16))
        self.findp.place(relx=0.01, rely=0.035)
        self.findp.set("Select Patient ID")
        
        self.searchp = CTkButton(
            self.tab, text="Search", text_color="#000000",
            hover_color="#FFFFFF", fg_color='#f5f3e6', width=50,
            command=self.show_patient_profile
        )
        self.searchp.place(relx=0.245, rely=0.035)

        # Frame for profile
        self.frame = CTkFrame(
            self.tab, fg_color="#ffffff", height=430, width=400
        )
        self.frame.place(relx=0.01, rely=0.13)

        self.pp_label = CTkLabel(self.frame, text="")
        self.pp_label.place(relx=0.20, rely=0.04)
        
        self.label_info = {
            "name": ("Name", 0.35),
            "age": ("Age", 0.45),
            "gender": ("Gender", 0.55),
            "bday": ("Birthday", 0.65),
            "address": ("Address", 0.75),
            "cno": ("Cel.No#", 0.85)
        }

        self.labels = {}
        for key, (label_text, rel_y) in self.label_info.items():
            label = CTkLabel(
                self.frame,
                text=f"{label_text}:",
                text_color="#000000",
            )
            label.place(relx=0.10, rely=rel_y)
            self.labels[key] = label

    def load_patient_ids(self):
        patient_ids = self.patient_repo.get_all_patient_ids()
        self.findp.configure(values=patient_ids)
        
    def _update_label(self, key, value):
        """Update a label safely if it exists."""
        if key in self.labels:
            display_name = self.label_info[key][0]
            self.labels[key].configure(text=f"{display_name}: {value if value else 'N/A'}")

    def show_patient_profile(self):
        pid = self.findp.get()
        if not pid:
            show_messagebox("Info", "No Data Found\nPlease Check Your ID")
            return

        patient_info: Patient | None = self.patient_repo.get_patient_profile(pid.upper())
        if not patient_info:
            show_messagebox("Info", "No Data Found\nPlease Check Your ID")
            return
        
        image_path = f"Images\\{'female' if patient_info.gender == 'Female' else 'male'}.png"
        self.pp_label.configure(image=load_image(image_path, size=(120, 120)))

        # Dynamically update all text labels
        data_map = {
            "name": patient_info.name,
            "age": patient_info.age,
            "gender": patient_info.gender,
            "bday": patient_info.birthdate,
            "address": patient_info.address,
            "cno": patient_info.cellphone_num,
        }

        for key, value in data_map.items():
            self._update_label(key, value)
