with open(r"f:\BAO_SAPO\sapo_new\build_demos.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "floating-social-wrapper" in line:
        print(f"Line {i+1}: {line.strip()}")
