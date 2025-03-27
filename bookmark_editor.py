import json
import os
import shutil
import platform
import tkinter as tk
from tkinter import ttk, messagebox, Scrollbar

def get_bookmarks_path():
    system = platform.system()
    if system == "Windows":
        return os.path.expanduser(r'~\AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\Bookmarks')
    elif system == "Darwin":
        return os.path.expanduser('~/Library/Application Support/BraveSoftware/Brave-Browser/Default/Bookmarks')
    else:
        return os.path.expanduser('~/.config/BraveSoftware/Brave-Browser/Default/Bookmarks')

class BookmarkEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("Brave Bookmark Folder Reorder")
        self.master.geometry("850x500")

        self.bookmarks_path = get_bookmarks_path()
        self.backup_path = self.bookmarks_path + '.backup'
        self.backup_created = False

        if not os.path.exists(self.bookmarks_path):
            messagebox.showerror("Error", "Bookmarks file not found.")
            master.quit()
            return

        self.load_bookmarks()
        self.history = []
        self.current = self.data['roots']['bookmark_bar']

        self.build_ui()
        self.refresh_list()

    def load_bookmarks(self):
        with open(self.bookmarks_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def save_bookmarks(self):
        if not self.backup_created:
            shutil.copy2(self.bookmarks_path, self.backup_path)
            self.backup_created = True
            self.status_label.config(text="✅ Backup created before saving.")

        with open(self.bookmarks_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2)
        messagebox.showinfo("Saved", "Bookmarks saved successfully.")

    def restore_backup(self):
        if os.path.exists(self.backup_path):
            shutil.copy2(self.backup_path, self.bookmarks_path)
            self.load_bookmarks()
            self.current = self.data['roots']['bookmark_bar']
            self.history.clear()
            self.refresh_list()
            self.status_label.config(text="🔄 Restored from backup.")
            messagebox.showinfo("Restored", "Bookmarks restored from backup.")
        else:
            messagebox.showwarning("Restore Failed", "No backup file found.")

    def build_ui(self):
        frame = tk.Frame(self.master)
        frame.pack(fill=tk.BOTH, expand=True)

        # === Left Panel: Treeview ===
        self.tree = ttk.Treeview(frame, columns=("Name",), show='headings', height=25)
        self.tree.heading("Name", text="Name")
        self.tree.column("Name", anchor="w", width=400)
        self.tree.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)

        scrollbar = Scrollbar(frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns", pady=10)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<Double-1>", self.enter_folder)

        # === Right Panel: Buttons ===
        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=0, column=2, sticky="ns", padx=10, pady=10)

        # Sorting buttons
        tk.Button(btn_frame, text="Sort All (Asc, Folders First)", command=lambda: self.sort_all_and_refresh(True, False)).pack(pady=2)
        tk.Button(btn_frame, text="Sort All (Asc, Bookmarks First)", command=lambda: self.sort_all_and_refresh(True, True)).pack(pady=2)
        tk.Button(btn_frame, text="Sort All (Desc, Folders First)", command=lambda: self.sort_all_and_refresh(False, False)).pack(pady=2)
        tk.Button(btn_frame, text="Sort All (Desc, Bookmarks First)", command=lambda: self.sort_all_and_refresh(False, True)).pack(pady=2)

        tk.Label(btn_frame, text="─ This Folder Only ─", fg="gray").pack(pady=(10, 0))
        tk.Button(btn_frame, text="Sort Asc (Folders First)", command=lambda: self.sort_folder(True, False)).pack(pady=2)
        tk.Button(btn_frame, text="Sort Asc (Bookmarks First)", command=lambda: self.sort_folder(True, True)).pack(pady=2)
        tk.Button(btn_frame, text="Sort Desc (Folders First)", command=lambda: self.sort_folder(False, False)).pack(pady=2)
        tk.Button(btn_frame, text="Sort Desc (Bookmarks First)", command=lambda: self.sort_folder(False, True)).pack(pady=2)

        # Navigation and utility
        tk.Label(btn_frame, text="─ Navigation ─", fg="gray").pack(pady=(10, 0))
        tk.Button(btn_frame, text="Go Back", command=self.go_back).pack(pady=2)
        tk.Button(btn_frame, text="Restore Original", command=self.restore_backup).pack(pady=2)
        tk.Button(btn_frame, text="Save", command=self.save_bookmarks).pack(pady=2)
        tk.Button(btn_frame, text="Exit", command=self.master.quit).pack(pady=(10, 2))

        self.status_label = tk.Label(self.master, text="📁 Bookmarks loaded.", fg="blue")
        self.status_label.pack(pady=(0, 5))

        # Apply tag styles
        style = ttk.Style()
        style.configure("Treeview", rowheight=24)
        self.tree.tag_configure('folder', background="#fffacd")     # light yellow
        self.tree.tag_configure('bookmark', background="#dcdcdc")   # light gray

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

    def refresh_list(self):
        self.tree.delete(*self.tree.get_children())
        for item in self.current.get('children', []):
            name = item.get('name', '(Unnamed)')
            tag = 'folder' if item.get('type') == 'folder' else 'bookmark'
            self.tree.insert('', 'end', values=(name,), tags=(tag,))

    def enter_folder(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        name = self.tree.item(selected[0], "values")[0]
        folder = next((f for f in self.current.get('children', []) if f.get('type') == 'folder' and f['name'] == name), None)
        if folder:
            self.history.append(self.current)
            self.current = folder
            self.refresh_list()

    def go_back(self):
        if self.history:
            self.current = self.history.pop()
            self.refresh_list()
        else:
            messagebox.showinfo("Info", "Already at the top level.")

    def sort_folder(self, ascending=True, bookmarks_first=False):
        children = self.current.get('children', [])
        folders = [f for f in children if f.get('type') == 'folder']
        bookmarks = [f for f in children if f.get('type') != 'folder']
        folders.sort(key=lambda f: f['name'].lower(), reverse=not ascending)
        bookmarks.sort(key=lambda f: f['name'].lower(), reverse=not ascending)
        self.current['children'] = bookmarks + folders if bookmarks_first else folders + bookmarks
        self.refresh_list()
        position = "Bookmarks First" if bookmarks_first else "Folders First"
        self.status_label.config(text=f"🔤 Sorted {'A→Z' if ascending else 'Z→A'} ({position}).")

    def sort_all_folders(self, folder, ascending=True, bookmarks_first=False):
        if 'children' not in folder:
            return
        folders = [f for f in folder['children'] if f.get('type') == 'folder']
        bookmarks = [f for f in folder['children'] if f.get('type') != 'folder']
        folders.sort(key=lambda f: f['name'].lower(), reverse=not ascending)
        bookmarks.sort(key=lambda f: f['name'].lower(), reverse=not ascending)
        folder['children'] = bookmarks + folders if bookmarks_first else folders + bookmarks
        for subfolder in folders:
            self.sort_all_folders(subfolder, ascending, bookmarks_first)

    def sort_all_and_refresh(self, ascending=True, bookmarks_first=False):
        self.sort_all_folders(self.data['roots']['bookmark_bar'], ascending, bookmarks_first)
        self.refresh_list()
        self.status_label.config(text=f"✅ All folders sorted {'A→Z' if ascending else 'Z→A'} ({'Bookmarks First' if bookmarks_first else 'Folders First'}).")

def run_app():
    root = tk.Tk()
    app = BookmarkEditor(root)
    root.mainloop()

if __name__ == "__main__":
    run_app()
