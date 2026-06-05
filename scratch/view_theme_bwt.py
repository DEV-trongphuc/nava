def main():
    filepath = 'sapo_BWT_new/layout/theme.bwt'
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for idx, line in enumerate(lines):
        if 'toast-container' in line:
            print(f"=== Line {idx+1} ===")
            for i in range(max(0, idx-5), min(len(lines), idx+30)):
                safe_line = lines[i].rstrip('\r\n').encode('ascii', errors='backslashreplace').decode('ascii')
                print(f"{i+1}: {safe_line}")

if __name__ == '__main__':
    main()
