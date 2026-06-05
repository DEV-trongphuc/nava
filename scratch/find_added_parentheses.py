import subprocess

def check_parentheses(line):
    open_count = 0
    close_count = 0
    in_string = False
    str_char = ''
    i = 0
    while i < len(line):
        c = line[i]
        if in_string:
            if c == str_char and line[i-1] != '\\':
                in_string = False
        else:
            if c in ['"', "'", '`']:
                in_string = True
                str_char = c
            elif c == '(':
                open_count += 1
            elif c == ')':
                close_count += 1
        i += 1
    return open_count, close_count

def main():
    res = subprocess.run(['git', 'diff', 'sapo_BWT_new/Templates/product.bwt'], capture_output=True, text=True, encoding='utf-8')
    diff_lines = res.stdout.splitlines()
    for l_num, line in enumerate(diff_lines):
        if line.startswith('+') and not line.startswith('+++'):
            clean_line = line[1:]
            op, cl = check_parentheses(clean_line)
            if cl > op:
                print(f"Potential extra closing paren in diff line {l_num+1}: {line}")
            elif op > cl:
                print(f"Potential extra opening paren in diff line {l_num+1}: {line}")

if __name__ == '__main__':
    main()
