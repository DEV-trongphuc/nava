with open("sapo_BWT_new/Templates/product.bwt", "r", encoding="utf-8") as f:
    content = f.read()

import re

# Find all Liquid tags
tags = re.findall(r'{%-?\s*(.*?)\s*-?%}', content)

stack = []
errors = []

for tag in tags:
    parts = tag.strip().split()
    if not parts:
        continue
    op = parts[0]
    
    # Check open/close matching
    if op == 'if' or op == 'unless' or op == 'for' or op == 'paginate':
        stack.append((op, tag))
    elif op == 'endif' or op == 'endunless' or op == 'endfor' or op == 'endpaginate':
        expected = op[3:] # e.g. 'if' for 'endif'
        if not stack:
            errors.append(f"Unexpected closing tag '{op}' ({tag}) when stack is empty")
        else:
            last_op, last_tag = stack.pop()
            if last_op != expected:
                errors.append(f"Mismatched closing tag '{op}' ({tag}) for opening tag '{last_op}' ({last_tag})")

while stack:
    last_op, last_tag = stack.pop()
    errors.append(f"Unclosed tag '{last_op}' ({last_tag})")

print(f"Validation finished. Found {len(errors)} errors.")
for err in errors:
    print(err)
