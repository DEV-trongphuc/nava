import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

search_dir = r"f:\BAO_SAPO\sapo_new"
for root, dirs, files in os.walk(search_dir):
    for file in files:
        if file.endswith((".bwt", ".html", ".txt")):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                if "floating-social-wrapper" in content:
                    print(f"Found in {path}")
            except Exception as e:
                pass
