from bookmark_stats import generate_stats

def test_generate_stats_runs(monkeypatch):
    dummy_data = {
        "roots": {
            "bookmark_bar": {
                "children": [
                    {"type": "folder", "name": "Folder", "children": [
                        {"type": "url", "name": "Example", "url": "http://example.com"},
                        {"type": "url", "name": "Example2", "url": "http://example.org"}
                    ]}
                ]
            }
        }
    }
    monkeypatch.setattr("tkinter.Toplevel", lambda *a, **k: type("MockWin", (), {"title": lambda s, t: None, "geometry": lambda s, g: None})())
    monkeypatch.setattr("tkinter.Text", lambda *a, **k: type("MockText", (), {
        "pack": lambda s, **kw: None,
        "insert": lambda s, pos, text: None,
        "config": lambda s, **kw: None
    })())
    generate_stats(dummy_data, None)
