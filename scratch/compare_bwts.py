import difflib
import sys

sys.stdout.reconfigure(encoding='utf-8')

def read_clean(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return [l.strip() + "\n" for l in lines if l.strip()]

bwt = read_clean("sapo_BWT_new/Templates/product.bwt")
fixed = read_clean("sapo_BWT_new/Templates/product_fixed.bwt")

print(f"Cleaned product.bwt lines: {len(bwt)}")
print(f"Cleaned product_fixed.bwt lines: {len(fixed)}")

diff = list(difflib.unified_diff(fixed, bwt, fromfile="product_fixed.bwt", tofile="product.bwt", n=2))
print(f"Total clean diff lines: {len(diff)}")
for line in diff[:100]:
    sys.stdout.write(line)
