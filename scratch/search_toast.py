import os

def main():
    root = '.'
    for dirpath, _, filenames in os.walk(root):
        if '.git' in dirpath or '__pycache__' in dirpath:
            continue
        for f in filenames:
            path = os.path.join(dirpath, f)
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                if 'toast-container' in content:
                    print(f"Found 'toast-container' in {path}")
            except Exception:
                pass

if __name__ == '__main__':
    main()
