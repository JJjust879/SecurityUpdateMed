import customtkinter
from db.db_manager import DatabaseManager
from ui.patient_tab import PatientProfileTab
from ui.prescription_tab import PrescriptionTab
from ui.auth_frame import AuthFrame
from ui.log_viewer_tab import LogViewerTab


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

        # --- Initialize Login Page ---
        self.auth_frame = AuthFrame(self.root, self.db, self.show_main_app)
        self.auth_frame.pack(fill="both", expand=True)

        # Main app (hidden initially)
        self.tabview = None

    def show_main_app(self, username, role):
        """
        Switch from the auth screen to the main UI.
        RBAC: always show Patient/Prescription tabs; show Security Logs only for admin.
        """
        # Remember who is logged in and what their role is
        self.current_user = username
        self.current_role = role

        # Hide the login/register frame
        self.auth_frame.pack_forget()

        # Create the main tab view container
        self.tabview = customtkinter.CTkTabview(
            self.root, height=550, width=750, fg_color="#87CEEB"
        )
        self.tabview.pack(padx=10, pady=5)

        # --- Tabs that everyone (staff + admin) can use ---
        # These classes are already written to add their own tabs inside the tabview
        self.patient_tab = PatientProfileTab(self.tabview, self.db)
        self.prescription_tab = PrescriptionTab(self.tabview, self.db)

        # --- Admin-only tab (RBAC) ---
        # Only create and mount the Security Logs tab if this user is an admin.
        if self.current_role == "admin":
            # Make a new tab named "Security Logs"
            self.tabview.add("Security Logs")

            # Put our LogViewer frame inside that tab
            self.log_viewer = LogViewerTab(self.tabview.tab("Security Logs"))
            self.log_viewer.pack(fill="both", expand=True, padx=10, pady=10)

