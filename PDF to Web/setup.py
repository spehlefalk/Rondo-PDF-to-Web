import sys
from cx_Freeze import setup, Executable

# Include additional files and folders
build_exe_options = {
    "packages": ["os", "re", "sqlite3", "pdfplumber", "pandas", "tkinter", "selenium"],
    "include_files": [
        "Profile 1",
        "chrome_user_data",
        "__pycache__"
    ]
}

# Base for the executable
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Define the executables for Windows and Mac
executables = [
    Executable("main.py", base=base, icon="appicon.ico")
]

# Setup configuration
setup(
    name="PDF to Web",
    version="2.0",
    description="Automate PDF to Web tasks",
    options={"build_exe": build_exe_options},
    executables=executables
)
