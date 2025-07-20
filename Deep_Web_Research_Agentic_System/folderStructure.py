import os
import venv
import subprocess
from pathlib import Path
import platform

# Create virtual environment
venv_dir = "venv"
builder = venv.EnvBuilder(with_pip=True)
builder.create(venv_dir)
print(f"\n✅ Virtual environment created at: {os.path.abspath(venv_dir)}")

# Activation instructions
print("\n🔧 To activate the virtual environment, run:")
if platform.system() == "Windows":
    print("    .\\venv\\Scripts\\activate")
else:
    print("    source venv/bin/activate")

# File and folder structure
list_of_files = [
    ".GitHub/workflows/.gitkeep",
    "agent/__init__.py",
    "agent/agentic_pipeline.py",
    "config/__init__.py",
    "config/config.yaml",
    "prompt_library/__init__.py",
    "prompt_library/prompt.py",
    "tools/__init__.py",
    "utils/__init__.py",
    "logger/__init__.py",
    "logger/logger.py",
    "exception/__init__.py",
    "exception/exception.py",
    "templates/index.html",
    "statics/style.css",
    "experiments/notebook.ipynb",
    "outputs/",
    "save_documents/",
    "init_setup.sh",
    "requirements.lock.txt",
    "Dockerfile",
    "app.py",
    "setup.py",
    ".env",
    ".gitignore",
    "README.md",
]

print("\n Creating project structure...")
for filepath in list_of_files:
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    # Skip folder creation for trailing slashes
    if filepath.endswith("/"):
        continue

    if not path.exists():
        path.touch()
        print(f"  Created: {path}")
    else:
        print(f"  Already exists: {path}")

# Write boilerplate content to certain files
boilerplate = {
    "README.md": "# Project Title\n\nDescribe your project here.\n",
    ".gitignore": "venv/\n__pycache__/\n.env\n*.pyc\n",
    "app.py": 'print("Hello, world! Your app is ready.")\n',
}

for filename, content in boilerplate.items():
    file_path = Path(filename)
    if file_path.exists() and file_path.stat().st_size == 0:
        file_path.write_text(content)
        print(f"  Wrote boilerplate to: {filename}")

# Install requirements if file exists
requirements_file = Path("requirements.lock.txt")
if requirements_file.exists() and requirements_file.stat().st_size > 0:
    print("\n Installing dependencies from requirements.lock.txt...")
    pip_executable = (
        "venv\\Scripts\\pip.exe" if platform.system() == "Windows" else "venv/bin/pip"
    )
    subprocess.run([pip_executable, "install", "-r", str(requirements_file)])
    print(" Dependencies installed.")
else:
    print("\n  No requirements.lock.txt found or it's empty — skipping install.")

print("\n Setup complete!")
