import sys
from cx_Freeze import setup, Executable

# Include additional files and folders
build_exe_options = {
    "packages": ["os", "re", "sqlite3", "pdfplumber", "pandas", "tkinter", "selenium","json","sys","webdriver_manager.chrome"],
    "include_files": [
        "Profile 1",
        "chrome_user_data",
        "__pycache__"
    ],
    "build_exe": "build_app"
}

# Base for the executable
base = None
if sys.platform == "win32":
    base = "Win32GUI"
elif sys.platform == "darwin":
    base = None  # macOS applications typically do not need a base specification

setup(
    name="PDF to Web",
    version="3.0",
    description="Automate PDF to Web ",
    options={"build_exe": build_exe_options},
    executables=[
        Executable("main.py", base=base, target_name="main.exe",icon="appicon.ico"),
        Executable("settings.py", base=base, target_name="settings.exe",icon="settingsicon.ico")
    ]
)