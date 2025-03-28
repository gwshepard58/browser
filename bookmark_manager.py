# bookmark_manager.py
import os, json, shutil

class BookmarkManager:
    def __init__(self, path):
        self.path = path
        self.backup_path = path + '.backup'
        self.backup_created = False
        self.history = []
        self.current = None
        self.data = None
        self.load()

    def load(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        self.current = self.data['roots']['bookmark_bar']
        self.history = []

    def save(self):
        if not self.backup_created:
            shutil.copy2(self.path, self.backup_path)
            self.backup_created = True
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2)

    def restore(self):
        if os.path.exists(self.backup_path):
            shutil.copy2(self.backup_path, self.path)
            self.load()

    def go_back(self):
        if self.history:
            self.current = self.history.pop()
            return True
        return False

    def enter_folder(self, name):
        folder = next((f for f in self.current.get('children', []) if f.get('type') == 'folder' and f['name'] == name), None)
        if folder:
            self.history.append(self.current)
            self.current = folder
            return True
        return False

    def sort(self, folder=None, ascending=True, bookmarks_first=False):
        if folder is None:
            folder = self.current
        children = folder.get('children', [])
        folders = [f for f in children if f.get('type') == 'folder']
        bookmarks = [f for f in children if f.get('type') != 'folder']
        folders.sort(key=lambda f: f['name'].lower(), reverse=not ascending)
        bookmarks.sort(key=lambda f: f['name'].lower(), reverse=not ascending)
        folder['children'] = bookmarks + folders if bookmarks_first else folders + bookmarks

    def sort_all(self, folder=None, ascending=True, bookmarks_first=False):
        if folder is None:
            folder = self.current
        self.sort(folder, ascending, bookmarks_first)
        for item in folder.get('children', []):
            if item.get('type') == 'folder':
                self.sort_all(item, ascending, bookmarks_first)
