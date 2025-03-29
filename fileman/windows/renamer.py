import tkinter as tk
import tkinter.ttk as ttk
import os

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
