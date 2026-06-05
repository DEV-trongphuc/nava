import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open(r"f:\BAO_SAPO\sapo_new\assets\main.js", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "tối đa 2 sản phẩm" in line or "alert(" in line or "compareList.length" in line:
        if any(k in line for k in ["alert", "compareList", "length", "limit"]):
            print(f"Line {i+1}: {line.strip()}")
