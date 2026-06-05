import re

def main():
    filepath = 'build_demos.py'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Length of build_demos.py:", len(content))
    
    # find imports or functions defined
    funcs = re.findall(r'def\s+(\w+)\s*\(', content)
    print("Functions in build_demos.py:", funcs[:20])
    
    # find references to files
    files = re.findall(r'[\w\-_\./]+\.(?:bwt|html|js|css|py)', content)
    print("File references found in build_demos.py:", list(set(files))[:30])

if __name__ == '__main__':
    main()
