Agent instructions for `desktop_app/` module

- Keep UI logic thin and delegate persistence/network to `storage` and `ai` modules.
- Run AI calls and disk writes off the main thread; keep UI responsive.
