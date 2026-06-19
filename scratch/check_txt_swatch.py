import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/live_scripts.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines in live_scripts.txt: {len(lines)}")
count = 0
for idx, line in enumerate(lines):
    if "swatch" in line.lower():
        count += 1
        if count <= 40: # in tối đa 40 dòng để tránh loãng
            print(f"Line {idx+1}: {line.strip()[:180]}")

print(f"Found total {count} occurrences of 'swatch' in live_scripts.txt.")
