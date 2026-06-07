with open(r"f:\BAO_SAPO\sapo_new\sapo_BWT_new\Templates\product.bwt", "r", encoding="utf-8") as f:
    content = f.read()

idx = 117868
snippet = content[idx-500:idx+800]
with open(r"f:\BAO_SAPO\sapo_new\scratch\price_match_2.txt", "w", encoding="utf-8") as out:
    out.write(snippet)
print("Snippet written successfully!")
