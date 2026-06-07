import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

def find_pattern(pattern):
    results = []
    for root, dirs, files in os.walk('.'):
        if '.git' in root or '.gemini' in root or 'node_modules' in root:
            continue
        for file in files:
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    for i, line in enumerate(f, 1):
                        if pattern in line:
                            results.append((path, i, line.strip()))
            except Exception:
                try:
                    with open(path, 'r', encoding='latin-1') as f:
                        for i, line in enumerate(f, 1):
                            if pattern in line:
                                results.append((path, i, line.strip()))
                except Exception:
                    pass
    for r in results[:100]:
        print(f"{r[0]}:{r[1]}: {r[2]}")

if __name__ == '__main__':
    find_pattern('back-to-top')
