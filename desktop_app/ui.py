"""Very small Tkinter UI for manual testing and development."""
from __future__ import annotations
import tkinter as tk
from tkinter import scrolledtext
import logging
from .editor import Editor
from storage import repository
from ai.presets import PRESETS, build_prompt
from ai.client import AIClient
import concurrent.futures
import tkinter.messagebox as messagebox
from config.settings import get_settings

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
        self.preset_var = tk.StringVar(value=list(PRESETS.keys())[0])
        self.preset_menu = tk.OptionMenu(self.sidebar, self.preset_var, *list(PRESETS.keys()))
        self.preset_menu.pack(padx=8, pady=4, fill=tk.X)

        self.rewrite_btn = tk.Button(self.sidebar, text="Rewrite (AI)", command=self.on_rewrite)
        self.rewrite_btn.pack(padx=8, pady=4, fill=tk.X)

        self.ai_status = tk.Label(self.sidebar, text="")
        self.ai_status.pack(padx=8, pady=(4,8))

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

        preset = self.preset_var.get()
        prompt = build_prompt(preset, text)
        self.ai_status.config(text="Requesting AI...")
        self.logger.info("Submitting rewrite request", extra={"preset": preset})
        fut = self._executor.submit(self._ai_client.rewrite, prompt)

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

def run_app() -> None:
    root = tk.Tk()
    root.title("AI Notepad (MVP)")
    root.geometry("900x600")
    App(root)
    root.mainloop()


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
