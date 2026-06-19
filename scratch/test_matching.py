import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/ssd24_live.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Mimic the selectEl options retrieval
options = []
select_pattern = re.compile(r'<select[^>]*id=["\']product-selectors["\'][^>]*>([\s\S]*?)</select>', re.IGNORECASE)
m = select_pattern.search(html)
if m:
    option_pattern = re.compile(r'<option([^>]*)>([\s\S]*?)</option>', re.IGNORECASE)
    for opt_m in option_pattern.finditer(m.group(1)):
        attrs_str = opt_m.group(1)
        text = opt_m.group(2).strip()
        # Parse attributes
        price = re.search(r'data-price=["\']([^"\']*)["\']', attrs_str)
        price_val = price.group(1) if price else "0"
        options.append({'text': text, 'price': price_val})

# Let's test selectedValues = ["256GB"]
selectedValues = ["256GB"]
print(f"Selected Values from Swatch: {selectedValues}")
print("Testing matching:")

matchedOption = None
for opt in options:
    text = opt['text']
    textParts = text.split('-')
    titlePart = '-'.join(textParts[:-1]).strip()
    # Strip ID prefix
    titlePart_stripped = re.sub(r'^\d+\s+', '', titlePart).strip()
    optValues = [v.strip() for v in titlePart_stripped.split('/')]
    
    isMatch = True
    for i in range(len(selectedValues)):
        if i >= len(optValues):
            isMatch = False
            break
        if optValues[i] != selectedValues[i]:
            isMatch = False
            break
            
    print(f"Option: '{text}' -> titlePart: '{titlePart}' -> stripped: '{titlePart_stripped}' -> optValues: {optValues} | Match: {isMatch}")
    if isMatch:
        matchedOption = opt

if matchedOption:
    print(f"\nSUCCESS: Matched Option: {matchedOption}")
else:
    print("\nFAILED: No option matched!")
