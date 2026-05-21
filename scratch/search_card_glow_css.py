import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"f:\BAO_SAPO\sapo_new\build_demos.py", "r", encoding="utf-8") as f:
    text = f.read()

# Let's search for all CSS blocks containing card-glow
import re
for m in re.finditer(r"\.card-glow\s*\{[^}]*\}", text):
    print(m.group(0))
