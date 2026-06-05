def main():
    filepath = 'build_demos.py'
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    print("=== Style lines in build_cart_page ===")
    for idx in range(5021, 5130):
        if idx < len(lines):
            safe_line = lines[idx].rstrip().encode('ascii', errors='backslashreplace').decode('ascii')
            print(f"{idx+1}: {safe_line}")

if __name__ == '__main__':
    main()
