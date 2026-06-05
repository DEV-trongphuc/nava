def main():
    with open('scratch/mew_cart.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("mew_cart.js length:", len(content))
    
    import re
    # search for remove or js-remove-item-cart or Xoa or X\u00f3a
    queries = ['js-remove-item-cart', 'remove', 'Xóa', 'X\\u00f3a', 'Xoa']
    for q in queries:
        matches = [m.start() for m in re.finditer(re.escape(q), content, re.IGNORECASE)]
        print(f"Query '{q}': {len(matches)} matches")
        for pos in matches[:5]:
            start = max(0, pos - 100)
            end = min(len(content), pos + 100)
            print(f"  Context: {repr(content[start:end])}")

if __name__ == '__main__':
    main()
