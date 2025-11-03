# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['game.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    # Exclude large development/test packaging modules not required at runtime
    excludes=['setuptools', 'pkg_resources', 'pip', 'distutils', 'pytest', 'unittest', 'tests', 'tkinter', 'importlib_metadata'],
    noarchive=False,
    # Use higher optimization to reduce size of bytecode
    optimize=2,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='game',
    debug=False,
    bootloader_ignore_signals=False,
    # Strip debug symbols from the bootloader/exe to reduce size
    strip=True,
    # Use UPX if available on the system to compress binaries further
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
