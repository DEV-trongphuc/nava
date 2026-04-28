import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the hero badge
pattern1 = r'([ \t]*)<div class="hero-badge">[\s\S]*?</div>\n?'
content = re.sub(pattern1, '', content, count=1)

# Remove the scroll indicator
pattern2 = r'([ \t]*)<!-- Scroll Indicator -->\s*<div class="hero-scroll-indicator">[\s\S]*?</div>\n?'
content = re.sub(pattern2, '', content, count=1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed successfully!")
