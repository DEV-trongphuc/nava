import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/ssd24_live.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for idx, line in enumerate(lines):
    if "512GB" in line or "512" in line or "variant" in line or "512 GB" in line:
        print(f"Line {idx+1}: {line.strip()[:180]}")
