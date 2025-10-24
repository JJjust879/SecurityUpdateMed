import os
from PIL import Image
import customtkinter
from CTkMessagebox import CTkMessagebox

def show_messagebox(title, message):
    CTkMessagebox(title=title, message=message)

def load_image(path, size=(100, 100)):
    if not os.path.exists(path):
        path = os.path.join(os.getcwd(), "Images/defaultprofile.png")
    return customtkinter.CTkImage(dark_image=Image.open(path), size=size)
