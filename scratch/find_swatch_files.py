import os

def list_all_files():
    for root, dirs, files in os.walk('.'):
        for file in files:
            full_path = os.path.join(root, file)
            if 'swatch' in file.lower() or 'swatch' in root.lower():
                print(f"File matching swatch: {full_path}")

list_all_files()
