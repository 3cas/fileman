import tkinter as tk
import tkinter.ttk as ttk

# contains filename and open button
class FilenameFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.label_filename = ttk.Label(self, text=f"Keyset {parent.keyset_name}.json")
        self.button_change_file = ttk.Button(self, text="OpenJ", command=parent.open_file)

        self.label_filename.pack(side="left", fill="x")
        self.button_change_file.pack(side="right")

# contains display name entry
class DisplayNameFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        label_ui_display = ttk.Label(self, text="Display:")
        entry_display = ttk.Entry(self)

        label_ui_display.pack(side="left")
        entry_display.pack(side="right", fill="x")

# contains output base setter
class OutputBaseFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        label_ui_output = ttk.Label(self, text="Output base:")
        button_set_output = ttk.Button(self, text="Open", command=parent.select_output_base)
        label_path_output = ttk.Label(self, text="None set")

        label_ui_output.pack(side="left", expand=True)
        button_set_output.pack(side="right")
        label_path_output.pack(side="bottom")

# contains input base setter
class InputBaseFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        label_ui_input = ttk.Label(self, text="Input base:")
        button_set_input = ttk.Button(self, text="Open", command=parent.select_input_base)
        button_remove_input = ttk.Button(self, text=" X ", command=parent.remove_input_base)
        label_path_input = ttk.Label(self, text="None set")

        label_ui_input.pack(side="left", fill="x")
        button_remove_input.pack(side="right")
        button_set_input.pack(side="right")
        label_path_input.pack(side="bottom")

# contains recent inputs dropdown and edit button
class RecentInputsFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        label_ui_recents = ttk.Label(self, text="Recent inputs:")
        button_edit_recents = ttk.Button(self, text="Edit", command=parent.edit_recent_dirs)
        dropdown_recents = ttk.Label(self, text="DROPDOWN HERE")

        label_ui_recents.pack(side="left", fill="x")
        button_edit_recents.pack(side="right")
        dropdown_recents.pack(side="bottom")

# contains bottom buttons
class BottomButtonsFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        frame_top = ttk.Frame(self)
        button_new = ttk.Button(frame_top, text="New", command=parent.new)
        button_del = ttk.Button(frame_top, text="Delete", command=parent.delete)
        button_new.pack(side="left")
        button_del.pack(side="right")

        frame_btm = ttk.Frame(self)
        button_save = ttk.Button(frame_btm, text="Save", command=parent.save)
        button_save_as = ttk.Button(frame_btm, text="Save As...", command=parent.save_as)
        button_save.pack(side="left")
        button_save_as.pack(side="right")

        frame_top.pack(side="top", fill="x")
        frame_btm.pack(side="bottom", fill="x")

# keyset frame options
class KeysetOptionsPane(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        frame_filename = FilenameFrame(self)
        frame_display = DisplayNameFrame(self)
        frame_output_base = OutputBaseFrame(self)
        frame_input_base = InputBaseFrame(self)
        frame_recent_inputs = RecentInputsFrame(self)
        frame_buttons = BottomButtonsFrame(self)

        frame_filename.pack()
        frame_display.pack()
        frame_output_base.pack()
        frame_input_base.pack()
        frame_recent_inputs.pack()
        frame_buttons.pack()
