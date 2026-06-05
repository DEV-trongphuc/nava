def main():
    bwt_path = r"sapo_BWT_new/Templates/product.bwt"
    with open(bwt_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    
    stack = []
    in_string = False
    str_char = ''
    in_multiline_comment = False
    in_script = False
    
    for idx, line in enumerate(lines):
        # We only want to check code inside <script> blocks
        if '<script>' in line or '<script ' in line:
            in_script = True
            continue
        elif '</script>' in line:
            in_script = False
            if stack:
                print(f"Unclosed brackets at script end (HTML Line {idx+1}):")
                for item in stack:
                    print(f"  {item[0]} at Line {item[1]}:{item[2]}")
                stack = []
            continue
            
        if not in_script:
            continue
            
        i = 0
        while i < len(line):
            c = line[i]
            
            if in_multiline_comment:
                if c == '*' and i + 1 < len(line) and line[i+1] == '/':
                    in_multiline_comment = False
                    i += 2
                    continue
                i += 1
                continue
            
            if not in_string and c == '/' and i + 1 < len(line) and line[i+1] == '/':
                break
            
            if not in_string and c == '/' and i + 1 < len(line) and line[i+1] == '*':
                in_multiline_comment = True
                i += 2
                continue
                
            if in_string:
                if c == str_char and line[i-1] != '\\':
                    in_string = False
                i += 1
                continue
            
            if c in ['"', "'", '`']:
                in_string = True
                str_char = c
                i += 1
                continue
            
            if c in ['{', '(', '[']:
                stack.append((c, idx + 1, i + 1))
            elif c in ['}', ')', ']']:
                if stack:
                    top_c, top_l, top_col = stack.pop()
                    match = False
                    if top_c == '{' and c == '}': match = True
                    if top_c == '(' and c == ')': match = True
                    if top_c == '[' and c == ']': match = True
                    if not match:
                        print(f"Mismatch: opened {top_c} at Line {top_l}:{top_col}, closed with {c} at Line {idx+1}:{i+1}")
                else:
                    print(f"Extra closing {c} at Line {idx+1}:{i+1}")
            i += 1
            
    print("Full check done.")

if __name__ == '__main__':
    main()
