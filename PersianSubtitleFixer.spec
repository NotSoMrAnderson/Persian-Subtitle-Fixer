# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets/comics-mask_97446.ico', 'assets')],
    hiddenimports=['PyQt5.sip'],  # Reduced hiddenimports to only what's essential
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['_gtkagg', '_tkagg', 'blib2to3', 'distutils', 'email', 'ftplib', 'html', 'http', 'lib2to3', 'logging', 'numpy', 'pandas', 'pydoc_data', 'pytz', 'test', 'unittest', 'xml'],  # Exclude unnecessary modules
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
    name='PersianSubtitleFixer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,  # Strip symbols to reduce size
    upx=True,
    console=False,  # Changed to False to hide terminal window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/comics-mask_97446.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=True,  # Strip symbols to reduce size
    upx=True,
    upx_exclude=[],
    name='PersianSubtitleFixer'
)