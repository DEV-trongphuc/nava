import sys
import os
sys.stdout.reconfigure(encoding='utf-8')

style_css_path = r"f:\BAO_SAPO\sapo_new\assets\style.css"
if os.path.exists(style_css_path):
    with open(style_css_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            if "product-card" in line or "card-image-wrap" in line:
                print(f"{i}: {line.strip()[:120]}")
else:
    print("style.css does not exist")
