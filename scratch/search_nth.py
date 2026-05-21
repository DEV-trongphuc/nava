import sys
import os
sys.stdout.reconfigure(encoding='utf-8')

for root, dirs, files in os.walk(r"f:\BAO_SAPO\sapo_new"):
    if ".git" in root or "__pycache__" in root:
        continue
    for file in files:
        if file.endswith((".html", ".css", ".bwt")):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for i, line in enumerate(f, 1):
                        if ":nth-" in line:
                            print(f"{path}:{i}: {line.strip()[:120]}")
            except Exception as e:
                pass
