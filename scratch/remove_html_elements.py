import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the hero badge
pattern1 = r'[ \t]*<div class="hero-badge"><i class="ph-fill ph-rocket-launch"></i> Tương lai của máy tính cá nhân\r?\n[ \t]*</div>\r?\n?'
content = re.sub(pattern1, '', content, count=1)

# Remove the scroll indicator
pattern2 = r'[ \t]*<!-- Scroll Indicator -->\r?\n[ \t]*<div class="hero-scroll-indicator">\r?\n[ \t]*<span>Khám phá</span>\r?\n[ \t]*<div class="mouse-icon">\r?\n[ \t]*<div class="wheel"></div>\r?\n[ \t]*</div>\r?\n[ \t]*</div>\r?\n?'
content = re.sub(pattern2, '', content, count=1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("HTML elements removed successfully.")
