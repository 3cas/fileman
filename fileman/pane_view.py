import tkinter.ttk as ttk
from PIL import ImageTk, Image, ImageOps
import pillow_heif
import os

import texts as t

class ImageFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.label_info = ttk.Label(self, text="(image info)")
        self.label_name = ttk.Label(self, text="(image name)")
        self.label_image = ttk.Label(self, text="No image loaded")

        self.label_info.pack(side="top", fill="x")
        self.label_name.pack(side="top", fill="x")
        self.label_image.pack(side="bottom", fill="both", expand=True)

        self.label_info.pack_forget()
        self.label_name.pack_forget()

    def display_image(self, filepath: str, index: int = None, index_of: int = None):
        parent, filename = os.path.split(filepath)
        image = Image.open(filepath)
        image = ImageOps.exif_transpose(image)
        image_width, image_height = image.size

        frame_width, frame_height = self.winfo_width(), self.winfo_height()
        max_image_width, max_image_height = frame_width - 20, frame_height - 20
        resize_ratio = min(max_image_width / image_width, max_image_height / image_height)
        display_size = (int(image_width * resize_ratio), int(image_height * resize_ratio))
        image_resized = image.resize(display_size)
        self.image_tk = ImageTk.PhotoImage(image_resized)

        self.label_image.configure(image=self.image_tk)
        self.label_name.configure(text=filename)
        info = f"{image_width}x{image_height}px"
        if index and index_of:
            info += f" ~ {index}/{index_of}"
        self.label_info.configure(text=info)


# navigation buttons / defaults at bottom
class NavFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        root = parent.root

        self.button_prev = ttk.Button(self, text="(\u2190) Prev", command=root.nav_prev)
        self.button_next = ttk.Button(self, text="Next (\u2192)", command=root.nav_next)
        self.button_undo = ttk.Button(self, text="Undo (s+Z)", command=root.undo_move)
        self.button_reload = ttk.Button(self, text="Reload (s+U)", command=root.reload_image)
        self.button_rename = ttk.Button(self, text="Rename (s+R)", command=root.rename_image)

        self.button_prev["state"] = "disabled"
        self.button_next["state"] = "disabled"
        self.button_undo["state"] = "disabled"
        self.button_rename["state"] = "disabled"

        self.button_prev.pack(side="left")
        self.button_undo.pack(side="left")
        self.button_reload.pack(side="left", fill="x")
        self.button_rename.pack(side="right")
        self.button_next.pack(side="right")

# composite viewerframe
class ViewPane(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.root = parent
        
        self.frame_image = ImageFrame(self)
        self.frame_nav = NavFrame(self)

        self.frame_image.pack(side="top", fill="both", expand=True)
        self.frame_nav.pack(side="bottom", fill="x")
