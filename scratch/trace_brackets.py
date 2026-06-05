def main():
    bwt_path = r"sapo_BWT_new/Templates/product.bwt"
    with open(bwt_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    
    start_line = 2538
    end_line = 2801
    
    stack = []
    in_string = False
    str_char = ''
    in_multiline_comment = False
    
    out_lines = []
    
    for idx in range(start_line - 1, end_line):
        line = lines[idx]
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
                out_lines.append(f"Push {c} at {idx+1}:{i+1} - Stack size: {len(stack)}\n")
            elif c in ['}', ')', ']']:
                if stack:
                    top_c, top_l, top_col = stack.pop()
                    out_lines.append(f"Pop {c} at {idx+1}:{i+1} matching {top_c} from {top_l}:{top_col} - Stack size: {len(stack)}\n")
                else:
                    out_lines.append(f"Extra closing {c} at {idx+1}:{i+1}\n")
            i += 1

    with open('scratch/bracket_trace_utf8.txt', 'w', encoding='utf-8') as f:
        f.writelines(out_lines)
    print("Done")

if __name__ == '__main__':
    main()
