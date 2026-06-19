import sys
sys.stdout.reconfigure(encoding='utf-8')

def find_in_file(filepath):
    print(f"\n--- Searching in {filepath} ---")
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    for idx, line in enumerate(lines):
        if "watch swatch radio" in line.lower() or "document.addeventlistener('change'" in line.lower():
            # In ra 10 dòng xung quanh
            start = max(0, idx - 2)
            end = min(len(lines), idx + 10)
            print(f"Occurence at Line {idx+1}:")
            for i in range(start, end):
                print(f"  {i+1}: {lines[i].rstrip()}")

find_in_file("sapo_BWT_new/Templates/product.bwt")
find_in_file("sapo_BWT_new/Templates/product_fixed.bwt")
