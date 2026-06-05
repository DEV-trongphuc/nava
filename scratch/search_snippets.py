import os

def main():
    root = 'sapo_BWT_new/snippets'
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            path = os.path.join(dirpath, f)
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                if 'cart-item-template' in content:
                    print(f"Found 'cart-item-template' in {path}")
            except Exception:
                pass

if __name__ == '__main__':
    main()
