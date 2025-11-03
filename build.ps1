# Build script for creating a single-file Windows executable with PyInstaller
# Usage (PowerShell):
#   ./build.ps1 [-EntryPoint <string>] [-OneFile] [-NoConsole]
# By default it builds `game_main.py` (recommended while `game.py` is unstable).
param(
    [string]$EntryPoint = "game_main.py",
    [switch]$OneFile = $true,
    [switch]$NoConsole = $true
)

# Ensure Python & pip are available. If pyinstaller isn't installed install from requirements.txt
Write-Host "Using Python executable:`n`t$(Get-Command python -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source -ErrorAction SilentlyContinue)"

try {
    python -c "import PyInstaller" 2>$null
} catch {
    Write-Host "PyInstaller not found; installing from requirements.txt..."
    python -m pip install -r requirements.txt
}

# Build options
$pyinstallerArgs = @()
if ($OneFile) { $pyinstallerArgs += "--onefile" }
if ($NoConsole) { $pyinstallerArgs += "--noconsole" }

# Add data: include the assets folder if present
if (Test-Path "assets") {
    # Windows path format: source;dest
    $addData = "assets;assets"
    # Add as a single argument with quotes so PowerShell doesn't split on ';'
    $pyinstallerArgs += "--add-data `"$addData`""
    Write-Host "Including assets folder: $addData"
} else {
    Write-Host "No assets/ folder found — skipping --add-data"
}

# Optional: include any extra non-Python files here (fonts, sfx, etc.) similarly
# Example: $pyinstallerArgs += "--add-data"; $pyinstallerArgs += "path/to/file;dest"

# Build command
$pyinstallerArgs += $EntryPoint
$cmd = "pyinstaller " + ($pyinstallerArgs -join ' ')
Write-Host "Running: $cmd"

# Execute
Invoke-Expression $cmd

Write-Host "Build finished. Dist output is in the 'dist' directory. Test the exe on a Windows machine."