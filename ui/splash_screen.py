import customtkinter
import os
from PIL import Image

class SplashScreen(customtkinter.CTkToplevel):
    def __init__(self, parent, on_close_callback=None, duration=2000):
        super().__init__(parent)
        self.parent = parent
        self.on_close_callback = on_close_callback
        self.duration = duration

        # --- Window setup ---
        self.overrideredirect(True)  # remove title bar
        self.configure(fg_color="#ffffff")
        self.title("VitalCare Medical Center")

        AppWidth, AppHeight = 650, 550
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (AppWidth // 2)
        y = (screen_height // 2) - (AppHeight // 2)
        self.geometry(f"{AppWidth}x{AppHeight}+{x}+{y}")

        # --- Icon setup ---
        icon_path = os.path.join(os.getcwd(), "Images", "transparent.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

        # --- Image setup ---
        image_path = os.path.join(os.getcwd(), "Images", "Hospital.png")
        if os.path.exists(image_path):
            splash_img = customtkinter.CTkImage(
                dark_image=Image.open(image_path), size=(AppWidth, AppHeight)
            )
            splash_label = customtkinter.CTkLabel(self, image=splash_img, text="")
            splash_label.place(relx=0, rely=0)

        # --- Schedule closing ---
        self.after(self.duration, self._close_splash)

    def _close_splash(self):
        """Safely close splash and trigger callback."""
        try:
            self.withdraw()
            self.update_idletasks()
        except Exception:
            pass # nosec B110

        if self.on_close_callback:
            self.after(200, self.on_close_callback)  # delay slightly for safety

        # finally destroy splash after callback triggered
        self.after(500, self.destroy)