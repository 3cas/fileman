import tkinter as tk

from frames.keyset_options import KeysetOptionsPane
from frames.keyset_editor import KeysetEditorPane

# keyset editor with options
class KeysetWin(tk.Toplevel):
    def __init__(self, root, keyset_name: str = None, keyset_data: dict = None):
        super().__init__(root)
        self.root = root
        self.keyset_name = keyset_name
        self.keyset_data = keyset_data

        frame_options = KeysetOptionsPane(self)
        self.frame_keyset = KeysetEditorPane(self)

        frame_options.pack(side="left", fill="both")
        self.frame_keyset.pack(side="right", fill="both", expand=True)

    def open_file(self): ...

    def new_keyset(self): ...

    def save_current(self):
        frame_keybinds = self.frame_keyset.frame_keybinds
        for i, keybind_editor in enumerate(frame_keybinds.winfo_children()):
            slot = i + 1
            key, subpath = keybind_editor.get_vals()

            ...  # Bro

    def save_current_as(self): ...

    def delete_current(self): ...

    def select_output_base(self): ...

    def select_input_base(self): ...

    def remove_input_base(self): ...

    def edit_recent_dirs(self): ...
