import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkmb
import tkinter.filedialog as tkfd
from PIL import Image, ImageTk, ImageOps
import pillow_heif
import os
import json

from setup import log, CONF_LOADED
from constants import VERSION, MAIN_DIR
from pane_menu import MenuPane
from pane_view import ViewPane
from dialogs import RenamerWin, KeysetWin

log("Initializing application...")

# define app
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.minsize(300, 300)
        self.title(f"FileMan v{VERSION}")

        self.style = ttk.Style()
        self.style.configure("Viewer.TFrame", background="lightblue")
        self.style.configure("Viewer.TLabel", background="lightblue")
        self.style.configure("KeyNormal.TEntry", background="white")
        self.style.configure("KeyActive.TEntry", background="red")

        self.menu = MenuPane(self)
        self.viewer = ViewPane(self)
        self._pack_panes()

        if "recent_keysets" in CONF_LOADED:
            keyset_name = CONF_LOADED["recent_keysets"]
            try:
                with open(os.path.join(MAIN_DIR, "keysets", keyset_name), "r") as f:
                    keyset = json.load(f)
            except: 
                keyset_name = None
                keyset = None
        else:
            keyset_name = None
            keyset = None

        self.current_keyset_name = keyset_name
        self.current_keyset = keyset
        self.current_dir = None
        self.current_filename = None

    def change_keyset(self):
        keyset_editor = KeysetWin(self, self.current_keyset_name, self.current_keyset)
        #keyset_result = keyset_editor.run()
        #if keyset_result:
            #log("")
            #self.current_keyset_name = keyset_result[0]
            #self.current_keyset = keyset_result[1]

    def show_help(self):
        ...

    def exit_fm(self):
        ...

    def _reset_panes(self):
        self.menu.pack_forget()
        self.viewer.pack_forget()

    def _pack_panes(self, menu_right: bool = False):
        side_menu = "right" if menu_right else "left"
        side_viewer = "left" if menu_right else "right"
        self.menu.frame_controls.button_move_left["state"] = "enabled" if menu_right else "disabled"
        self.menu.frame_controls.button_move_right["state"] = "disabled" if menu_right else "enabled"
        self.menu.pack(side=side_menu, fill="y")
        self.viewer.pack(side=side_viewer, fill="y", expand=True)

    def menu_left(self):
        self._reset_panes()
        self._pack_panes()

    def menu_right(self):
        self._reset_panes()
        self._pack_panes(True)

    def nav_prev(self):
        ...

    def nav_next(self):
        ...

    def undo_move(self):
        ...

    def reload_image(self):
        ...

    def rename_image(self):
        renamer = RenamerWin(self, self.current_keyset)
        new_name = renamer.run()
        log(f"Renamed {self.current_filename} -> {new_name}")
        self.current_filename = new_name


if __name__ == "__main__":
    App().mainloop()
