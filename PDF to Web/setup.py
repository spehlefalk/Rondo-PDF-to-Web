import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["selenium"],
    "include_files": ["chromedriver.exe"]  # Include your chromedriver executable
}

# Base for the executable
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "PDF to Web",
    version = "1.0",
    description = "",
    options = {"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base, icon="9637c5ff-cdf0-44d4-ad44-f1c8cc8b54a8 (1).ico")]
)
