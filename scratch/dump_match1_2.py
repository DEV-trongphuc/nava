import re

def main():
    with open('scratch/gmk_product.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    matches = [m.start() for m in re.finditer(r'data-dropdown-type="', content)]
    for idx in [0, 1]:
        if idx < len(matches):
            pos = matches[idx]
            start = max(0, pos - 200)
            end = min(len(content), pos + 1000)
            chunk = content[start:end]
            safe_chunk = chunk.encode('ascii', errors='backslashreplace').decode('ascii')
            print(f"Match {idx+1} near index {pos}:\n{safe_chunk}\n" + "-"*40)

if __name__ == '__main__':
    main()
