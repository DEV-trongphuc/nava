def main():
    with open('scratch/gmk_product.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for idx in range(2795, 2955):
        if idx < len(lines):
            line = lines[idx].rstrip('\r\n')
            safe_line = line.encode('ascii', errors='backslashreplace').decode('ascii')
            print(f"{idx+1}: {safe_line}")

if __name__ == '__main__':
    main()
