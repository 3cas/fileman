import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as tkfd
import os

from setup import log

# rename box dialog
class RenamerWin(tk.Toplevel):
    def __init__(self, root, current_dir: str, filename: str):
        super().__init__(root)
        self.root = root
        self.current_dir = current_dir
        self.filename = filename
        self.title("Rename File")

        head, self.ext = os.path.splitext(filename)
        label_ui_rename = ttk.Label(self, text=f"Rename {filename} to:")
        label_ui_ext = ttk.Label(self, text=f".{self.ext}")
        self.entry_newname = ttk.Entry(self)
        button_rename = ttk.Button(self, text="Rename", command=self.rename)
        button_cancel = ttk.Button(self, text="Cancel", command=self.destroy)

        label_ui_rename.grid(row=1, column=1, columnspan=2, padx=20, pady=(20, 0))
        self.entry_newname.grid(row=2, column=1, pady=5)
        label_ui_ext.grid(row=2, column=2, pady=5)
        button_rename.grid(row=3, column=1, pady=(0, 20))
        button_cancel.grid(row=3, column=2, pady=(0, 20))

        self.bind("<Enter>", self.rename)
        self.bind("<Escape>", self.destroy)
        self.entry_newname.focus_set()

    def rename(self):
        new_name_head = self.entry_newname.get()
        if new_name_head:
            self.new_name = new_name_head + "." + self.ext
            old_path = os.path.join(self.current_dir, self.filename)
            new_path = os.path.join(self.current_dir, self.new_name)
            os.rename(old_path, new_path)

    def run(self):
        self.wait_window()
        if hasattr(self, "new_name") and self.new_name:
            return self.new_name

# keyset info help
class KeysetHelp(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        ...

# keyset frame options
class KsOptionsPane(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        frame_filename = ttk.Frame(self)
        self.label_filename = ttk.Label(frame_filename, text=f"Keyset {parent.keyset_name}.json")
        button_change_file = ttk.Button(frame_filename, text="Change", command=parent.change_file)
        self.label_filename.pack(side="left", fill="x")
        button_change_file.pack(side="right")

        frame_display = ttk.Frame(self)
        label_ui_display = ttk.Label(frame_display, text="Display:")
        entry_display = ttk.Entry(frame_display)
        label_ui_display.pack(side="left")
        entry_display.pack(side="right", fill="x")

        frame_output = ttk.Frame(self)
        frame_output_ctl = ttk.Frame(frame_output)
        label_ui_output = ttk.Label(frame_output_ctl, text="Output base:")
        button_set_output = ttk.Button(frame_output_ctl, text="Open", command=parent.select_output_base)
        label_ui_output.pack(side="left", expand=True)
        button_set_output.pack(side="right")
        label_path_output = ttk.Label(frame_output, text="None set")
        frame_output_ctl.pack(side="top")
        label_path_output.pack(side="bottom")

        frame_input = ttk.Frame(self)
        frame_input_ctl = ttk.Frame(frame_input)
        label_ui_input = ttk.Label(frame_input_ctl, text="Input base:")
        button_set_input = ttk.Button(frame_input_ctl, text="Open", command=parent.select_input_base)
        button_remove_input = ttk.Button(frame_input_ctl, text=" X ", command=parent.remove_input_base)
        label_ui_input.pack(side="left", fill="x")
        button_remove_input.pack(side="right")
        button_set_input.pack(side="right")
        label_path_input = ttk.Label(frame_input, text="None set")
        frame_input_ctl.pack(side="top")
        label_path_input.pack(side="bottom")

        frame_recents = ttk.Frame(self)
        frame_recents_ctl = ttk.Frame(frame_recents)
        label_ui_recents = ttk.Label(frame_recents_ctl, text="Recent inputs:")
        button_edit_recents = ttk.Button(frame_recents_ctl, text="Edit", command=parent.edit_recent_dirs)
        label_ui_recents.pack(side="left", fill="x")
        button_edit_recents.pack(side="right")
        dropdown_recents = ttk.Label(frame_recents, text="PLACEHOLDER")
        frame_recents_ctl.pack(side="top")
        dropdown_recents.pack(side="bottom")

        frame_buttons_top = ttk.Frame(self)
        button_new = ttk.Button(frame_buttons_top, text="New", command=parent.new_keyset)
        button_save = ttk.Button(frame_buttons_top, text="Save", command=parent.save_keyset)
        button_del = ttk.Button(frame_buttons_top, text="Del", command=parent.delete_keyset)
        button_new.pack(side="left")
        button_save.pack(side="left")
        button_del.pack(side="left")

        frame_buttons_btm = ttk.Frame(self)
        button_duplicate = ttk.Button(frame_buttons_btm, text="Duplicate", command=parent.duplicate_keyset)
        button_help = ttk.Button(frame_buttons_btm, text="Help", command=parent.keyset_help)

        frame_filename.pack()
        frame_display.pack()
        frame_output.pack()
        frame_input.pack()
        frame_recents.pack()
        frame_buttons_top.pack()
        frame_buttons_btm.pack()

# keybind format for keyset editor
class KeybindEdit(ttk.Frame):
    def __init__(self, parent, initial_key: str = None, initial_subpath: str = None):
        super().__init__(parent)
        self.keyset_win = parent.parent

        button_delete = ttk.Button(self, text="X", command=self.delete, width=1)
        self.entry_key = ttk.Entry(self, width=3)
        self.entry_subpath = ttk.Entry(self, width=20)
        button_select = ttk.Button(self, text="Set", command=self.select_dir, width=3)

        button_delete.pack(side="left")
        self.entry_key.pack(side="left")
        self.entry_subpath.pack(side="left")
        button_select.pack(side="left")

        if initial_key:
            self.entry_key.insert(0, initial_key)
        if initial_subpath:
            self.entry_subpath.insert(0, initial_subpath)

    def delete(self):
        self.destroy()

    def select_dir(self):
        output_base = self.keyset_win.keyset_data["output_base"]
        path = tkfd.askdirectory(initialdir=output_base)
        head, directory = os.path.split(path)
        self.entry_subpath.delete(0, -1)
        self.entry_subpath.insert(0, directory)

    def get_vals(self):
        key = self.entry_key.get()
        subpath = self.entry_subpath.get()
        return key, subpath

# keyset frame display
class KsDisplayPane(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        if parent.keyset_data:
            display_label_text = f"Keyset \"{parent.keyset_data['display']}\""
        else:
            display_label_text = "No Keyset"

        self.label_display = ttk.Label(self, text=display_label_text)
        self.label_ui_no_binds = ttk.Label(self, text="No binds selected.")
        self.frame_keybinds = ttk.Frame(self)

        self.label_display.pack(side="top")
        self.label_ui_no_binds.pack(side="top")
        self.label_ui_no_binds.pack_forget()
        self.frame_keybinds.pack(side="top", fill="both", expand=True)
        self.label_ui_no_binds.pack_forget()

        self.load_display_keybinds()

    def load_display_keybinds(self):
        if self.parent.keyset_data:
            keybinds = self.parent.keyset_data["keys"]
            for key in keybinds.keys():
                bind_editor = KeybindEdit(self.frame_keybinds, key, keybinds[key])
                bind_editor.pack()
            self.frame_keybinds.pack()
            self.label_ui_no_binds.pack_forget()
        else:
            self.label_ui_no_binds.pack()
            self.frame_keybinds.pack_forget()

# change keyset
class KeysetWin(tk.Toplevel):
    def __init__(self, root, keyset_name: str = None, keyset_data: dict = None):
        super().__init__(root)
        self.root = root
        self.keyset_name = keyset_name
        self.keyset_data = keyset_data

        frame_options = KsOptionsPane(self)
        self.frame_keyset = KsDisplayPane(self)

        frame_options.pack(side="left", fill="both")
        self.frame_keyset.pack(side="right", fill="both", expand=True)

    def change_file(self):
        ...

    def select_output_base(self):
        ...

    def select_input_base(self):
        ...

    def remove_input_base(self):
        ...

    def edit_recent_dirs(self):
        ...

    def new_keyset(self):
        ...

    def save_keyset(self):
        frame_keybinds = self.frame_keyset.frame_keybinds
        for i, keybind_editor in enumerate(frame_keybinds.winfo_children()):
            slot = i + 1
            key, subpath = keybind_editor.get_vals()

            ... #Bro

    def delete_keyset(self):
        ...

    def duplicate_keyset(self):
        ...

    def keyset_help(self):
        KeysetHelp(self.root).run()
