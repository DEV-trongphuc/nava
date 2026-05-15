content = open('build_demos.py', encoding='utf-8').read()

# 1. AI button - use icon, darker blue
content = content.replace(
    '<button class="ai-btn" id="aiSearchBtn">\u2728 T\u00ecm ki\u1ebfm AI</button>',
    '<button class="ai-btn" id="aiSearchBtn"><i class="ph-bold ph-magnifying-glass"></i> T\u00ecm ki\u1ebfm AI</button>'
)

# 2. Compact ai-inner padding
content = content.replace(
    '.ai-inner { background: #fff; border-radius: 48px; display: flex; align-items: center; padding: 7px 8px 7px 20px; gap: 12px; }',
    '.ai-inner { background: #fff; border-radius: 48px; display: flex; align-items: center; padding: 5px 6px 5px 18px; gap: 10px; }'
)

# 3. Darker, more compact ai-btn
content = content.replace(
    '.ai-btn { background: linear-gradient(135deg, #1d4ed8, #3b82f6); border: none; color: white; padding: 10px 24px; border-radius: 40px; font-weight: 700; font-size: 0.95rem; cursor: pointer; transition: all 0.2s; box-shadow: 0 3px 10px rgba(59,130,246,0.35); white-space: nowrap; flex-shrink: 0; }',
    '.ai-btn { background: linear-gradient(135deg, #1e3a8a, #2563eb); border: none; color: white; padding: 8px 18px; border-radius: 40px; font-weight: 700; font-size: 0.85rem; cursor: pointer; transition: all 0.2s; box-shadow: 0 3px 10px rgba(30,58,138,0.35); white-space: nowrap; flex-shrink: 0; display: flex; align-items: center; gap: 6px; }'
)

# 4. Bigger AI result images
content = content.replace(
    '.ai-result-img { width: 48px; height: 48px; object-fit: contain; border-radius: 8px; background: #f8fafc; padding: 4px; flex-shrink: 0; }',
    '.ai-result-img { width: 64px; height: 64px; object-fit: contain; border-radius: 10px; background: #f1f5f9; padding: 6px; flex-shrink: 0; }'
)

# 5. Better ai-result-price badge
content = content.replace(
    '.ai-result-price { color: #2563eb; font-weight: 700; font-size: 0.88rem; }',
    '.ai-result-price { display: inline-block; color: white; background: linear-gradient(135deg,#1e3a8a,#2563eb); font-weight: 700; font-size: 0.82rem; padding: 3px 10px; border-radius: 20px; margin-top: 4px; }'
)

# 6. Remove compare checkbox - replace with cart button (5 cards)
old_compare = '''                                    <label style="display: flex; align-items: center; gap: 5px; color: var(--text-gray); font-size: 0.85rem; cursor: pointer;">
                                        <input type="checkbox" style="accent-color: var(--primary);"> So s\u00e1nh
                                    </label>'''
new_btn = '                                    <a href="#" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity=\'0.85\'" onmouseout="this.style.opacity=\'1\'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>'

content = content.replace(old_compare, new_btn)

open('build_demos.py', 'w', encoding='utf-8').write(content)
count = content.count('Xem ngay')
print(f'Done. Replaced compare buttons: {count} occurrences found.')
