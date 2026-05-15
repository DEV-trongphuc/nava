import re
with open('demo_collection.html', 'r', encoding='utf-8') as f:
    c = f.read()
matches = re.findall(r'<button class="compare-btn"[^>]*>', c)
with open('test_btns_out.txt', 'w', encoding='utf-8') as f:
    for m in matches[:5]:
        f.write(m + '\n')
