import re

def main():
    with open('scratch/live_cart.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("File length:", len(content))
    
    # 1. Search for 'ux-card' in HTML
    matches = [m.start() for m in re.finditer(r'ux-card', content)]
    print(f"Occurrences of 'ux-card': {len(matches)}")
    for idx, pos in enumerate(matches):
        line_no = content[:pos].count('\n') + 1
        print(f"  Match {idx+1}: line {line_no}")
        lines = content.splitlines()
        for i in range(max(0, line_no-3), min(len(lines), line_no+4)):
            print(f"    {i+1}: {lines[i]}")

    # 2. Search for any stylesheet links in live HTML
    links = re.findall(r'<link[^>]*href="([^"]+)"[^>]*>', content)
    print("\nStylesheets loaded in live cart HTML:")
    for l in links:
        if 'css' in l:
            print("  ", l)

if __name__ == '__main__':
    main()
