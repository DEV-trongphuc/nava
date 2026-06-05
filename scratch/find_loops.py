with open(r'f:\BAO_SAPO\sapo_new\sapo_BWT_new\Templates\product.bwt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open(r'f:\BAO_SAPO\sapo_new\scratch\find_loops_out.txt', 'w', encoding='utf-8') as out:
    for idx, line in enumerate(lines):
        if 'include' in line.lower() or 'render' in line.lower():
            out.write(f'{idx+1}: {line.strip()}\n')
