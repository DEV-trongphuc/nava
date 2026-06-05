def main():
    filepath = 'build_demos.py'
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for r in [(3690, 3720), (3925, 4010)]:
        print(f"=== Lines {r[0]} to {r[1]} ===")
        for idx in range(r[0]-1, r[1]):
            if idx < len(lines):
                line = lines[idx].rstrip('\r\n')
                safe_line = line.encode('ascii', errors='backslashreplace').decode('ascii')
                print(f"{idx+1}: {safe_line}")

if __name__ == '__main__':
    main()
