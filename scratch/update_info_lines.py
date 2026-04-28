import re

with open('assets/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("[INFO] CPU: Intel Core Ultra 5 225H", "[INFO] CPU: AMD Ryzen AI 7 350 8C/16T max 5.0Ghz")
content = content.replace("[INFO] RAM: DDR5 5600MHz SODIMM", "[INFO] RAM: 2x DDR5 5600 tối đa 128GB")
content = content.replace("[INFO] GPU: Intel Arc Graphics", "[INFO] GPU: AMD Radeon™ 860M")

with open('assets/main.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated 3 INFO lines in main.js")
