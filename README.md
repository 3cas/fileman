# pictureman
A time-saving keyboard-controlled photo organizer written in Python.

### Sales Pitch
Have you ever spent hours trying to organize your photos, dragging and dropping them between different folders, renaming them, and having to open each one only to close it again and drag it to the right folder? Well, if you share my frustration, Pictureman is for you! Pictureman is a simple utility that goes through the photos in a folder and lets you bind keypresses to different sorted folders. For example, you could make folders named "selfies", "memes", "nature", "family", and "cats" and then have them bound to S, M, N, F, and C, respectively. Then for each photo you just press the key of the folder, Pictureman moves the file for you, and it displays the next photo. Made a mistake? Just press Shift+Z.

### Other Features
- Shift+Z - undo move operation (supports multiple undos)
- Shift+R - rename file on-the-fly
- Shift+U - refresh window
- L/R arrow keys - go through photos

### It's not perfect
I made this for myself mainly, and right now it's lacking several features and it's not perfect in how it works. Hopefully though, it helps! Also, there's no "delete" function, but this is intentional because I don't want to be liable for deleting your files. You can simply make a "delete" folder and delete everything in it when you're done. 

### Coming Soon
- Better config file and an options menu
- Shift+Y to redo action
- Ability to undo renames and other operations
- Better UI (it's awful rn)
