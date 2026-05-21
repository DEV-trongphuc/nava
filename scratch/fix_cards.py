import re

with open("build_demos.py", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Remove MARK badges
text = re.sub(r'\s*<span class="spec-pill secondary">MARK</span>\n?', '', text)

# 2. Remove "Xem ngay" button
btn_html = '<a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity=\'0.85\'" onmouseout="this.style.opacity=\'1\'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>'
text = text.replace(btn_html, '')

# 3. Clean up card-title styles (remove inline height/display styles)
text = re.sub(
    r'<h2 class="card-title" style="font-size: 1rem; line-height: 1.4; margin-bottom: 10px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; height: 40px; font-weight: 700;">(.*?)</h2>',
    r'<h2 class="card-title">\1</h2>',
    text
)

# 4. Replace truncated title text with full names
text = text.replace("ASUS NUC 14 Essential Int...", "ASUS NUC 14 Essential Intel")
text = text.replace("AtomMan G7 PT Mini PC...", "AtomMan G7 PT Mini PC")
text = text.replace("Mini PC GMK EVO X1 32G...", "Mini PC GMK EVO X1 32G")
text = text.replace("Tablet Minisforum V3 SE...", "Tablet Minisforum V3 SE")
text = text.replace("Beelink SER8 AMD 884...", "Beelink SER8 AMD 884")

with open("build_demos.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Programmatic replacements in build_demos.py done!")
