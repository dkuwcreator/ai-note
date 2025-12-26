"""Editor widget with autosave debounce."""
from __future__ import annotations
import tkinter as tk
from tkinter import scrolledtext
import threading
import time
from typing import Optional
from storage import repository

class Editor(tk.Frame):
    def __init__(self, master=None, note_id: Optional[int] = None):
        super().__init__(master)
        self.note_id = note_id
        self.text = scrolledtext.ScrolledText(self)
        self.text.pack(fill=tk.BOTH, expand=True)
        self._debounce_ms = 2000
        self._last_change = time.time()
        self._stop = False
        self.text.bind("<<Modified>>", self._on_modified)
        self._autosave_thread = threading.Thread(target=self._autosave_loop, daemon=True)
        self._autosave_thread.start()

    def _on_modified(self, event=None):
        try:
            self.text.edit_modified(False)
        except Exception:
            pass
        self._last_change = time.time()

    def _autosave_loop(self):
        while not self._stop:
            time.sleep(0.5)
            if time.time() - self._last_change > (self._debounce_ms / 1000.0):
                self._save()
                self._last_change = time.time() + 9999

    def _save(self):
        content = self.text.get("1.0", tk.END).rstrip()
        if self.note_id is None:
            self.note_id = repository.create_note("Untitled", content)
        else:
            repository.update_note(self.note_id, "Untitled", content)

    def destroy(self) -> None:
        self._stop = True
        super().destroy()
