import tkinter as tk
import tkinter.ttk as ttk

# help window
class HelpWin(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.title("Help")
        self.geometry("400x300")
        self.resizable(False, False)

        label_help = ttk.Label(self, text="Help content goes here.")
        label_help.pack(pady=20)

        button_close = ttk.Button(self, text="Close", command=self.destroy)
        button_close.pack(pady=10)

        # self.bind("<Escape>", lambda e: self.destroy())
        self.bind("<Escape>", self.destroy)
