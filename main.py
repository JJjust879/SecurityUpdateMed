from ui.splash_screen import SplashScreen
import customtkinter
from app import VitalCareApp
        
def start_main_app(root):
    """Initialize and show the main application window."""
    root.deiconify()  # show the main app window
    VitalCareApp(root)

def main():
    root = customtkinter.CTk()
    root.withdraw()  # hide until splash finishes

    # Create splash screen (child of root)
    SplashScreen(root, on_close_callback=lambda: start_main_app(root), duration=2000)

    # Start the event loop
    root.mainloop()

if __name__ == "__main__":
    main()