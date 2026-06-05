import re

with open('sapo_BWT_new/Templates/product.bwt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'productContent' in line or 'specs_content' in line or 'split' in line:
        clean_line = line.strip().encode('ascii', 'ignore').decode()
        print(f"Line {i}: {clean_line}")
