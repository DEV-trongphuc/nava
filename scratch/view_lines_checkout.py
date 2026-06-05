def main():
    filepath = 'sapo_BWT_new/Templates/product.bwt'
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    print("=== Lines 2988 to 3045 ===")
    for idx in range(2987, 3045):
        if idx < len(lines):
            line = lines[idx].rstrip('\r\n')
            safe_line = line.encode('ascii', errors='backslashreplace').decode('ascii')
            print(f"{idx+1}: {safe_line}")

if __name__ == '__main__':
    main()
