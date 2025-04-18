import tkinter.ttk as ttk
import tkinter.filedialog as tkfd
import os

# keyset frame display
class KeysetEditorPane(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.toplevel = parent

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
        if self.toplevel.keyset_data:
            keybinds = self.toplevel.keyset_data["keys"]
            for key in keybinds.keys():
                bind_editor = EditableKeybind(self.frame_keybinds, key, keybinds[key])
                bind_editor.pack()
            self.frame_keybinds.pack()
            self.label_ui_no_binds.pack_forget()
        else:
            self.label_ui_no_binds.pack()
            self.frame_keybinds.pack_forget()

# keybind format for keyset editor
class EditableKeybind(ttk.Frame):
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
