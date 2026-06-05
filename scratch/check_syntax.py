import re
import subprocess
import tempfile
import sys

def main():
    bwt_path = r"sapo_BWT_new/Templates/product.bwt"
    with open(bwt_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Simple regex to find all <script> blocks
    # Note: this is a simple checker, we will strip liquid tags since they are not valid JS
    script_blocks = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
    
    print(f"Found {len(script_blocks)} script blocks.")
    
    for i, block in enumerate(script_blocks):
        # We need to clean up Liquid tags so they don't trigger syntax errors themselves
        # e.g., {% if ... %} or {{ ... }}
        # Let's replace {% ... %} with space or mock them, and {{ ... }} with dummy values
        cleaned = re.sub(r'{%-?\s*.*?\s*-?%}', ' ', block)
        cleaned = re.sub(r'{{\s*.*?\s*}}', '123', cleaned)
        
        with tempfile.NamedTemporaryFile(suffix='.js', delete=False, mode='w', encoding='utf-8') as temp_f:
            temp_f.write(cleaned)
            temp_name = temp_f.name
            
        # Run node -c on the temporary file
        res = subprocess.run(['node', '-c', temp_name], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"--- Script block {i+1} has syntax error ---")
            # Map lines back to original or show the error
            print(res.stderr)
            # Print lines around the error
            lines = cleaned.splitlines()
            # Try to get line number from stderr
            match = re.search(r':(\d+)\r?\n', res.stderr)
            if match:
                err_line = int(match.group(1))
                print(f"Error line {err_line}:")
                start = max(0, err_line - 5)
                end = min(len(lines), err_line + 5)
                for l_idx in range(start, end):
                    print(f"{l_idx+1}: {lines[l_idx]}")
            else:
                print("Could not parse line number from error:")
                print(res.stderr)
        else:
            print(f"Script block {i+1} is syntax valid.")

if __name__ == '__main__':
    main()
