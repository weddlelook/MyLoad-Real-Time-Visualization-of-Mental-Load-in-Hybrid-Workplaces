import os
import sys
from pathlib import Path
import subprocess
from PyInstaller import __main__ as pyinstaller

def get_project_root():
    return Path(sys.argv[0]).parent.resolve()

def get_poetry_venv_path():
    """Get the Poetry virtual environment path dynamically."""
    try:
        venv_path = subprocess.check_output(["poetry", "env", "info", "--path"], text=True).strip()
        return Path(venv_path)
    except subprocess.CalledProcessError:
        print("Error: Could not determine Poetry virtual environment path.")
        sys.exit(1)

# Get paths
poetry_venv_dir = get_poetry_venv_path()
project_root = get_project_root()
brainflow_lib_dir = poetry_venv_dir / "lib/python3.13/site-packages/brainflow/lib"  # Adjust for your Python version

# Add BrainFlow dynamic libraries
brainflow_libs = [
    str(brainflow_lib_dir / "libBoardController.so"),
    str(brainflow_lib_dir / "libDataHandler.so"),  # Make sure to include libDataHandler.so
]

# Collect all binaries to include in PyInstaller package
binaries = [(lib, "brainflow/lib/") for lib in brainflow_libs]

# Create the PyInstaller analysis object
a = Analysis(
    [str(project_root / 'app' / '__main__.py')],
    pathex=[str(project_root), str(poetry_venv_dir)],
    binaries=binaries,  # Include BrainFlow shared libraries dynamically
    datas=[
        (str(project_root / 'app'), 'app'),
        ('app/res/styles', 'styles'),
        ('app/res/setting_files', 'setting_files'),
        ('app/res/h5_session_files', 'h5_session_files'),
    ],
    hiddenimports=['PyQt6', 'numpy', 'matplotlib', 'pyqtgraph', 'brainflow'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

# Generate the PyInstaller .exe file
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
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
