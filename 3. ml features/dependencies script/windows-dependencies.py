import os
import subprocess

def install_windows_dependencies():
    print("Creating a virtual environment...")
    venv_dir = "venv"
    subprocess.check_call(["python", "-m", "venv", venv_dir])

    print("Activating the virtual environment...")
    activate_script = os.path.join(venv_dir, "Scripts", "activate")
    pip_path = os.path.join(venv_dir, "Scripts", "pip")

    if not os.path.exists(activate_script):
        print(f"Virtual environment activation script not found at {activate_script}.")
        return

    print("Installing Python dependencies in the virtual environment...")
    dependencies = [
        "moviepy",
        "pydub",
        "speechrecognition",
        "transformers",
        "langdetect",
        "googletrans==4.0.0-rc1",
        "fpdf",
        "pytesseract",
    ]

    for package in dependencies:
        subprocess.check_call([pip_path, "install", package])

    print("Installing Tesseract OCR...")
    tesseract_installer_path = "<path_to_installer>\\tesseract-ocr-w64-setup-v5.3.0.20221222.exe"

    if not os.path.exists(tesseract_installer_path):
        print(f"Tesseract installer not found at {tesseract_installer_path}. Please update the path.")
        return

    subprocess.check_call(["start", "/WAIT", tesseract_installer_path], shell=True)

    print("Dependencies installed successfully in the virtual environment.")

if __name__ == "__main__":
    install_windows_dependencies()
