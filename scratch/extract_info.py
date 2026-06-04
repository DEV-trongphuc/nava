import re

with open("demo_product.html", "r", encoding="utf-8") as f:
    content = f.read()

# Find the start of nava-product-layout or product-detail-container
start_idx = content.find("class=\"nava-product-layout\"")
if start_idx == -1:
    start_idx = content.find("nava-prod-info")

if start_idx != -1:
    # Get 30000 characters around this area to see the layout
    snippet = content[max(0, start_idx - 1000):start_idx + 25000]
    with open("scratch/extracted_product_info.html", "w", encoding="utf-8") as out:
        out.write(snippet)
    print("Found and extracted snippet!")
else:
    print("Could not find nava-product-layout or nava-prod-info!")
