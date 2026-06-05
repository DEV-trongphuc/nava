import re

def main():
    with open('scratch/gmk_product.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    matches = [m.start() for m in re.finditer(r'NO SSD', content)]
    print(f"Total matches of 'NO SSD': {len(matches)}")
    for idx, pos in enumerate(matches):
        line_no = content[:pos].count('\n') + 1
        print(f"Match {idx+1}: line {line_no}")
        lines = content.splitlines()
        for i in range(max(0, line_no-3), min(len(lines), line_no+4)):
            safe_line = lines[i].encode('ascii', errors='backslashreplace').decode('ascii')
            print(f"  {i+1}: {safe_line}")

if __name__ == '__main__':
    main()
