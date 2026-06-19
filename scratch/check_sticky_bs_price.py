import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/ssd24_live.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("Searching for sticky-price and bs-price static definitions:")
for idx, line in enumerate(lines):
    if "sticky-price" in line or "bs-price" in line:
        print(f"Line {idx+1}: {line.strip()[:180]}")
