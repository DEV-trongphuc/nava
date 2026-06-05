def main():
    filepath = 'cart_page_original_utf8.html'
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for idx, line in enumerate(lines):
        if 'cart-item-template' in line:
            print(f"=== Line {idx+1} ===")
            for i in range(max(0, idx-10), min(len(lines), idx+20)):
                safe_line = lines[i].rstrip().encode('ascii', errors='backslashreplace').decode('ascii')
                print(f"{i+1}: {safe_line}")

if __name__ == '__main__':
    main()
