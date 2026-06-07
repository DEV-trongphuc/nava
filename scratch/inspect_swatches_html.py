with open(r"f:\BAO_SAPO\sapo_new\sapo_BWT_new\Templates\product.bwt", "r", encoding="utf-8") as f:
    content = f.read()

idx = 71406
snippet = content[idx-1000:idx+4000]
with open(r"f:\BAO_SAPO\sapo_new\scratch\swatch_render.txt", "w", encoding="utf-8") as out:
    out.write(snippet)
print("Snippet written successfully!")
