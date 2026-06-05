with open(r'f:\BAO_SAPO\sapo_new\build_demos.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open(r'f:\BAO_SAPO\sapo_new\scratch\find_includes_out.txt', 'w', encoding='utf-8') as out:
    for idx, line in enumerate(lines):
        if 'include' in line.lower() or 'snippet' in line.lower():
            out.write(f'{idx+1}: {line.strip()[:120]}\n')
