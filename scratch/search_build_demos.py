def main():
    filepath = 'build_demos.py'
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"=== Occurrences of syncSwatches in {filepath} ===")
    for idx, line in enumerate(lines):
        if 'syncSwatches' in line:
            # print up to 50 chars of the line
            print(f"Line {idx+1}: {line.strip()[:100]}")

if __name__ == '__main__':
    main()
