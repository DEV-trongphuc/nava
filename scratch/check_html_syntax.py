import os
import re
import subprocess
import tempfile
import sys

def check_html_file(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    script_blocks = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
    print(f"Checking {html_path}: Found {len(script_blocks)} script blocks.")
    
    for i, block in enumerate(script_blocks):
        if not block.strip():
            continue
            
        with tempfile.NamedTemporaryFile(suffix='.js', delete=False, mode='w', encoding='utf-8') as temp_f:
            temp_f.write(block)
            temp_name = temp_f.name
            
        res = subprocess.run(['node', '-c', temp_name], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"--- {html_path} Script block {i+1} has syntax error ---")
            print(res.stderr)
            lines = block.splitlines()
            match = re.search(r':(\d+)\r?\n', res.stderr)
            if match:
                err_line = int(match.group(1))
                print(f"Error line {err_line}:")
                start = max(0, err_line - 5)
                end = min(len(lines), err_line + 5)
                for l_idx in range(start, end):
                    print(f"{l_idx+1}: {lines[l_idx]}")
            return False
    return True

def main():
    root_dir = r"f:\BAO_SAPO\sapo_new"
    all_ok = True
    for f in os.listdir(root_dir):
        if f.endswith('.html') and f.startswith('demo_') or f in ['index.html', 'account.html', 'addresses.html', 'change_pass.html']:
            path = os.path.join(root_dir, f)
            if not check_html_file(path):
                all_ok = False
                
    if all_ok:
        print("All HTML files are syntax valid.")
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
