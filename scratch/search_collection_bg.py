import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"f:\BAO_SAPO\sapo_new\build_demos.py", "r", encoding="utf-8") as f:
    text = f.read()

# Let's search inside the build_collection function (lines 89 to 1180) for any CSS rules setting background colors
import re
collection_func = text[text.find("def build_collection"):text.find("def build_product")]
style_blocks = re.findall(r'<style>.*?</style>', collection_func, re.DOTALL)
for idx, style in enumerate(style_blocks):
    print(f"Style Block {idx+1}:")
    for line in style.split('\n'):
        if "background" in line:
            print("  ", line.strip())
