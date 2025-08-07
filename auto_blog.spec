# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=['C:\\my_games\\auto_blog\\.venv\\Scripts\\python.exe'],
    binaries=[],
    datas=[('C:\\\\my_games\\\\auto_blog\\\\data_basic', './data_basic'), ('C:\\\\my_games\\\\auto_blog\\\\mysettings', './mysettings'), ('auto_blog.ico', './')],
    hiddenimports=['PyQt5', 'pyserial', 'OpenAI', 'feedparser', 'requests', 'chardet', 'google.generativeai'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='auto_blog',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['auto_blog.ico','auto_blog.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='auto_blog',
)
