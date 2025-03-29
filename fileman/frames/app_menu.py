import tkinter.ttk as ttk
from PIL import ImageTk, Image

from constants import LOGO_PATH
import texts as t

# frame containing just the logo
class LogoFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.image_logo = ImageTk.PhotoImage(Image.open(LOGO_PATH))
        label_ui_logo = ttk.Label(self, image=self.image_logo)
        label_ui_logo.pack()

# frame containing keyset info and table
class KeysFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.label_key_count = ttk.Label(self, text=t.KEYSET_NO_LOAD)
        self.tree_keyset = ttk.Treeview(self, columns=("key", "dir"), show="headings")
        self.tree_keyset.heading("key", text="Key")
        self.tree_keyset.heading("dir", text="Folder")

        self.label_key_count.pack(side="top")
        self.tree_keyset.pack(side="top")
        self.tree_keyset.pack_forget()

    def load_keyset(self):
        pass
        ...
        self.tree_keyset.pack()

# frame containing all controls
class ControlsFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        root = parent.root

        frame_upper = ttk.Frame(self)
        frame_lower = ttk.Frame(self)
        label_ui_copyright = ttk.Label(self, text=t.COPYRIGHT)

        # upper frame
        label_ui_keyset = ttk.Label(frame_upper, text=t.KEYSET_LABEL)
        self.label_active_keyset = ttk.Label(frame_upper, text=t.KEYSET_NONE)
        button_change_keyset = ttk.Button(frame_upper, text=t.BTN_CHANGE, command=root.edit_keyset)

        label_ui_keyset.pack(side="left")
        self.label_active_keyset.pack(side="left")
        button_change_keyset.pack(side="left")

        # lower middle frame
        frame_lower_middle = ttk.Frame(frame_lower)
        button_help = ttk.Button(frame_lower_middle, text=t.BTN_HELP, width=8, command=root.show_help)
        button_exit = ttk.Button(frame_lower_middle, text=t.BTN_EXIT, width=8, command=root.exit_fm)

        button_help.pack(side="left", fill="x")
        button_exit.pack(side="right", fill="x")

        # lower frame
        self.button_move_left = ttk.Button(frame_lower, text=t.BTN_LEFT, width=6, command=root.ui_menu_left)
        self.button_move_right = ttk.Button(frame_lower, text=t.BTN_RIGHT, width=6, command=root.ui_menu_right)
        self.button_move_left["state"] = "disabled"

        self.button_move_left.pack(side="left")
        frame_lower_middle.pack(side="left", fill="x")
        self.button_move_right.pack(side="right")

        # pack controls
        frame_upper.pack(side="top")
        frame_lower.pack(side="top")
        label_ui_copyright.pack(side="top")

# menu frame left of viewer frame
class MenuPane(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.root = parent

        frame_logo = LogoFrame(self)
        self.frame_keys = KeysFrame(self)
        self.frame_controls = ControlsFrame(self)

        frame_logo.pack(side="top")
        self.frame_keys.pack(side="top", expand=True)
        self.frame_controls.pack(side="bottom")

