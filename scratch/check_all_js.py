import os
import subprocess
import sys

def check_file(filepath):
    if filepath.endswith('.js'):
        res = subprocess.run(['node', '-c', filepath], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"Syntax error in {filepath}:")
            print(res.stderr)
            return False
    return True

def main():
    root = r"f:\BAO_SAPO\sapo_new"
    all_ok = True
    for dirpath, _, filenames in os.walk(root):
        if '.git' in dirpath or 'node_modules' in dirpath:
            continue
        for f in filenames:
            if f.endswith('.js'):
                path = os.path.join(dirpath, f)
                if not check_file(path):
                    all_ok = False
    if all_ok:
        print("All JS files are syntax valid.")
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
