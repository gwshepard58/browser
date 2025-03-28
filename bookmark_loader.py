## 🔹 `bookmark_loader.py`
import os
import platform
import json
import shutil

def get_bookmarks_path():
    system = platform.system()
    if system == "Windows":
        return os.path.expanduser(r'~\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Bookmarks')
    elif system == "Darwin":
        return os.path.expanduser('~/Library/Application Support/BraveSoftware/Brave-Browser/Default/Bookmarks')
    else:
        return os.path.expanduser('~/.config/BraveSoftware/Brave-Browser/Default/Bookmarks')

def load_bookmarks(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_bookmarks(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def backup_bookmarks(original_path):
    backup_path = original_path + '.backup'
    shutil.copy2(original_path, backup_path)
    return backup_path

def restore_backup(original_path):
    backup_path = original_path + '.backup'
    if os.path.exists(backup_path):
        shutil.copy2(backup_path, original_path)
        return True
    return False 

# Placeholder - bookmark_loader module
