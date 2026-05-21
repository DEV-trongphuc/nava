import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"f:\BAO_SAPO\sapo_new\assets\style.css", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx in range(933, 1025):
    if idx < len(lines):
        print(f"{idx+1}: {lines[idx]}", end="")
