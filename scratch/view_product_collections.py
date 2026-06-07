import re

paths = [
    r"f:\BAO_SAPO\sapo_new\sapo_BWT_new\snippets\breadcrumb.bwt",
    r"f:\BAO_SAPO\sapo_new\sapo_BWT_new\layout\theme.bwt"
]

for path in paths:
    print("\n========================================")
    print("FILE:", path)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    matches = [m.start() for m in re.finditer("product.collections", content)]
    for idx in matches:
        start = max(0, idx - 150)
        end = min(len(content), idx + 250)
        print("MATCH:")
        print(content[start:end])
