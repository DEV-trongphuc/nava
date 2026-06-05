def main():
    filepath = 'build_demos.py'
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"=== Search results in {filepath} ===")
    for idx, line in enumerate(lines):
        if 'sapo_BWT' in line or 'Templates' in line or 'product' in line:
            print(f"Line {idx+1}: {line.strip()[:100]}")

if __name__ == '__main__':
    main()
