with open("assets/style.css", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer(r'floating-social-wrapper|fab-menu|fab-main', content, re.IGNORECASE)]
with open("scratch/social_css.txt", "w", encoding="utf-8") as out:
    out.write(f"Found {len(matches)} occurrences:\n")
    for m in matches:
        out.write(content[max(0, m-200):m+400])
        out.write("\n" + "="*40 + "\n")
print("Done!")
