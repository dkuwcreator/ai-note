"""Entry point for the desktop app (minimal Tkinter-based UI)."""
from __future__ import annotations
import sys
import logging
from pathlib import Path
import tkinter as tk
import tkinter.messagebox as messagebox
from desktop_app.ui import App


def _configure_logging() -> None:
    root = logging.getLogger()
    if root.handlers:
        return
    log_file = Path(__file__).resolve().parents[1] / "app.log"
    handlers = [logging.StreamHandler()]
    try:
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))
    except Exception:
        # If file handler can't be created, continue with console logging
        pass
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=handlers,
    )


def main() -> int:
    _configure_logging()
    logger = logging.getLogger(__name__)
    try:
        logger.info("Starting AI Notepad")
        # Create Tk root and add top-level menu with Settings entry
        root = tk.Tk()
        root.title("AI Notepad (MVP)")
        root.geometry("900x600")

        menubar = tk.Menu(root)
        settings_menu = tk.Menu(menubar, tearoff=0)

        # Initialize application UI
        app = App(root)

        def _open_settings():
            try:
                app.open_settings()
            except Exception:
                messagebox.showerror("Settings", "Failed to open Settings dialog.")

        settings_menu.add_command(label="Open Settings", command=_open_settings)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        root.config(menu=menubar)

        root.mainloop()
        logger.info("AI Notepad exited normally")
        return 0
    except Exception:
        logger.exception("Error launching app")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
