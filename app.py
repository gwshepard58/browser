# app.py
import tkinter as tk
from ui import BookmarkEditorApp

def run():
    root = tk.Tk()
    app = BookmarkEditorApp(root)
    root.mainloop()

if __name__ == '__main__':
    run()
