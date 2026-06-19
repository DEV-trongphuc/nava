import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/ssd24_live.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("Searching for buy buttons JS logic:")
for idx, line in enumerate(lines):
    if "btn-buy-now" in line or "btnBuyNow" in line or "global-product-contact-only" in line:
        print(f"Line {idx+1}: {line.strip()[:180]}")
