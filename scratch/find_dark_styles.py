with open(r'f:\BAO_SAPO\sapo_new\assets\style.css', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if '[data-theme="dark"]' in line and ('footer' in line.lower() or 'company' in line.lower() or 'brand' in line.lower()):
            print(f'{idx+1}: {line.strip()}')
