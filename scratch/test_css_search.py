import re

with open(r'f:\BAO_SAPO\sapo_new\assets\style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# search for classes containing 'back' or 'top'
matches = re.findall(r'\.[a-zA-Z0-9_-]*(?:back|top)[a-zA-Z0-9_-]*\s*\{[^}]*\}', css, re.IGNORECASE)
for m in matches[:20]:
    print(m)
