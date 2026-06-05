def main():
    filepath = 'scratch/live_cart.html'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    classes = ['cart-items-container', 'cart-grid', 'cart-summary', 'cart-layout', 'nava-cart-page']
    for c in classes:
        print(f"Class '{c}': {content.count(c)} occurrences")

if __name__ == '__main__':
    main()
