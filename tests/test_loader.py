import os
import json
import tempfile
from bookmark_loader import load_bookmarks, save_bookmarks, backup_bookmarks, restore_backup

def test_load_and_save_bookmarks():
    data = {"roots": {"bookmark_bar": {"children": []}}}
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        save_bookmarks(tmp.name, data)
        loaded = load_bookmarks(tmp.name)
        assert loaded == data

def test_backup_and_restore():
    data = {"roots": {"bookmark_bar": {"children": []}}}
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        save_bookmarks(tmp.name, data)
        backup_path = backup_bookmarks(tmp.name)
        assert os.path.exists(backup_path)
        assert restore_backup(tmp.name)
