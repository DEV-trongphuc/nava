import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"f:\BAO_SAPO\sapo_new\build_demos.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Let's print from lines 430 to 520
for idx in range(430, 520):
    if idx < len(lines):
        print(f"{idx+1}: {lines[idx]}", end="")
