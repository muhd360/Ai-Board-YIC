import os
import subprocess

def install_linux_dependencies():
    print("Creating a virtual environment...")
    venv_dir = "venv"
    subprocess.check_call(["python3", "-m", "venv", venv_dir])

    print("Activating the virtual environment...")
    pip_path = os.path.join(venv_dir, "bin", "pip")

    print("Installing Tesseract OCR...")
    subprocess.check_call(["sudo", "apt", "update"])
    subprocess.check_call(["sudo", "apt", "install", "-y", "tesseract-ocr"])

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

    print("Dependencies installed successfully in the virtual environment.")

if __name__ == "__main__":
    install_linux_dependencies()
