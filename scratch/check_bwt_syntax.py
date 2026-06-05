import re
import tempfile
import subprocess
import os

def main():
    filepath = "sapo_BWT_new/Templates/product.bwt"
    if not os.path.exists(filepath):
        print(f"File {filepath} does not exist.")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        bwt = f.read()

    # Process Liquid comments out first so we don't extract commented scripts
    # replace {% comment %}...{% endcomment %} with spaces
    bwt = re.sub(r'{%\s*comment\s*%}.*?{%\s*endcomment\s*%}', lambda m: ' ' * len(m.group(0)), bwt, flags=re.DOTALL)

    lines = bwt.splitlines()
    in_script = False
    script_lines = []
    script_start = 0
    
    for idx, line in enumerate(lines):
        if '<script>' in line or '<script ' in line:
            if '</script>' in line:
                content = re.search(r'<script.*?>(.*?)</script>', line)
                if content:
                    check_block(content.group(1), idx + 1, idx + 1)
            else:
                in_script = True
                script_start = idx + 1
                match = re.search(r'<script.*?>', line)
                if match:
                    start_content = line[match.end():]
                    script_lines = [start_content] if start_content.strip() else []
                else:
                    script_lines = []
        elif '</script>' in line:
            in_script = False
            match = re.search(r'</script>', line)
            if match:
                end_content = line[:match.start()]
                if end_content.strip():
                    script_lines.append(end_content)
            block = '\n'.join(script_lines)
            check_block(block, script_start, idx + 1)
        elif in_script:
            script_lines.append(line)

def check_block(block, start_line, end_line):
    if not block.strip():
        return
        
    # Replace Liquid output tags: {{ ... }} with dummy JS strings or numbers
    # For example, {{ product.name | json }} => "dummy"
    # We replace them with an equal length of spaces/valid JS to maintain exact line numbers
    def replace_output(match):
        expr = match.group(1)
        # Check if the output is likely a string or object
        if 'json' in expr or 'src' in expr or 'url' in expr or 'image' in expr:
            return '"' + 'x' * (len(match.group(0)) - 2) + '"'
        else:
            return ' ' * len(match.group(0))
            
    processed = re.sub(r'\{\{(.*?)\}\}', replace_output, block)
    
    # Replace Liquid control tags: {% ... %} with space to keep line structure intact
    processed = re.sub(r'\{%(.*?)%\}', lambda m: ' ' * len(m.group(0)), processed)

    with tempfile.NamedTemporaryFile(suffix='.js', delete=False, mode='w', encoding='utf-8') as temp_f:
        temp_f.write(processed)
        temp_name = temp_f.name
        
    try:
        res = subprocess.run(['node', '-c', temp_name], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"\n--- Syntax Error in product.bwt Script block {start_line}-{end_line} ---")
            print(res.stderr.strip())
            
            # Print surrounding lines
            match = re.search(r':(\d+)\r?\n', res.stderr)
            if match:
                err_offset = int(match.group(1))
                block_lines = block.splitlines()
                start_idx = max(0, err_offset - 10)
                end_idx = min(len(block_lines), err_offset + 10)
                print("\nCode around error:")
                for idx_line in range(start_idx, end_idx):
                    prefix = ">>> " if idx_line + 1 == err_offset else "    "
                    print(f"{prefix}Line {start_line + idx_line}: {block_lines[idx_line]}")
    finally:
        try:
            os.remove(temp_name)
        except:
            pass

if __name__ == '__main__':
    main()
