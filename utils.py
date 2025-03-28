# utils.py
import platform, os

def get_bookmarks_path():
    system = platform.system()
    if system == "Windows":
        return os.path.expanduser(r'~\AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\Bookmarks')
    elif system == "Darwin":
        return os.path.expanduser('~/Library/Application Support/BraveSoftware/Brave-Browser/Default/Bookmarks')
    else:
        return os.path.expanduser('~/.config/BraveSoftware/Brave-Browser/Default/Bookmarks')
