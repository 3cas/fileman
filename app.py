import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkmb
import tkinter.filedialog as tkfd
import ttkbootstrap as tbs
from PIL import Image, ImageTk, ImageOps
import pillow_heif
import sys
import os
import json
import random


AUTO_OPEN = os.path.join("/home/cas/Pictures/photos/iPhone/MacImports", "mod_2019")
AUTO_KEYS = "main.json"
EXTRA_INFO = False

man_dir = os.path.dirname(__file__)

pillow_heif.register_heif_opener()

VALID_KEYS = "abcdefghijklmnopqrstuvwxyz"
IMAGE_EXTS = ["png", "jpg", "jpeg", "heic", "heif", "webp", "gif"]
BASE = "$BASE_DIR"
LOGFILE = "latest.log"

INFO_BUILTINS = """
Built-in Keybinds

Shift+Z = undo move
Shift+U = Update
Shift+R = Rename
Left Arrow = back
Right Arrow = next
"""

INFO_KEYHELP = """
How to set keybinds

Keybinds can be set as absolute paths or relative paths. If a base path is set, all relative keybinds will extend from that base path. If the base path is relative, or if there is no base path, all relative paths will be relative to the Pictures directory, or if not present, the directory this program is run from.

The Open button always sets an absolute path to what you select. Importing and Exporting stores keybinds and base directory info in JSON format.
"""

ideal_p_dir = os.path.join(os.path.expanduser("~"), "Pictures")
if os.path.isdir(ideal_p_dir):
    PICTURES_DIR = ideal_p_dir
else:
    PICTURES_DIR = None


def set_box(box: ttk.Entry|tk.Entry, text: str):
    box.delete(0, tk.END)
    box.insert(0, text)

def log(message: str):
    if LOGFILE:
        with open(LOGFILE, "a") as f:
            f.write(message)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # VARS

        self.keybinds = {}
        self.dir = None

        self.base_dir = self.keybinds.get(BASE, None)

        self.actions = []

        self.open_dir(AUTO_OPEN, init=True)
        self.filename = self.files[self.index]

        #self.import_keys("main.json", init=True)

        # TK

        self.minsize(500, 500)
        self.title("pictureman")

        self.style = ttk.Style()
        #self.style = tbs.Style(theme="litera")
        self.style.configure("Viewer.TFrame", background="lightblue")
        self.style.configure("Viewer.TLabel", background="lightblue")
        self.style.configure("KeyNormal.TEntry", background="white")
        self.style.configure("KeyActive.TEntry", background="red")
        
        menu = ttk.Frame(self)
        viewer = ttk.Frame(self, style="Viewer.TFrame", borderwidth=5, relief="sunken")
        keys = ttk.Frame(self)

        # MENU FRAME

        frame_builtins = ttk.Frame(menu, borderwidth=5, relief="raised")

        lb_welc = ttk.Label(menu, text="Welcome to PictureMan.")
        lb_sort = ttk.Label(menu, text="Sort:")
        self.lb_keys = ttk.Label(menu, text="0 directory keybinds")
        lb_builtins = ttk.Label(frame_builtins, text=INFO_BUILTINS, justify="center")

        btn_open = ttk.Button(menu, text="Open", width=6, command=self.open_dir) 
        btn_exit = ttk.Button(menu, text="Exit PictureMan", command=(lambda: sys.exit(0)))

        self.sort = tk.StringVar()

        opt_sort = ttk.OptionMenu(menu, self.sort, "alphabetical", "os default", "alphabetical", "random")

        lb_builtins.pack(padx=20)

        lb_welc.grid(row=1, column=1, columnspan=3, padx=20, pady=(30, 10))
        lb_sort.grid(row=2, column=1)
        opt_sort.grid(row=2, column=2)
        btn_open.grid(row=2, column=3)
        self.lb_keys.grid(row=3, column=1, columnspan=3)
        frame_builtins.grid(row=4, column=1, columnspan=3, pady=5)
        btn_exit.grid(row=5, column=1, columnspan=3, pady=(0, 30))

        # VIEWER FRAME

        self.lb_file = ttk.Label(viewer, text="<filename>", style="Viewer.TLabel")
        self.lb_data = ttk.Label(viewer, text="<data>", style="Viewer.TLabel")
        self.lb_img = ttk.Label(viewer)

        self.lb_file.pack(padx=30, pady=(30, 5))
        self.lb_data.pack(pady=(5, 10))
        self.lb_img.pack(pady=(0, 30))

        # KEYS FRAME

        frame_info = ttk.Frame(keys)
        frame_io = ttk.Frame(keys)
        frame_binds = ttk.Frame(keys)
        frame_aa = ttk.Frame(keys)

        lb_dirkeys = ttk.Label(frame_info, text="Directory Keybinds")
        btn_keyhelp = ttk.Button(frame_info, text="?", width=1, command=self.key_help)

        btn_import = ttk.Button(frame_io, text="Import", command=self.import_keys)
        btn_export = ttk.Button(frame_io, text="Export", command=self.export_keys)

        btn_add = ttk.Button(frame_aa, text="Add key", command=self.add_key)
        btn_apply = ttk.Button(frame_aa, text="Apply", command=self.apply)

        btn_base = ttk.Button(frame_binds, text="Set", command=self.open_base, width=3)

        lb_base = ttk.Label(frame_binds, text="Base directory:")
        lb_key = ttk.Label(frame_binds, text="Key")
        lb_path = ttk.Label(frame_binds, text="Directory")

        self.box_base = ttk.Entry(frame_binds)

        self.frame_keys = ttk.Frame(frame_binds, border=2)
        first_key_entry = KeyBind(self.frame_keys)

        first_key_entry.pack()

        lb_dirkeys.grid(row=1, column=2, padx=10)
        btn_keyhelp.grid(row=1, column=3, padx=(30, 0))

        btn_import.pack(side="left")
        btn_export.pack(side="left")

        btn_add.pack(side="left")
        btn_apply.pack(side="left")

        lb_base.grid(row=1, column=1, columnspan=2)
        self.box_base.grid(row=1, column=3)
        btn_base.grid(row=1, column=4)
        lb_key.grid(row=2, column=2)
        lb_path.grid(row=2, column=3)
        self.frame_keys.grid(row=3, column=1, columnspan=4)

        frame_info.pack()
        frame_io.pack(pady=10)
        frame_binds.pack()
        frame_aa.pack(pady=10)
        
        self.bind("<KeyRelease>", self.move_file)

        self.update_labels()

        menu.pack(side="left", padx=10)
        viewer.pack(side="left", padx=10, pady=10, expand=1, )
        keys.pack(side="left", padx=10)

    def open_dir(self, path: str = None, *, init: bool = False):
        if not path:
            path = tkfd.askdirectory(initialdir=PICTURES_DIR)

        if not init:
            sort = self.sort.get()
        else:
            sort = "alphabetical"

        if os.path.isdir(path):
            files = []
            for filename in os.listdir(path):
                if "." in filename:
                    if filename.rsplit(".", 1)[1].lower() in IMAGE_EXTS and os.path.isfile(os.path.join(path, filename)):
                        files.append(filename)

            if files:
                self.dir = path

                if sort == "alphabetical":
                    files = sorted(files)
                elif sort == "random":
                    random.shuffle(files)

                self.load_files(files)

            else:
                tkmb.showerror("No Files", f"Directory '{path}' has no images in it!", parent=self)
        
        else:
            tkmb.showerror("Error", f"Directory '{path}' does not exist!", parent=self)

    def load_files(self, files: list):
        self.files = files
        self.index = 0

    def update_labels(self):
        if self.index >= len(self.files):
            self.index = len(self.files) - 1

        if len(self.files) == 0:
            tkmb.showinfo("Done", "All files in that directory have been moved!")
            return

        self.filename = self.files[self.index]

        win_size = self.winfo_width(), self.winfo_height()

        if win_size == (1, 1):
            win_size = (500, 500)
        
        win_width, win_height = win_size
        max_width, max_height = win_width - 100, win_height - 150

        file_path = os.path.join(self.dir, self.filename)
        img_og = Image.open(file_path)
        img_og = ImageOps.exif_transpose(img_og)
        og_width, og_height = img_og.size
        resize_ratio = min(max_width/og_width, max_height/og_height)
        new_size = (int(og_width * resize_ratio), int(og_height * resize_ratio))
        img_resized = img_og.resize(new_size, resample=True)
        self.img_tk = ImageTk.PhotoImage(img_resized)

        self.lb_file.configure(text=self.filename)
        self.lb_data.configure(text=f"{self.index + 1} of {len(self.files)} - {new_size[0]}x{new_size[1]}")
        self.lb_img.configure(image=self.img_tk)

    def move_file(self, event: tk.Event):
        key = event.keysym

        if key in ["Left", "Right", "U", "R", "Z", "Y", "T"] or key in VALID_KEYS:
            if key == "Left":
                self.index -= 1
                if self.index < 0:
                    self.index = len(self.files) - 1

            elif key == "Right":
                self.index += 1
                if self.index > (len(self.files) - 1):
                    self.index = 0

            elif key == "Z":
                last = old_path, new_path = self.actions[-1]
                os.rename(new_path, old_path)

                log(f"\n{new_path} -> {old_path}")

                self.actions.remove(last)

                head, old_name = os.path.split(old_path)
                self.files.insert(self.index, old_name)

            elif key == "Y":
                tkmb.showwarning("Nope", "Redo not yet implemented")

            elif key == "R":
                filename = self.files[self.index]
                renamer = Renamer(self, filename, self.dir)
                new_name = renamer.run()
                
                if new_name:
                    self.files[self.index] = new_name

            elif key == "T":
                tkmb.showwarning("Nope", "Rotate not yet implemented")

            else:
                dir_path = self.keybinds.get(key)
                if dir_path:
                    filename = self.files[self.index]
                    cur_path = os.path.join(self.dir, filename)

                    if self.base_dir and not os.path.isabs(dir_path):
                        dir_path = os.path.join(self.base_dir, dir_path)
                    
                    if os.path.isdir(dir_path):
                        new_path = os.path.join(dir_path, filename)

                        self.actions.append((cur_path, new_path))

                        if LOGFILE:
                            with open(LOGFILE, "a") as f:
                                f.write(f"\n{cur_path} -> {new_path}")

                        os.rename(cur_path, new_path)
                        self.files.remove(filename)

                        keybind_frame = self.frame_keys.bind_frames.get(key)

                        def reset_flash():
                            keybind_frame.box_key.configure(style="KeyNormal.TEntry")
                            keybind_frame.box_path.configure(style="KeyNormal.TEntry")

                        keybind_frame.box_key.configure(style="KeyActive.TEntry")
                        keybind_frame.box_path.configure(style="KeyActive.TEntry")
                        self.update()

                        #self.after(250, reset_flash)
                        self.update()

                    else:
                        tkmb.showerror("Error", f"Directory {dir_path} does not exist!", parent=self)

            self.update_labels()

    def get_keybinds(self):
        keybinds = {}
        errors = []
        lookup = {}

        base_dir = self.box_base.get()
        if base_dir:
            if not os.path.isdir(base_dir):
                tkmb.showerror("Invalid", "Invalid base dir. The base dir is optional, but if provided, relative paths are attached to it.", parent=self)
                return
            
            keybinds[BASE] = base_dir
            
        else:
            base_dir = None

        for i, keybind in enumerate(self.frame_keys.winfo_children()):
            slot = i + 1
            key = keybind.box_key.get()
            path_val = keybind.box_path.get()

            if base_dir and not os.path.isabs(path_val):
                path = os.path.join(base_dir, path_val)
            else:
                path = path_val

            error = False

            if (not key) or (key.lower() not in VALID_KEYS) or (key in keybinds):
                keybind.box_key.configure(background="red")
                error = True

                if not key:
                    errors.append(f"Missing key in slot #{slot}")
                elif key.lower() not in VALID_KEYS:
                    errors.append(f"Invalid key '{key}'")
                elif key in keybinds:
                    errors.append(f"Duplicate key {key} in slot #{slot}")\
                    
            if key not in VALID_KEYS and key.lower() in VALID_KEYS:
                key = key.lower()
                set_box(keybind.box_key, key)

            if (not path) or (not os.path.join):
                keybind.box_path.configure(background="red")
                error = True

            if not path:
                errors.append(f"Missing path in slot #{slot}")

            if not error:
                keybinds[key] = path_val
                lookup[key] = keybind

        return keybinds, errors, lookup

    def import_keys(self, load_file: str = None, *, init: bool = False):
        if not load_file:
            load_file = tkfd.askopenfilename(filetypes=[("JSON Files", "*.json")])

        with open(load_file, "r") as f:
            try:
                keybinds = json.load(f)
            except:
                tkmb.showerror("error", "invalid file!", parent=self) 
        
        count = len(keybinds)
        if BASE in keybinds: count -= 1
        cont = tkmb.askokcancel("Continue?", f"You are about to import {count} keybinds and overwrite your current set. Do you wish to continue?", parent=self)

        if cont:
            for widget in self.frame_keys.winfo_children():
                if isinstance(widget, KeyBind):
                    widget.destroy()
        
            for key in keybinds:
                if key == BASE:
                    set_box(self.box_base, keybinds[key])
                    continue

                keybind = KeyBind(self.frame_keys)
                set_box(keybind.box_key, key)
                set_box(keybind.box_path, keybinds[key])
                keybind.pack()

            self.apply()

    def export_keys(self):
        keybinds, errors = self.get_keybinds()

        with tkfd.asksaveasfile("w", confirmoverwrite=True, filetypes=[("JSON files", "*.json")]) as f:
            json.dump(keybinds, f, indent=4)
    
    def add_key(self):
        new_bind = KeyBind(self.frame_keys)
        new_bind.pack()

    def apply(self):
        keybinds, errors, bind_frames = self.get_keybinds()

        if errors:
            message = f"{len(errors)} error(s):"
            for error in errors:
                message += f"\n - {error}"
            tkmb.showwarning("Error", message, parent=self)

        self.keybinds = keybinds
        count = len(keybinds)
        if BASE in keybinds: count -= 1
        self.lb_keys.configure(text=f"{count} keybinds set")

        if EXTRA_INFO:
            keybinds_message = "Set the following keybind(s):"
            for key in keybinds:
                if key == BASE:
                    continue
                keybinds_message += f"\n - {key} : {keybinds[key]}"

            tkmb.showinfo("keybinds Set!", keybinds_message, parent=self)

        if BASE in self.keybinds:
            self.base_dir = self.keybinds[BASE]

        self.frame_keys.bind_frames = bind_frames

    def open_base(self):
        initial = getattr(self, "dir") or PICTURES_DIR
        path = tkfd.askdirectory(initialdir=initial)
        set_box(self.box_base, path) 

    def key_help(self):
        tkmb.showinfo("Information", INFO_KEYHELP)
        

class Renamer(tk.Toplevel):
    def __init__(self, master, filename: str, dir_path: str):
        super().__init__(master)

        self.dir_path = dir_path
        self.filename = filename
        self.ext = self.filename.rsplit(".", 1)[1]

        self.title("Rename")

        lb_rename = ttk.Label(self, text=f"Rename {filename} to:")
        lb_ext = ttk.Label(self, text=f".{self.ext}")

        self.box_rename = ttk.Entry(self)

        btn_rename = ttk.Button(self, text="Rename", command=self.rename)
        btn_cancel = ttk.Button(self, text="Cancel", command=self.destroy)

        lb_rename.grid(row=1, column=1, columnspan=2, padx=20, pady=(20, 0))
        self.box_rename.grid(row=2, column=1, pady=5)
        lb_ext.grid(row=2, column=2, pady=5)
        btn_rename.grid(row=3, column=1, pady=(0, 20))
        btn_cancel.grid(row=3, column=2, pady=(0, 20))
        
        self.bind("<Enter>", self.rename)
        self.box_rename.focus_set()

    def rename(self, *args):
        new_name = self.box_rename.get()
        if new_name:
            self.new_name = new_name + "." + self.ext

            old_path = os.path.join(self.dir_path, self.filename)
            new_path = os.path.join(self.dir_path, self.new_name)

            print(old_path)
            print(new_path)
            print(os.path.isfile(old_path))

            os.rename(old_path, new_path)
            log(f"\n{old_path} -> {new_path}")

    def run(self):
        self.wait_window()
        if hasattr(self, "new_name") and self.new_name:
            return self.new_name
        

class KeyBind(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.box_key = ttk.Entry(self, width=3, style="KeyNormal.TEntry")
        self.box_path = ttk.Entry(self, width=20, style="KeyNormal.TEntry")

        btn_open = ttk.Button(self, text="Set", command=self.open_dir, width=3)
        btn_delete = ttk.Button(self, text="X", command=self.delete, width=1)

        btn_delete.grid(row=1, column=1)
        self.box_key.grid(row=1, column=2)
        self.box_path.grid(row=1, column=3)
        btn_open.grid(row=1, column=4)

    def open_dir(self):
        initial = self.dir or PICTURES_DIR
        path = tkfd.askdirectory(initialdir=initial)
        set_box(self.box_path, path)

    def delete(self):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
