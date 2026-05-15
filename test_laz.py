with open('demo_collection.html', 'r', encoding='utf-8') as f:
    c = f.read()
if 'Laz' in c or 'laz' in c:
    print('Lazada icon found')
else:
    print('Not found')
