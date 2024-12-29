# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['__main__.py'],
    pathex=[],
    binaries=[('bin/ffmpeg/windows/ffmpeg.exe', '.')],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='USWG',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='assets/icon.ico')
