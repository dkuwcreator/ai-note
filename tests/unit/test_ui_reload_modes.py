import tkinter as tk
from desktop_app.ui import App
from storage.db import RewriteMode


def test_reload_rewrite_options(monkeypatch):
    # Create a headless Tk root
    root = tk.Tk()
    root.withdraw()

    # Patch repository functions used by App
    class FakeRepo:
        def __init__(self):
            pass

    def fake_get_connection():
        return None

    def fake_list_rewrite_modes(conn):
        return [RewriteMode(id=1, name='One', instruction_template='{text}', enabled=True, order=1, applies_to='selection-only', builtin=False, advanced_settings=None)]

    import storage.db as db_mod
    monkeypatch.setattr(db_mod, 'get_connection', fake_get_connection)
    monkeypatch.setattr(db_mod, 'list_rewrite_modes', fake_list_rewrite_modes)

    app = App(root)
    # call reload and verify preset_var was set
    app.reload_rewrite_options()
    assert app.preset_var.get().startswith('mode:1:')
    root.destroy()
