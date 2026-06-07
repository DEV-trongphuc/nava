with open(r"f:\BAO_SAPO\sapo_new\sapo_BWT_new\Templates\product.bwt", "r", encoding="utf-8") as f:
    content = f.read()

def print_snippet(title, index, length=600):
    print(f"\n=== {title} ===")
    start = max(0, index - 200)
    end = min(len(content), index + length)
    print(content[start:end])

# Print swatch snippet
import re
swatch_matches = [m.start() for m in re.finditer("swatch", content, re.IGNORECASE)]
if swatch_matches:
    print_snippet("SWATCH MATCH 1", swatch_matches[0], 1200)

# Print related product snippet
relate_matches = [m.start() for m in re.finditer("m_relate_product", content, re.IGNORECASE)]
if relate_matches:
    print_snippet("RELATED PRODUCT MATCH", relate_matches[0], 1000)
