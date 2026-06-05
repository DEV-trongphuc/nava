import re
import tempfile
import subprocess
import os

def main():
    filepath = "demo_product.html"
    if not os.path.exists(filepath):
        print(f"File {filepath} does not exist.")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    lines = html.splitlines()
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
    with tempfile.NamedTemporaryFile(suffix='.js', delete=False, mode='w', encoding='utf-8') as temp_f:
        temp_f.write(block)
        temp_name = temp_f.name
        
    try:
        res = subprocess.run(['node', '-c', temp_name], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"\n--- Syntax Error in Script block {start_line}-{end_line} ---")
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
