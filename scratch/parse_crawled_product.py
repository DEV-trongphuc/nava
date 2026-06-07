with open(r"C:\Users\AD\.gemini\antigravity-ide\brain\c67fc15a-2f7f-4635-8abd-f2a4ed79f6c7\.system_generated\steps\3588\content.md", "r", encoding="utf-8") as f:
    content = f.read()

import re

scripts = [m.start() for m in re.finditer("<script", content)]
print("Total scripts in crawled page:", len(scripts))

with open(r"f:\BAO_SAPO\sapo_new\scratch\crawled_scripts.txt", "w", encoding="utf-8") as out:
    for idx in scripts:
        out.write(content[idx:idx+350])
        out.write("\n=========================================\n")
print("Written scripts to crawled_scripts.txt")
