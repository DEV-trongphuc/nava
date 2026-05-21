import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"f:\BAO_SAPO\sapo_new\build_demos.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines, 1):
    if 'class="product-card"' in line:
        # print the line and the next 10 lines
        print(f"--- Line {i} ---")
        for j in range(i-1, i+15):
            if j < len(lines):
                print(f"{j+1}: {lines[j].strip()}")
