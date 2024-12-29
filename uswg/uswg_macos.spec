# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['__main__.py'],
    pathex=[],
    binaries=[('/opt/homebrew/bin/ffmpeg', '.')],
    datas=[],
    hiddenimports=[
        'pkg_resources.py2_warn',
        'tkinter',
        'unsilence'
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=False)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='USWG',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False)

app = BUNDLE(exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='USWG.app',
    icon='assets/icon.icns',  # Optional: Add macOS icon
    bundle_identifier='com.uswg.app',
    info_plist={
        'NSHighResolutionCapable': 'True',
        'LSBackgroundOnly': 'False',
        'CFBundleName': 'USWG',
        'CFBundleDisplayName': 'USWG',
        'CFBundleGetInfoString': "Unsilence Video Tool",
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
    },
)
