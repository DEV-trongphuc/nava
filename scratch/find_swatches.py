import os

def find_files():
    for root, dirs, files in os.walk('.'):
        for file in files:
            if 'swatch' in file.lower() or file.endswith('.bwt') or file.endswith('.html'):
                full_path = os.path.join(root, file)
                if 'swatch' in file.lower():
                    print(f"Found swatch file: {full_path}")
                # check file content
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if 'swatch' in content.lower() or 'ddr5' in content.lower():
                            if 'Templates' in root or 'snippets' in root or root == '.':
                                print(f"Found keyword in content of: {full_path}")
                except Exception as e:
                    pass

find_files()
