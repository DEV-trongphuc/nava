import re
import os

files_to_validate = [
    "sapo_BWT_new/Templates/article.bwt",
    "sapo_BWT_new/Templates/blog.bwt",
    "sapo_BWT_new/Templates/page.bwt",
    "sapo_BWT_new/Templates/page.contact.bwt",
    "sapo_BWT_new/layout/theme.bwt"
]

all_errors = 0

for file_path in files_to_validate:
    if not os.path.exists(file_path):
        print(f"Skipping {file_path} - does not exist")
        continue

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

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
        if op in ('if', 'unless', 'for', 'paginate', 'form'):
            stack.append((op, tag))
        elif op in ('endif', 'endunless', 'endfor', 'endpaginate', 'endform'):
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

    print(f"Validation for {file_path}: Found {len(errors)} errors.")
    for err in errors:
        print("  [ERROR]", err)
        all_errors += 1

print(f"\nTotal Liquid validation errors found: {all_errors}")
if all_errors > 0:
    exit(1)
else:
    print("All Liquid files passed structure validation!")
    exit(0)
