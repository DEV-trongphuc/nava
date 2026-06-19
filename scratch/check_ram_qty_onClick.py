import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/ram_live.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
# Tìm input có id="qtym"
idx = html.find('id="qtym"')
if idx != -1:
    print("Found qtym input context on RAM page:")
    print(html[idx-300:idx+500])
else:
    print("Not found qtym input on RAM page")
