import re

file_path = 'f:/BAO_SAPO/sapo_new/assets/style.css'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's find all rules containing product-img or hover on product-card
lines = content.split('\n')
print(f"Total lines in style.css: {len(lines)}")

for idx, line in enumerate(lines, 1):
    if 'product-img' in line or 'card-image-wrap' in line:
        print(f"Line {idx}: {line.strip()}")
