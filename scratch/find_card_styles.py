with open(r"f:\BAO_SAPO\sapo_new\sapo_BWT_new\Templates\collection.bwt", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "product-card" in line or "card-glow" in line:
        print(f"Line {i+1}: {line.strip()}")
