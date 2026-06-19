import sys
sys.stdout.reconfigure(encoding='utf-8')

def find_in_file(filepath, query):
    print(f"\n--- Searching for '{query}' in {filepath} ---")
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    for idx, line in enumerate(lines):
        if query.lower() in line.lower() and ("innerText" in line or "textContent" in line or "innerHTML" in line):
            print(f"Line {idx+1}: {line.strip()}")

find_in_file("sapo_BWT_new/Templates/product.bwt", "selected-variant-price")
find_in_file("sapo_BWT_new/Templates/product.bwt", "priceEl")
find_in_file("sapo_BWT_new/Templates/product.bwt", "bsPriceEl")
find_in_file("sapo_BWT_new/Templates/product.bwt", "stickyPriceEl")
