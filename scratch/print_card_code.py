import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"f:\BAO_SAPO\sapo_new\build_demos.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx in range(498, 590):
    print(f"{idx+1}: {lines[idx]}", end="")
