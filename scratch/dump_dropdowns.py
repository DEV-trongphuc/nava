import re

def main():
    with open('scratch/gmk_product.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # find dropdown containers
    pattern = r'(<div[^>]*data-dropdown-type="[^"]+"[^>]*>.*?</div>)'
    # Since dropdowns might span multiple lines, let's write a simple regex or search around indices
    matches = [m.start() for m in re.finditer(r'data-dropdown-type="', content)]
    for idx, pos in enumerate(matches):
        start = max(0, pos - 100)
        end = min(len(content), pos + 1000)
        chunk = content[start:end]
        safe_chunk = chunk.encode('ascii', errors='backslashreplace').decode('ascii')
        print(f"Match {idx+1} near index {pos}:\n{safe_chunk}\n" + "-"*40)

if __name__ == '__main__':
    main()
