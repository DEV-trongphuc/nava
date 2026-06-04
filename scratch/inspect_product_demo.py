import re

def inspect_product():
    with open("f:\\BAO_SAPO\\sapo_new\\demo_product.html", "r", encoding="utf-8") as f:
        content = f.read()
        
    targets = ["Số lượng", "12.390.000", "price", "product-form", "prod-info", "custom-select", "specs"]
    
    with open("scratch/product_inspect.txt", "w", encoding="utf-8") as out:
        out.write(f"File size: {len(content)} chars\n")
        for t in targets:
            matches = [m.start() for m in re.finditer(re.escape(t), content, re.IGNORECASE)]
            out.write(f"Search for '{t}': found {len(matches)} matches\n")
            if matches:
                first_match = matches[0]
                start = max(0, first_match - 200)
                end = min(len(content), first_match + 800)
                out.write(f"Snippet near match of '{t}':\n")
                out.write(content[start:end])
                out.write("\n" + "="*50 + "\n")
                
    print("Done! Output written to scratch/product_inspect.txt")

inspect_product()
