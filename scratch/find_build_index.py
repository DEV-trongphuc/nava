with open(r"f:\BAO_SAPO\sapo_new\build_demos.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "def build_index" in line:
        print(f"Found build_index at line {i+1}: {line.strip()}")
    if "def build_all" in line:
        print(f"Found build_all at line {i+1}: {line.strip()}")
