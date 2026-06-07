with open(r"f:\BAO_SAPO\sapo_new\sapo_BWT_new\Templates\product.bwt", "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find("function syncSwatches")
if idx != -1:
    snippet = content[idx:idx+15000]
    with open(r"f:\BAO_SAPO\sapo_new\scratch\sync_swatches_snippet.txt", "w", encoding="utf-8") as out:
        out.write(snippet)
    print("Snippet written successfully!")
else:
    print("function syncSwatches not found!")
