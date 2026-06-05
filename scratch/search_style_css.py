def main():
    filepath = 'assets/style.css'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Length of assets/style.css:", len(content))
    import re
    matches = [m.start() for m in re.finditer(r'ux-card', content, re.IGNORECASE)]
    print("Matches of 'ux-card':", len(matches))
    for m in matches[:10]:
        start = max(0, m - 100)
        end = min(len(content), m + 100)
        print(repr(content[start:end]))

if __name__ == '__main__':
    main()
