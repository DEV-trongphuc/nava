with open('demo_collection.html', 'r', encoding='utf-8') as f:
    c = f.read()
print('count:', c.count('id="compare-bar"'))
