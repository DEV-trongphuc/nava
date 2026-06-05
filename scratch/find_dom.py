import re

def main():
    with open('scratch/gmk_product.html', 'r', encoding='utf-8') as f:
        content = f.read()

    selectors = [
        'data-dropdown-type="ram"',
        'ram-selected-text',
        'data-dropdown-type="ssd"',
        'ssd-selected-text',
        'id="availability-status"',
        'class="swatch"',
        'product-selectors',
        'variantId',
        'nava-dropdown-selected',
        'NO SSD',
        'NO RAM',
    ]
    
    for s in selectors:
        count = len(re.findall(re.escape(s), content, re.IGNORECASE))
        print(f"Selector '{s}': {count} occurrences")
        
    # Find all data-dropdown-type elements
    dropdowns = re.findall(r'data-dropdown-type="[^"]+"', content)
    print("\nDropdown types found:", dropdowns)

if __name__ == '__main__':
    main()
