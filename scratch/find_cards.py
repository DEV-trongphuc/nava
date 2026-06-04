with open('build_demos.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's find occurrences of <div class="product-card">
start_idx = 0
while True:
    idx = content.find('product-card', start_idx)
    if idx == -1:
        break
    # Print 500 characters around this index
    print(f"--- MATCH AT INDEX {idx} ---")
    print(content[idx-100:idx+500])
    start_idx = idx + 12
    if start_idx > len(content) or start_idx > 200000: # limit to avoid giant output
        break
