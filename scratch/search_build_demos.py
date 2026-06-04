import re

with open('build_demos.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'collection' in line.lower() and ('html' in line or 'write' in line or 'template' in line):
        print(f"Line {i+1}: {line.strip()[:120]}")
