def main():
    with open('scratch/gmk_product.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for idx in range(3295, 3465):
        if idx < len(lines):
            line = lines[idx].rstrip('\r\n')
            # replace non-ascii characters with safe representation
            safe_line = line.encode('ascii', errors='backslashreplace').decode('ascii')
            print(f"{idx+1}: {safe_line}")

if __name__ == '__main__':
    main()
