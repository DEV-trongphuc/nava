with open('sapo_BWT_new/Templates/collection.bwt', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f, 1):
        if 'breadcrumb' in line.lower() or 'crumb' in line.lower():
            print(f"Match found at line {idx}: {line.strip()}")
