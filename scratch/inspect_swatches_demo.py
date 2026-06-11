with open('sapo_BWT_new/Templates/product.bwt', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'nava-bs-options-container' in line or 'bs-options-container' in line:
        print(f"Line {i+1}: {line.strip()}")
