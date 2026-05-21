import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"f:\BAO_SAPO\sapo_new\build_demos.py", "r", encoding="utf-8") as f:
    content = f.read()

# Let's search for "product-grid" or where product-cards are rendered in build_collection
pos = content.find("build_collection")
if pos != -1:
    print("Found build_collection at character:", pos)
    # let's find product-grid within build_collection
    grid_pos = content.find("class=\"product-grid\"", pos)
    if grid_pos != -1:
        print("Found product-grid at character:", grid_pos)
        print(content[grid_pos:grid_pos+2000])
