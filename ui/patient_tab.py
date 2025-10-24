import customtkinter
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
        self.findp = customtkinter.CTkComboBox(self.tab, width=160, font=("", 16))
        self.findp.place(relx=0.01, rely=0.035)
        self.findp.set("Select Patient ID")
        
        self.searchp = customtkinter.CTkButton(
            self.tab, text="Search", text_color="#000000",
            hover_color="#FFFFFF", fg_color='#f5f3e6', width=50,
            command=self.show_patient_profile
        )
        self.searchp.place(relx=0.245, rely=0.035)

        # Frame for profile
        self.frame = customtkinter.CTkFrame(
            self.tab, fg_color="#ffffff", height=430, width=580
        )
        self.frame.place(relx=0.01, rely=0.13)

        self.pp_label = customtkinter.CTkLabel(self.frame, text="")
        self.pp_label.place(relx=0.20, rely=0.04)

        self.labels = {
            "name": customtkinter.CTkLabel(self.frame, text="Name:", text_color="#000000"),
            "age": customtkinter.CTkLabel(self.frame, text="Age:", text_color="#000000"),
            "gender": customtkinter.CTkLabel(self.frame, text="Gender:", text_color="#000000"),
            "bday": customtkinter.CTkLabel(self.frame, text="Birthday:", text_color="#000000"),
            "address": customtkinter.CTkLabel(self.frame, text="Address:", text_color="#000000"),
            "cno": customtkinter.CTkLabel(self.frame, text="Cel.No#:", text_color="#000000"),
        }

        positions = [0.35, 0.45, 0.55, 0.65, 0.75, 0.9]
        for label, rel_y in zip(self.labels.values(), positions):
            label.place(relx=0.10, rely=rel_y)

    def load_patient_ids(self):
        patient_ids = self.patient_repo.get_all_patient_ids()
        self.findp.configure(values=patient_ids)

    def show_patient_profile(self):
        pid = self.findp.get()
        if not pid:
            show_messagebox("Info", "No Data Found\nPlease Check Your ID")
            return

        patient_info: Patient | None = self.patient_repo.get_patient_profile(pid.upper())
        if not patient_info:
            show_messagebox("Info", "No Data Found\nPlease Check Your ID")
            return

        # Update UI
        image_path = f"Images\\{'female' if patient_info.gender == "Female" else "male"}.png"
        self.pp_label.configure(image=load_image(image_path, size=(120, 120)))
        self.labels["name"].configure(text=f"Name: {patient_info.name}")
        self.labels["age"].configure(text=f"Age: {patient_info.age}")
        self.labels["bday"].configure(text=f"Birthday: {patient_info.birthdate}")
        self.labels["gender"].configure(text=f"Gender: {patient_info.gender}")
        self.labels["address"].configure(text=f"Address: {patient_info.address}")
        self.labels["cno"].configure(text=f"Cel.No #: {patient_info.cellphone_num}")
