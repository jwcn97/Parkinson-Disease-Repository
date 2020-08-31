# IO functions for test

# === Imports ===
import os

# === 'csv_files' Folder ===
def load_csv_files():
    """
    Loads csv files in 'csv_files' folder
    """
    csv_folder = "\\".join([os.getcwd(), "tests", "csv_files"])

    # Load files
    files = os.listdir(csv_folder)

    # Prepend strings with folder names
    files = ["\\".join([csv_folder, f]) for f in files]

    return files 