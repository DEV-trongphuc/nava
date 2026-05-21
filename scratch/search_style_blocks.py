import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"f:\BAO_SAPO\sapo_new\build_demos.py", "r", encoding="utf-8") as f:
    text = f.read()

# Let's search for any occurrences of "odd", "even", "nth-child", "background" in style tags
import re
styles = re.findall(r'<style>.*?</style>', text, re.DOTALL)
print(f"Found {len(styles)} style blocks")
for idx, style in enumerate(styles):
    if any(k in style for k in ["background", "color", "nth", "even", "odd"]):
        print(f"--- Style Block {idx+1} ---")
        lines = style.split('\n')
        for line in lines:
            if any(k in line for k in ["background:", "background-color:", "nth-", "even", "odd"]):
                print(line.strip()[:150])
