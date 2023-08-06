import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkmb
import tkinter.filedialog as tkfd
from PIL import Image, ImageTk
import sys
import os
import json


man_dir = os.path.dirname(os.path.realpath(__file__))


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("pictureman")

        self.btn_open = ttk.Button(self, text="Open directory...", command=self.open_dir) 
        self.btn_keys = ttk.Button(self, text="0 keybinds set", command=self.manage_keys)

    def open_dir(self):
        initial = None
        pictures_dir = os.path.join(os.path.expanduser("~"), "Pictures")
        if os.path.isdir(pictures_dir):
            initial = pictures_dir

        self.current_dir = tkfd.askdirectory(initialdir=initial)



    def manage_keys(self):
        key_manager = KeyManager(self)
        key_manager.mainloop()



class KeyManager(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("key manager")

        self.btn_import = ttk.Button(self, text="Import", command=self.import_keys)
        self.btn_export = ttk.Button(self, text="Export", command=self.export_keys)
        self.btn_apply = ttk.Button(self, text="Apply", command=self.apply)
        self.btn_add = ttk.Button(self, text="Add key", command=self.add_key)

        self.lb_key = ttk.Label(self, text="key")
        self.lb_path = ttk.Label(self, text="directory path...")
        
        self.frame_keys = ttk.Frame(self, border=2)
        first_key_entry = KeyEntry(self.frame_keys)

    def import_keys(self):
        f = tkfd.askopenfile(mode="r", filetypes=[("JSON Files", "*.json")])
        if f is None:
            tkmb.showerror("error", "invalid file!")
        else:
            bindings = json.load(f)
            

    def apply(self):
        bindings = {}
        for key_entry in self.frame_keys:
            key = key_entry.box_key.get()
            path = key_entry.box_path.get()

            error = False

            if (not key) or (key not in VALID_KEYS) or (key in bindings):
                key_entry.box_key.configure(bg="red")
                error = True
            if (not path) or (not os.path.isdir(path)):
                key_entry.box_path.configure(bg="red")
                error = True

            if not error:
                bindings[key] = path

        self.parent.new_bindings = bindings


class KeyEntry(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.box_key = ttk.Entry(self, width=3)
        self.box_path = ttk.Entry(self, width=20)

        self.btn_open = ttk.Entry(self, text="open", command=self.open_dir)
        self.btn_delete = ttk.Entry(self, text="x", command=self.delete)