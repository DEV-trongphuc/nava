import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/ssd24_live.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("Searching for frequently-buy-together:")
count = 0
for idx, line in enumerate(lines):
    if "frequently-buy-together" in line.lower() or "fbt" in line.lower():
        count += 1
        print(f"Line {idx+1}: {line.strip()[:180]}")

print(f"Total occurrences: {count}")
