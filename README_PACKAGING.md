Packaging the game (Windows, PyInstaller)

This repository contains a small helper and guidance to build a standalone exe using PyInstaller.

Prerequisites
- Python (the same interpreter you use to run the game). On your machine this is `C:/Python313`.
- Pip and a working internet connection for the first-time install of dependencies.

Quick steps
1. Install required Python packages (recommended in a virtualenv):

   ```powershell
   python -m pip install -r requirements.txt
   ```

2. Build the executable (PowerShell helper provided):

   ```powershell
   ./build.ps1
   ```

   The script will by default build `game_main.py` into a single-file exe and include the `assets/` folder if it exists.

Manual PyInstaller example
- If you prefer to run PyInstaller directly (Windows example):

  ```powershell
  pyinstaller --onefile --noconsole --add-data "assets;assets" game_main.py
  ```

  Notes:
  - The `--add-data` syntax differs between OSes. On Windows use `source;dest`. On macOS/Linux use `source:dest`.
  - `game_main.py` is used while `game.py` is being stabilized. Replace it with `game.py` if/when `game.py` is clean.

resource_path helper
- This project includes a `utils.resource_path(relative_path)` helper that returns a path suitable both in development and when running a PyInstaller-built exe. The code already uses this helper in `sounds.py`. If you add other asset loads (images, fonts, etc.), use `resource_path('assets/...')` when passing file paths to loaders.

Troubleshooting
- If the exe fails to find assets at runtime, ensure you included `--add-data "assets;assets"` (or equivalent) when running PyInstaller.
- If the build fails due to Python syntax or import errors, run the game locally (python game_main.py) and fix errors before packaging.

Testing the exe
- After PyInstaller finishes you'll find the exe under `dist\<entrypoint>.exe`. Run it on the target Windows machine. If it fails due to missing DLLs, check the PyInstaller log for what was excluded and add explicit hooks if needed.

If you want, I can:
- Search and convert all remaining explicit file-loads to use `utils.resource_path(...)` (none were found except in `sounds.py`).
- Run a PyInstaller build here in the workspace and report back any errors (I can do that if you want me to run the build now).