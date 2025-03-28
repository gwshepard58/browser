from collections import defaultdict, Counter
import urllib.parse
import tkinter as tk

def generate_stats(data, master):
    total_bookmarks = 0
    total_folders = 0
    top_level_folders = 0
    missing_titles = 0
    domain_counter = Counter()
    folder_sizes = []
    max_depth = 0
    all_urls = defaultdict(list)

    def walk(node, depth=1, path="Bookmark Bar"):
        nonlocal total_bookmarks, total_folders, max_depth, missing_titles

        if 'children' in node:
            total_folders += 1
            folder_sizes.append(len(node['children']))
            max_depth = max(max_depth, depth)

            for child in node['children']:
                if child['type'] == 'folder':
                    walk(child, depth + 1, f"{path}/{child.get('name', '(Unnamed)')}")
                elif child['type'] == 'url':
                    total_bookmarks += 1
                    url = child.get('url', '')
                    name = child.get('name', '')
                    if not name:
                        missing_titles += 1
                    if url:
                        domain = urllib.parse.urlparse(url).netloc
                        domain_counter[domain] += 1
                        all_urls[url].append((name, path))

    root = data['roots']['bookmark_bar']
    top_level_folders = len([item for item in root.get('children', []) if item.get('type') == 'folder'])
    walk(root)

    duplicates = sum(1 for urls in all_urls.values() if len(urls) > 1)
    most_common = domain_counter.most_common(1)[0] if domain_counter else ("N/A", 0)
    avg_items_per_folder = round(sum(folder_sizes) / len(folder_sizes), 1) if folder_sizes else 0

    stats = f"""📈 Bookmark Stats Summary:
--------------------------
Total bookmarks: {total_bookmarks}
Total folders: {total_folders}
Top-level folders: {top_level_folders}
Duplicate bookmarks: {duplicates}
Most common domain: {most_common[0]} ({most_common[1]})
Average items per folder: {avg_items_per_folder}
Deepest folder level: {max_depth}
Bookmarks missing title: {missing_titles}
"""

    stat_window = tk.Toplevel(master)
    stat_window.title("Bookmark Statistics")
    stat_window.geometry("500x300")

    text_area = tk.Text(stat_window, wrap="word")
    text_area.pack(fill=tk.BOTH, expand=True)
    text_area.insert(tk.END, stats)
    text_area.config(state=tk.DISABLED)