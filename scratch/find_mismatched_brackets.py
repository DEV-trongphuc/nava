def main():
    bwt_path = r"sapo_BWT_new/Templates/product.bwt"
    with open(bwt_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    
    start_line = 1871
    end_line = 2800
    
    stack = []
    in_string = False
    str_char = ''
    in_comment = False
    in_multiline_comment = False
    
    for idx in range(start_line - 1, end_line):
        line = lines[idx]
        i = 0
        while i < len(line):
            c = line[i]
            
            # Handle comments
            if in_multiline_comment:
                if c == '*' and i + 1 < len(line) and line[i+1] == '/':
                    in_multiline_comment = False
                    i += 2
                    continue
                i += 1
                continue
            
            if not in_string and c == '/' and i + 1 < len(line) and line[i+1] == '/':
                # Single line comment, skip rest of line
                break
            
            if not in_string and c == '/' and i + 1 < len(line) and line[i+1] == '*':
                in_multiline_comment = True
                i += 2
                continue
                
            # Handle strings
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
            
            # Handle brackets
            if c in ['{', '(', '[']:
                stack.append((c, idx + 1, i + 1))
            elif c in ['}', ')', ']']:
                if not stack:
                    print(f"Extra closing {c} at Line {idx+1}, Col {i+1}")
                else:
                    top_c, top_l, top_col = stack.pop()
                    # Check match
                    match = False
                    if top_c == '{' and c == '}': match = True
                    if top_c == '(' and c == ')': match = True
                    if top_c == '[' and c == ']': match = True
                    if not match:
                        print(f"Mismatch: opened {top_c} at Line {top_l}:{top_col}, closed with {c} at Line {idx+1}:{i+1}")
            i += 1
            
    print(f"Finished check. Stack size: {len(stack)}")
    if stack:
        print("Unclosed brackets/parens in stack:")
        for item in stack:
            print(f"  {item[0]} at Line {item[1]}:{item[2]}")

if __name__ == '__main__':
    main()
