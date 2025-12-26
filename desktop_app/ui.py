"""Very small Tkinter UI for manual testing and development."""
from __future__ import annotations
import tkinter as tk
from tkinter import scrolledtext
import logging
from .editor import Editor
from storage import repository
from storage import db as storage_db
from ai.presets import PRESETS, build_prompt
from ai.client import AIClient
import concurrent.futures
import tkinter.messagebox as messagebox
from config.settings import get_settings


def _load_qt_settings_dialog():
    """Load Qt settings dialog lazily.

    Importing PySide6/QtWidgets during Tkinter app startup can crash the process
    if any QWidget is created before a QApplication exists.
    """

    try:
        from PySide6 import QtWidgets  # type: ignore
        from .settings_dialog import SettingsDialog  # type: ignore
    except Exception:
        return None, None
    return QtWidgets, SettingsDialog

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.logger = logging.getLogger(__name__)
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.sidebar = tk.Frame(self, width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(self.sidebar, text="Search").pack(padx=8, pady=(8,0))
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.sidebar, textvariable=self.search_var)
        self.search_entry.pack(padx=8, pady=4, fill=tk.X)
        self.search_entry.bind('<Return>', self.on_search)

        tk.Label(self.sidebar, text="Notebooks").pack(padx=8, pady=(8,0))
        self.notebooks_list = tk.Listbox(self.sidebar)
        self.notebooks_list.pack(padx=8, pady=4, fill=tk.BOTH, expand=True)

        tk.Label(self.sidebar, text="Recent").pack(padx=8, pady=(8,0))
        self.recent_list = tk.Listbox(self.sidebar)
        self.recent_list.pack(padx=8, pady=4, fill=tk.BOTH, expand=True)

        self.editor = Editor(self)
        self.editor.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # AI rewrite controls
        self.preset_var = tk.StringVar()
        self.preset_menu = tk.OptionMenu(self.sidebar, self.preset_var, "")
        # populate menu items properly
        self.reload_rewrite_options()
        self.preset_menu.pack(padx=8, pady=4, fill=tk.X)

        self.rewrite_btn = tk.Button(self.sidebar, text="Rewrite (AI)", command=self.on_rewrite)
        self.rewrite_btn.pack(padx=8, pady=4, fill=tk.X)

        self.test_conn_btn = tk.Button(self.sidebar, text="Test AI Connection", command=self.on_test_connection)
        self.test_conn_btn.pack(padx=8, pady=4, fill=tk.X)

        self.ai_status = tk.Label(self.sidebar, text="")
        self.ai_status.pack(padx=8, pady=(4,8))

        # Settings menu/button (open dialog if available)
        settings_btn = tk.Button(self.sidebar, text="Settings", command=self.open_settings)
        settings_btn.pack(padx=8, pady=4, fill=tk.X)

        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        self._ai_client = AIClient()
        self.logger.info("UI initialized, AI client created")

        self.load_notebooks()
        self.load_recent()

    def load_notebooks(self):
        self.notebooks_list.delete(0, tk.END)
        for nb in repository.list_notebooks():
            self.notebooks_list.insert(tk.END, nb['name'])

    def load_recent(self):
        self.recent_list.delete(0, tk.END)
        for r in repository.list_recent():
            self.recent_list.insert(tk.END, str(r['note_id']))

    def on_search(self, event=None):
        q = self.search_var.get().strip()
        if not q:
            return
        results = repository.search(q)
        if results:
            # open first result for now
            nid = results[0]['id']
            note = repository.get_note(nid)
            self.editor.text.delete('1.0', tk.END)
            self.editor.text.insert('1.0', note.get('body',''))

    def on_rewrite(self):
        sel = self.editor.text.tag_ranges(tk.SEL)
        if sel:
            text = self.editor.text.get(*sel)
        else:
            text = self.editor.text.get('1.0', tk.END).strip()

        if not text:
            messagebox.showinfo("Rewrite", "No text selected or available to rewrite.")
            return

        # Ensure Azure OpenAI settings are configured before making a request
        settings = get_settings()
        if not settings.azure_openai_endpoint or not settings.azure_openai_deployment:
            msg = (
                "Azure OpenAI is not configured.\n"
                "Set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_DEPLOYMENT environment variables."
            )
            self.logger.error("Azure OpenAI configuration missing")
            messagebox.showerror("AI Not Configured", msg)
            return

        sel_option = self.preset_var.get()
        self.ai_status.config(text="Requesting AI...")
        # Determine if selection is a stored mode or a preset
        try:
            if sel_option.startswith("mode:"):
                # format: mode:<id>:<name>
                parts = sel_option.split(":", 2)
                mode_id = int(parts[1])
                conn = storage_db.get_connection()
                mode = next((m for m in storage_db.list_rewrite_modes(conn) if m.id == mode_id), None)
                if not mode:
                    raise RuntimeError("Selected rewrite mode not found")
                fut = self._executor.submit(self._ai_client.apply_rewrite_mode, mode, text)
            elif sel_option.startswith("preset:"):
                key = sel_option.split(":", 1)[1]
                prompt = build_prompt(key, text)
                fut = self._executor.submit(self._ai_client.rewrite, prompt)
            else:
                # fallback to first preset
                prompt = build_prompt(list(PRESETS.keys())[0], text)
                fut = self._executor.submit(self._ai_client.rewrite, prompt)
            self.logger.info("Submitting rewrite request", extra={"selection": sel_option})
        except Exception as e:
            self.logger.exception("Failed to submit rewrite request")
            messagebox.showerror("AI Error", str(e))
            self.ai_status.config(text="")
            return

        def cb(future):
            try:
                result = future.result()
            except Exception as e:
                err_msg = str(e)
                self.logger.exception("AI rewrite failed")
                self.master.after(0, lambda err=err_msg: (self.ai_status.config(text="AI error"), messagebox.showerror("AI Error", err)))
                return

            def show_preview():
                self.ai_status.config(text="")
                self.logger.info("AI rewrite received", extra={"chars": len(result) if result else 0})
                PreviewDialog(self.master, original=text, rewritten=result, apply_callback=lambda r: self._apply_rewrite(sel, r))

            self.master.after(0, show_preview)
        fut.add_done_callback(cb)

    def _apply_rewrite(self, sel, new_text):
        self.logger.info("Applying rewrite", extra={"selected": bool(sel)})
        if sel:
            self.editor.text.delete(*sel)
            self.editor.text.insert(sel[0], new_text)
        else:
            self.editor.text.delete('1.0', tk.END)
            self.editor.text.insert('1.0', new_text)

    def on_test_connection(self):
        """Asynchronously test the AI connection and display categorized results."""
        settings = get_settings()
        if not settings.azure_openai_endpoint or not settings.azure_openai_deployment:
            messagebox.showerror("AI Not Configured", "Azure OpenAI endpoint or deployment is not configured.")
            return

        self.ai_status.config(text="Testing connection...")
        fut = self._executor.submit(self._ai_client.test_connection)

        def cb(future):
            try:
                res = future.result()
            except Exception as e:
                self.logger.exception("Test connection failed")
                self.master.after(0, lambda: (self.ai_status.config(text="Test failed"), messagebox.showerror("Test Error", str(e))))
                return

            # Update UI on main thread
            def ui_update():
                status = res.get("status", "other")
                ok = res.get("ok", False)
                details = res.get("details", "")
                if ok:
                    self.ai_status.config(text="Connection OK")
                    messagebox.showinfo("AI Connection", f"OK — {details}")
                else:
                    self.ai_status.config(text=f"Connection: {status}")
                    messagebox.showerror("AI Connection", f"Status: {status}\nDetails: {details}")

            self.master.after(0, ui_update)

        fut.add_done_callback(cb)

    def open_settings(self):
        QtWidgets, SettingsDialog = _load_qt_settings_dialog()
        if QtWidgets is None or SettingsDialog is None:
            messagebox.showinfo("Settings", "Settings dialog unavailable (PySide6 not installed).")
            return
        try:
            qt_app = QtWidgets.QApplication.instance()
            if qt_app is None:
                qt_app = QtWidgets.QApplication([])
            dlg = SettingsDialog()
            dlg.exec()
            # After settings dialog closes, refresh rewrite options
            try:
                self.reload_rewrite_options()
            except Exception:
                pass
        except Exception:
            messagebox.showerror("Settings", "Failed to open Settings dialog.")

    def reload_rewrite_options(self):
        # Rebuild the rewrite options from storage and presets
        try:
            conn = storage_db.get_connection()
            modes = storage_db.list_rewrite_modes(conn)
        except Exception:
            modes = []

        options = []
        for m in modes:
            options.append(f"mode:{m.id}:{m.name}")
        for k in PRESETS.keys():
            options.append(f"preset:{k}")

        # Clear existing menu
        menu = self.preset_menu['menu']
        menu.delete(0, 'end')
        for opt in options:
            menu.add_command(label=opt, command=lambda v=opt: self.preset_var.set(v))

        # Set default if not set
        if options and not self.preset_var.get():
            self.preset_var.set(options[0])


def run_app() -> None:
    root = tk.Tk()
    root.title("AI Notepad (MVP)")
    root.geometry("900x600")
    App(root)
    root.mainloop()

    
def _build_menu_options_from_modes_and_presets(modes):
    options = []
    for m in modes:
        options.append(f"mode:{m.id}:{m.name}")
    for k in PRESETS.keys():
        options.append(f"preset:{k}")
    return options



class PreviewDialog(tk.Toplevel):
    def __init__(self, master, original: str, rewritten: str, apply_callback):
        super().__init__(master)
        self.title("AI Rewrite Preview")
        self.apply_callback = apply_callback
        self.geometry("800x400")

        self.orig_text = scrolledtext.ScrolledText(self, width=40)
        self.orig_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.orig_text.insert('1.0', original)
        self.orig_text.config(state=tk.DISABLED)

        self.rew_text = scrolledtext.ScrolledText(self, width=40)
        self.rew_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.rew_text.insert('1.0', rewritten)

        btn_frame = tk.Frame(self)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X)

        accept_btn = tk.Button(btn_frame, text="Accept", command=self._accept)
        accept_btn.pack(side=tk.RIGHT, padx=8, pady=8)

        cancel_btn = tk.Button(btn_frame, text="Cancel", command=self._cancel)
        cancel_btn.pack(side=tk.RIGHT, padx=8, pady=8)

    def _accept(self):
        new_text = self.rew_text.get('1.0', tk.END).rstrip()
        self.apply_callback(new_text)
        self.destroy()

    def _cancel(self):
        self.destroy()

    def open_settings(self):
        QtWidgets, SettingsDialog = _load_qt_settings_dialog()
        if QtWidgets is None or SettingsDialog is None:
            messagebox.showinfo("Settings", "Settings dialog unavailable (PySide6 not installed).")
            return
        try:
            qt_app = QtWidgets.QApplication.instance()
            if qt_app is None:
                qt_app = QtWidgets.QApplication([])
            dlg = SettingsDialog()
            dlg.exec()
        except Exception:
            messagebox.showerror("Settings", "Failed to open Settings dialog.")
