import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/ssd24_live.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("Searching for callback functions:")
for idx, line in enumerate(lines):
    if "selectcallback" in line.lower() or "onvariantselected" in line.lower():
        print(f"Line {idx+1}: {line.strip()[:180]}")
