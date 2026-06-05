import re

def main():
    with open('scratch/gmk_product.html', 'r', encoding='utf-8') as f:
        content = f.read()
        
    print("Length of gmk_product.html:", len(content))
    
    matches = [m.start() for m in re.finditer(r'ux-card', content)]
    print(f"Total matches of 'ux-card': {len(matches)}")
    for idx, pos in enumerate(matches):
        line_no = content[:pos].count('\n') + 1
        print(f"Match {idx+1}: line {line_no}")
        lines = content.splitlines()
        for i in range(max(0, line_no-3), min(len(lines), line_no+4)):
            print(f"  {i+1}: {lines[i]}")

if __name__ == '__main__':
    main()
