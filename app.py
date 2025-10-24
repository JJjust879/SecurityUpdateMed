import customtkinter
from db.db_manager import DatabaseManager
from ui.patient_tab import PatientProfileTab
from ui.prescription_tab import PrescriptionTab

class VitalCareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VitalCare Medical Center")
        self.root.configure(fg_color="#87CEEB")
        self.root.iconbitmap("Images/transparent.ico")
        self.root.resizable(False, False)

        app_width, app_height = 750, 550
        screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
        x, y = (screen_width / 2) - (app_width / 2), (screen_height / 2) - (app_height / 2)
        self.root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

        # Initialize Database
        self.db = DatabaseManager("db.db")

        # Setup Tab View
        self.tabview = customtkinter.CTkTabview(
            self.root, height=550, width=750, fg_color="#87CEEB"
        )
        self.tabview.pack(padx=10, pady=5)

        # Tabs
        self.patient_tab = PatientProfileTab(self.tabview, self.db)
        self.prescription_tab = PrescriptionTab(self.tabview, self.db)
