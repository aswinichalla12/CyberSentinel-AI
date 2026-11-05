
import sys
import importlib.metadata

print("Python version:", sys.version)
print("Python executable:", sys.executable)

packages = [
    "pandas",
    "numpy",
    "scikit-learn",
    "matplotlib",
    "seaborn",
    "streamlit",
    "joblib",
    "requests"
]

print("\nChecking installed packages:\n")

for package in packages:
    try:
        version = importlib.metadata.version(package)
        print(f"{package}: Installed ({version})")
    except importlib.metadata.PackageNotFoundError:
        print(f"{package}: NOT INSTALLED")

print("\nEnvironment check completed.")
