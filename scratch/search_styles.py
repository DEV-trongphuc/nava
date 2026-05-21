import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"f:\BAO_SAPO\sapo_new\build_demos.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "product-card" in line or "background" in line or "style=" in line:
        if any(keyword in line for keyword in ["product-card", "background", "linear-gradient", "xen kẻ", "xen kẽ", "bg-", "blue", "green"]):
            print(f"{i+1}: {line.strip()[:150]}")
