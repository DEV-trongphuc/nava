def main():
    filepath = 'scratch/cart_style.css'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    import re
    matches = [m.start() for m in re.finditer(r'\.ux-card', content)]
    for idx, pos in enumerate(matches):
        print(f"=== Match {idx+1} ===")
        start = max(0, pos - 100)
        end = min(len(content), pos + 1000)
        print(content[start:end])

if __name__ == '__main__':
    main()
