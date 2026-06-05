import os

results = []
for root, dirs, files in os.walk("."):
    if any(p in root for p in [".git", "node_modules", "scratch", ".gemini"]):
        continue
    for file in files:
        if file.endswith(('.js', '.css', '.bwt', '.html')):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                if "mew_collection_script" in content or "SearchFilter" in content:
                    results.append(path)
            except:
                pass

print(f"Files referencing mew_collection_script or SearchFilter: {results}")
