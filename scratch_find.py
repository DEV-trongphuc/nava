import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

path = r"f:\BAO_SAPO\sapo_new\build_demos.py"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx in range(3189, min(3230, len(lines))):
    print(f"{idx+1}: {lines[idx].rstrip()}")
