with open('demo_collection.html', 'r', encoding='utf-8') as f:
    c = f.read()
idx = c.find('id="compare-bar"')
with open('test_body_out.txt', 'w', encoding='utf-8') as f:
    f.write(f'compare-bar is at index: {idx}\n')
    f.write(f'Total length: {len(c)}\n')
    f.write('End of file snippet:\n')
    f.write(c[-500:])
