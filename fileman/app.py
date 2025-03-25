import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkmb
import tkinter.filedialog as tkfd
from PIL import Image, ImageTk, ImageOps
import pillow_heif

from setup import log
from constants import VERSION
from frames import MenuFrame, ViewerFrame

log("Initializing application...")

# define app
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.minsize(500, 500)
        self.title(f"FileMan v{VERSION}")

        self.style = ttk.Style()
        self.style.configure("Viewer.TFrame", background="lightblue")
        self.style.configure("Viewer.TLabel", background="lightblue")
        self.style.configure("KeyNormal.TEntry", background="white")
        self.style.configure("KeyActive.TEntry", background="red")

        menu = MenuFrame(self)
        viewer = ViewerFrame(self)

        menu.pack(side="left", padx=10)
        viewer.pack(side="right", padx=10, pady=10, expand=1)
        