# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app\\__main__.py'],
    pathex=['C:\\Users\\Clara\\AppData\\Local\\pypoetry\\Cache\\virtualenvs\\playground-pv6Vx99u-py3.13\\Lib\\site-packages'],
    binaries=[
        ('C:\\Users\\Clara\\AppData\\Local\\pypoetry\\Cache\\virtualenvs\\playground-pv6Vx99u-py3.13\\Lib\\site-packages\\brainflow\\lib', 'brainflow/lib'),
    ],
    datas=[
        ('app/view/styles','styles'),
        ('app/Settings Files', 'Settings Files'),
        ('app/h5_session_files', 'h5_session_files')
    ],
    hiddenimports=['PyQt6', 'numpy', 'matplotlib', 'pyqtgraph', 'brainflow'],
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
    a.binaries,
    a.datas,
    [],
    name='MyLoad',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
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
