import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("sapo_BWT_new/Templates/product.bwt", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("Searching for dispatchEvent in product.bwt:")
count = 0
for idx, line in enumerate(lines):
    if "dispatchevent" in line.lower():
        count += 1
        print(f"Line {idx+1}: {line.strip()[:180]}")

print(f"Total occurrences: {count}")
