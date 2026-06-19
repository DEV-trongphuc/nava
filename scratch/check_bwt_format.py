import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("sapo_BWT_new/Templates/product.bwt", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("Searching for formatVietnameseCurrency in product.bwt:")
count = 0
for idx, line in enumerate(lines):
    if "formatvietnamesecurrency" in line.lower() or "animateprice" in line.lower() or "animatevalue" in line.lower():
        count += 1
        print(f"Line {idx+1}: {line.strip()[:180]}")

print(f"Total: {count}")
