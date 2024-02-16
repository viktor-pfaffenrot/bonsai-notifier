# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['bonsai_notifier.py'],
    pathex=[],
    binaries=[],
    datas=[('/home/pfaffenrot/anaconda3/lib/python3.9/site-packages/customtkinter', 'customtkinter/'), ('/home/pfaffenrot/bonsai_notification/src_canvas/db/*','db/'),('/home/pfaffenrot/bonsai_notification/src_canvas/images/*','images/')],
    hiddenimports=['PIL._tkinter_finder'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='bonsai_notifier',
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
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='bonsai_notifier',
)
