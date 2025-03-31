# Building an Excecutable

## Requirements

- You have installed poetry and all dependencies in the poetry toml (via `poetry install`)
- You have run the complete application at least once before and bothe the Hdf5-File an Settings folder have been created (via `poetry run python -m app`)


##  **Building the Executable (Linux & Windows)**
We use PyInstaller to package MyLoad as a standalone application.

### 1️⃣ **Clean Previous Builds (if any)**
```sh
# Linux/macOS
rm -rf build dist MyLoad.spec

# Windows (PowerShell)
Remove-Item -Recurse -Force build, dist, MyLoad.spec
```

### 2️⃣ **Build the Executable**
```sh
poetry run pyinstaller --clean -y MyLoad.spec
```

### 3️⃣ **Run the Built Application**
- **Linux/macOS:**
  ```sh
  cd dist/MyLoad
  ./MyLoad
  ```
- **Windows:**
  ```powershell
  cd dist\MyLoad
  .\MyLoad.exe
  ```

## 🛠 **Troubleshooting**
### 🔹 "ModuleNotFoundError: No module named 'app'"
Make sure you are running the script from the root directory of the project.

### 🔹 "FileNotFoundError: libBoardController.so is missing"
If PyInstaller does not package the required BrainFlow shared library, ensure it is included in `MyLoad.spec`:
```python
binaries=[
    ("/path/to/brainflow/lib/libBoardController.so", "brainflow/lib/")
    ('/path/to/brainflow/lib/libDataHandler.so', 'brainflow/lib/libDataHandler.so')
]
```
Manually copy the file if necessary:
```sh
cp /path/to/brainflow/lib/libBoardController.so dist/MyLoad/brainflow/lib/
```

### 🔹 "Error: Could not determine Poetry virtual environment path"
Run:
```sh
poetry env info --path
```
Ensure Poetry is correctly installed and that you are in the project directory.

Happy coding! 🚀

