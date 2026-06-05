import urllib.request
import ssl
import re
import tempfile
import subprocess

def main():
    url = "https://navastore.vn/mini-pc-ho-tro-ai-asus-nuc-14-pro-rnuc14rvhu700001i-ultra-7-155h-2xnvme-sata-2x-hdmi-2-1-2x-dp-1-4a-vesa-mount"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx) as response:
            html = response.read().decode('utf-8')
    except Exception as e:
        print("Error fetching URL:", e)
        return

    lines = html.splitlines()
    in_script = False
    script_lines = []
    script_start = 0
    
    for idx, line in enumerate(lines):
        if '<script>' in line or '<script ' in line:
            if '</script>' in line:
                content = re.search(r'<script.*?>(.*?)</script>', line)
                if content:
                    check_block(content.group(1), idx + 1, idx + 1, lines)
            else:
                in_script = True
                script_start = idx + 1
                script_lines = []
        elif '</script>' in line:
            in_script = False
            block = '\n'.join(script_lines)
            check_block(block, script_start, idx + 1, lines)
        elif in_script:
            script_lines.append(line)

def check_block(block, start_line, end_line, all_lines):
    if not block.strip():
        return
    with tempfile.NamedTemporaryFile(suffix='.js', delete=False, mode='w', encoding='utf-8') as temp_f:
        temp_f.write(block)
        temp_name = temp_f.name
        
    res = subprocess.run(['node', '-c', temp_name], capture_output=True, text=True)
    if res.returncode != 0:
        # Check if this is the large script block containing our error (around line 4117)
        match = re.search(r':(\d+)\r?\n', res.stderr)
        if match:
            err_offset = int(match.group(1))
            html_err_line = start_line + err_offset
            
            # Save debug information to file
            with open('scratch/error_script_lines.txt', 'w', encoding='utf-8') as f:
                f.write(f"Syntax error found in script block starting at HTML line {start_line} and ending at HTML line {end_line}\n")
                f.write(f"Node Error: {res.stderr}\n")
                f.write(f"Calculated Error Line in HTML: {html_err_line}\n")
                f.write(f"Calculated Error Line in Script block: {err_offset}\n\n")
                
                block_lines = block.splitlines()
                start_idx = max(0, err_offset - 20)
                end_idx = min(len(block_lines), err_offset + 20)
                for idx_line in range(start_idx, end_idx):
                    f.write(f"Script Line {idx_line+1} (HTML Line {start_line + idx_line + 1}): {block_lines[idx_line]}\n")
            print(f"Error details written to scratch/error_script_lines.txt for HTML block {start_line}-{end_line}")

if __name__ == '__main__':
    main()
