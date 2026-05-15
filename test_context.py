with open('demo_collection.html', 'r', encoding='utf-8') as f:
    c = f.read()
idx = c.find('id="compare-bar"')
print(c[idx-200:idx+200])
