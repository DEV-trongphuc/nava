with open('demo_collection.html', 'r', encoding='utf-8') as f:
    c = f.read()
print('compare-bar:', 'id="compare-bar"' in c)
print('compare-slots:', 'id="compare-slots"' in c)
print('compare-count:', 'id="compare-count"' in c)
print('compare-submit:', 'id="compare-submit"' in c)
