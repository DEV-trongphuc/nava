import re

def main():
    with open('scratch/gmk_product.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print("=== Occurrences of mainProductAvailable ===")
    for idx, line in enumerate(lines):
        if 'mainProductAvailable' in line:
            print(f"Line {idx+1}: {line.strip()}")
            
    print("\n=== Occurrences of isSoldOut ===")
    for idx, line in enumerate(lines):
        if 'isSoldOut' in line:
            print(f"Line {idx+1}: {line.strip()}")

if __name__ == '__main__':
    main()
