def main():
    import re
    
    # Check cart_style.css
    with open('scratch/cart_style.css', 'r', encoding='utf-8') as f:
        cart_css = f.read()
    print("=== Matches in cart_style.css ===")
    matches = [m.start() for m in re.finditer(r'box-shadow', cart_css)]
    for pos in matches:
        print(repr(cart_css[max(0, pos-50):min(len(cart_css), pos+150)]))
        
    # Check assets/style.css
    with open('assets/style.css', 'r', encoding='utf-8') as f:
        style_css = f.read()
    print("=== Matches in assets/style.css ===")
    matches2 = [m.start() for m in re.finditer(r'ux-card|\.product|cart__basket', style_css)]
    print(f"Total matching selectors in assets/style.css: {len(matches2)}")
    for pos in matches2[:10]:
        print(repr(style_css[max(0, pos-50):min(len(style_css), pos+150)]))

if __name__ == '__main__':
    main()
