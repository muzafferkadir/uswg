from setuptools import setup, find_packages
import os
import subprocess

ffmpeg_path = '/opt/homebrew/bin/ffmpeg'
DATA_FILES = [('', [ffmpeg_path])]

APP = ['src/main.py']
OPTIONS = {
    'argv_emulation': False,
    'packages': find_packages() + ['unsilence'],
    'includes': ['tkinter', 'ffmpeg'],
    'excludes': ['matplotlib', 'numpy'],
    'site_packages': True,
    'resources': [ffmpeg_path],
    'plist': {
        'CFBundleName': 'Video Silence Remover',
        'CFBundleShortVersionString': '1.0',
        'LSMinimumSystemVersion': '10.10',
    }
}

setup(
    name='VideoSilenceRemover',
    version='1.0',
    packages=find_packages(),
    data_files=DATA_FILES,
    install_requires=['unsilence'],
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
