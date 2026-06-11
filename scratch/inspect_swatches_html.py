import os

def search_swatch():
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.bwt') or file.endswith('.html') or file.endswith('.js'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        for i, line in enumerate(lines):
                            if 'swatch' in line.lower() and ('option' in line.lower() or 'var ' in line.lower() or 'const ' in line.lower() or 'function' in line.lower() or 'select' in line.lower()):
                                print(f"{path}:{i+1}: {line.strip()}")
                except Exception as e:
                    pass

search_swatch()
