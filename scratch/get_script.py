with open("demo_product.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer(r'function selectVariantDropdown', content, re.IGNORECASE)]
if matches:
    start = matches[0]
    # search for next </script>
    end = content.find("</script>", start)
    if end != -1:
        with open("scratch/dropdown_script_block.js", "w", encoding="utf-8") as out:
            out.write(content[start:end])
        print("Script block extracted!")
else:
    print("Not found!")
