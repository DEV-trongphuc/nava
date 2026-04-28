import re

with open('assets/main.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Replace limit=10 with limit=6 in the URL
js_content = js_content.replace('limit=10&offset=0', 'limit=6&offset=0')

with open('assets/main.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Updated URL limit to 6.")
