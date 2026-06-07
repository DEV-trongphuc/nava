import re

with open(r"f:\BAO_SAPO\sapo_new\sapo_BWT_new\Templates\product.bwt", "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find("function syncSwatches")
if idx != -1:
    script_end = content.find("</script>", idx)
    sync_func = content[idx:script_end]
    
    with open(r"f:\BAO_SAPO\sapo_new\scratch\sync_swatches_dom_updates.txt", "w", encoding="utf-8") as out:
        out.write("Updates to DOM in syncSwatches:\n")
        for m in re.finditer(r'(innerText|innerHTML|textContent|html|text|val)\s*=', sync_func):
            start = max(0, m.start() - 100)
            end = min(len(sync_func), m.start() + 200)
            out.write("---\n")
            out.write(sync_func[start:end])
            out.write("\n")
    print("Done writing to file!")
else:
    print("syncSwatches not found!")
