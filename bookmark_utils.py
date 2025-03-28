
#bookmark_utils.py`

from collections import defaultdict
import tkinter as tk
from tkinter import messagebox

def find_duplicates(data, master):
    def collect_bookmarks(folder, path="Bookmark Bar"):
        for item in folder.get("children", []):
            if item.get("type") == "folder":
                collect_bookmarks(item, f"{path}/{item['name']}")
            elif item.get("type") == "url":
                url = item.get("url")
                if url:
                    all_bookmarks.setdefault(url, []).append((item.get("name", "(Unnamed)"), path))

    all_bookmarks = {}
    collect_bookmarks(data['roots']['bookmark_bar'])
    duplicates = {url: entries for url, entries in all_bookmarks.items() if len(entries) > 1}

    if not duplicates:
        messagebox.showinfo("No Duplicates", "No duplicate bookmarks found.")
        return

    dup_window = tk.Toplevel(master)
    dup_window.title("Duplicate Bookmarks")
    dup_window.geometry("600x400")
    text_area = tk.Text(dup_window, wrap="word")
    text_area.pack(fill=tk.BOTH, expand=True)

    for url, entries in duplicates.items():
        text_area.insert(tk.END, f"🔗 {url}\n")
        for name, folder_path in entries:
            text_area.insert(tk.END, f"    📁 {folder_path} — {name}\n")
        text_area.insert(tk.END, "\n")

    text_area.config(state=tk.DISABLED)

