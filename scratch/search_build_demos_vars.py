def main():
    filepath = 'build_demos.py'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    import re
    queries = ['isSoldOut', 'mainProductAvailable']
    for q in queries:
        matches = [m.start() for m in re.finditer(q, content)]
        print(f"Total matches of '{q}' in build_demos.py: {len(matches)}")
        for idx, pos in enumerate(matches):
            line_no = content[:pos].count('\n') + 1
            print(f"  Match {idx+1}: line {line_no}")

if __name__ == '__main__':
    main()
