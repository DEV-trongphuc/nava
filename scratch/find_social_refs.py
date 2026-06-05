import os
import re

results = []
for root, dirs, files in os.walk("."):
    if any(p in root for p in [".git", "node_modules", "scratch", ".gemini"]):
        continue
    for file in files:
        if file.endswith(('.js', '.css', '.bwt')):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                if "floating-social-wrapper" in content or "fabMainBtn" in content or "fab-menu" in content:
                    results.append(path)
            except:
                pass
print(f"Files with social wrapper: {results}")
