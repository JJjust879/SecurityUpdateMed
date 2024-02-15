import os

from customtkinter import *
from subprocess import call
from PIL import Image


splash = CTk(fg_color="#ffffff")
iconfilepath = r'Images\transparent.ico'
iconfullpath = os.path.join(os.getcwd(), iconfilepath)
splash.iconbitmap(iconfullpath)
splash.title("VitalCare Medical Center")

AppWidth = 650
AppHeight = 550

ScreenWidth = splash.winfo_screenwidth()
ScreenHeight = splash.winfo_screenheight()

x = (ScreenWidth / 2) - (AppWidth / 2)
y = (ScreenHeight / 2) - (AppHeight / 2)

splash.geometry(f'{AppWidth}x{AppHeight}+{int(x)}+{int(y)}')

pfilepath = r"Images\Hospital.png"
pfullpath = os.path.join(os.getcwd(), pfilepath)
pp = CTkImage(dark_image=Image.open(pfullpath), size=(650, 550))  # profile picture
pp_label = CTkLabel(splash, image=pp, text=" ")
pp_label.place(relx=0.0, rely=0.0)

def MainWindow():

    splash.destroy()
    call(["python", "main.py"])

splash.after(2000, MainWindow)

splash.mainloop()

