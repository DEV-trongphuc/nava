import os

def main():
    root = 'sapo_BWT_new'
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            rel = os.path.relpath(os.path.join(dirpath, f), root)
            print(rel)

if __name__ == '__main__':
    main()
