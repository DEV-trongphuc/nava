import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

path = r"f:\BAO_SAPO\sapo_new\assets\style.css"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx in range(5600, min(5700, len(lines))):
    print(f"{idx+1}: {lines[idx].rstrip()}")
