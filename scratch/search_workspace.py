def main():
    filepath = 'sapo_BWT_new/Templates/product.bwt'
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"=== Occurrences of isDefaultRam in {filepath} ===")
    for idx, line in enumerate(lines):
        if 'isDefaultRam' in line:
            print(f"Line {idx+1}: {line.strip()}")

if __name__ == '__main__':
    main()
