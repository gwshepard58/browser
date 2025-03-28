import tkinter as tk
from bookmark_utils import find_duplicates

def test_find_duplicates_runs():
    dummy_data = {
        "roots": {
            "bookmark_bar": {
                "children": [
                    {"type": "url", "name": "Example", "url": "http://example.com"},
                    {"type": "url", "name": "Example Duplicate", "url": "http://example.com"}
                ]
            }
        }
    }

    root = tk.Tk()
    root.withdraw()  # Prevent window from showing

    find_duplicates(dummy_data, root)

    root.destroy()  # Clean up
