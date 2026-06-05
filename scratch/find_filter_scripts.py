with open("sapo_BWT_using_no_change_it/layout/theme.bwt", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split('\n')
for i, line in enumerate(lines):
    if 'filter' in line.lower() or 'search' in line.lower():
        print(f"Line {i+1}: {line}")
