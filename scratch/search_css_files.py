import os
import re

def main():
    root = '.'
    for dirpath, _, filenames in os.walk(root):
        # skip git and pycache
        if '.git' in dirpath or '__pycache__' in dirpath:
            continue
        for f in filenames:
            if f.endswith('.css'):
                path = os.path.join(dirpath, f)
                try:
                    with open(path, 'r', encoding='utf-8') as file:
                        content = file.read()
                    if 'ux-card' in content:
                        print(f"Found 'ux-card' in {path}")
                except Exception as e:
                    pass

if __name__ == '__main__':
    main()
