import re

with open('build_demos.py', 'r', encoding='utf-8') as f:
    content = f.read()

# For grid products:
cards = re.split(r'<!-- Product \d+ -->', content)
if len(cards) > 1:
    for i in range(1, len(cards)):
        card = cards[i]
        if "class=\"compare-btn\"" in card:
            continue
            
        img_match = re.search(r'<img src="([^"]+)" alt="([^"]+)"', card)
        price_match = re.search(r'<span style="color: var\(--text-color\); font-weight: 800; font-size: 1.1\d*rem;">([^<]+)</span>', card)
        
        if img_match and price_match:
            img_url = img_match.group(1)
            title_match = re.search(r'<h2 class="card-title"[^>]*>([^<]+)</h2>', card)
            name = title_match.group(1).replace('...', '').strip() if title_match else img_match.group(2)
            price = price_match.group(1)
            
            btn_html = f'<button class="compare-btn" data-name="{name}" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-color); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, \'{name}\', \'{img_url}\', \'{price}\')" onmouseover="if(this.style.background!==\'var(--primary)\'){{this.style.borderColor=\'var(--primary)\'; this.style.color=\'var(--primary)\'}}"><i class="ph ph-arrows-left-right"></i></button>\n                                '
            
            # Inject right after <div class="card-image-wrap"...
            # The structure is: <div class="card-image-wrap" ...>\n  <img ...>
            # Let's find `<img` and insert before it.
            pos = card.find('<img src="')
            if pos != -1:
                cards[i] = card[:pos] + btn_html + card[pos:]

    new_content = cards[0]
    for i in range(1, len(cards)):
        new_content += f'<!-- Product {i} -->' + cards[i]

    with open('build_demos.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Injected compare buttons for grid products!")
else:
    print("No grid products found!")
