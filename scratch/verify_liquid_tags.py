import os
import re

# Block tags mapping: open_tag -> close_tag
BLOCK_MAP = {
    'if': 'endif',
    'unless': 'endunless',
    'for': 'endfor',
    'form': 'endform',
    'paginate': 'endpaginate',
    'capture': 'endcapture',
    'comment': 'endcomment',
    'schema': 'endschema',
    'style': 'endstyle',
    'javascript': 'endjavascript'
}

CLOSE_TO_OPEN = {v: k for k, v in BLOCK_MAP.items()}

def verify_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    errors = []
    
    # 1. Check basic delimiter balancing
    open_delims = re.findall(r'\{[%{]', content)
    close_delims = re.findall(r'[%}]\}', content)
    if len(open_delims) != len(close_delims):
        errors.append(f"Delimiter count mismatch: found {len(open_delims)} open delimiters and {len(close_delims)} close delimiters.")
    
    # 2. Match tag blocks
    # Liquid tag pattern: {% tagname args %}
    # We ignore raw text and variables {{ ... }} and look specifically at {% ... %}
    liquid_tags = re.findall(r'\{%\s*(-?)\s*(\w+)(.*?)\s*-?%\}', content, re.DOTALL)
    
    stack = []
    for match in liquid_tags:
        dash, tag_name, args = match
        
        # If it's a block opener
        if tag_name in BLOCK_MAP:
            stack.append((tag_name, filepath))
        # If it's a block closer
        elif tag_name in CLOSE_TO_OPEN:
            expected_open = CLOSE_TO_OPEN[tag_name]
            if not stack:
                errors.append(f"Unmatched closer tag '{tag_name}' found.")
            else:
                top_open, _ = stack.pop()
                if top_open != expected_open:
                    errors.append(f"Mismatched tags: expected close for '{top_open}', but found '{tag_name}' instead.")
    
    while stack:
        unclosed, _ = stack.pop()
        errors.append(f"Unclosed tag '{unclosed}' remains at end of file.")
        
    return errors

def main():
    target_dir = r"f:\BAO_SAPO\sapo_new\sapo_BWT_new"
    print(f"Scanning Liquid templates in {target_dir}...")
    total_files = 0
    total_errors = 0
    
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.endswith('.bwt'):
                total_files += 1
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, target_dir)
                errors = verify_file(filepath)
                if errors:
                    print(f"\n[ERROR] {rel_path}:")
                    for err in errors:
                        print(f"  - {err}")
                    total_errors += len(errors)
                else:
                    # Print success per file
                    print(f"[OK] {rel_path}")
                    
    print(f"\nScan completed. Total files checked: {total_files}. Total issues found: {total_errors}.")
    return total_errors

if __name__ == '__main__':
    exit(main())
