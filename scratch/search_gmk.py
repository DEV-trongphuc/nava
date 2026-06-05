import re

def main():
    with open('scratch/gmk_product.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("File length:", len(content))
    
    queries = ['mainProductAvailable', 'BizwebAnalytics', 'window.', 'available', 'Còn hàng', 'MUA NGAY', '0đ']
    for q in queries:
        matches = [m.start() for m in re.finditer(re.escape(q), content, re.IGNORECASE)]
        print(f"Query '{q}': {len(matches)} matches")
        if matches:
            # print first match surrounding context
            start = max(0, matches[0] - 50)
            end = min(len(content), matches[0] + 50)
            print(f"  First match context: ... {repr(content[start:end])} ...")

if __name__ == '__main__':
    main()
