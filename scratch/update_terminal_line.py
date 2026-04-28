import re

with open('assets/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

old_cmd = '<span class="t-cmd">run benchmark --device asus-nuc-15-pro</span>'
new_cmd = '<span class="t-cmd">run benchmark --device asus-nuc-ai-350</span>'

old_cpu_line = "{ cls: 't-out', html: '[INFO] CPU: AMD Ryzen AI 7 350 8C/16T max 5.0Ghz' },"
new_lines = "{ cls: 't-out', html: '[INFO] Model: NUC AI 350 (PN54)' },\n        { cls: 't-out', html: '[INFO] CPU: AMD Ryzen AI 7 350 8C/16T max 5.0Ghz' },"

content = content.replace(old_cmd, new_cmd)
content = content.replace(old_cpu_line, new_lines)

with open('assets/main.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Main.js updated successfully!")
