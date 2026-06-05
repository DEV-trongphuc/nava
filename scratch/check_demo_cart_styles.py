def main():
    filepath = 'demo_cart.html'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    print("demo_cart.html length:", len(content))
    
    # check for key style properties
    properties = [
        'background: transparent !important;',
        'max-width: 100px !important;',
        'flex: 1 !important;',
        'display: inline-flex !important; align-items: center; justify-content: center; transition: 0.2s;'
    ]
    
    for prop in properties:
        print(f"Property '{prop}': {content.count(prop)} occurrences")

if __name__ == '__main__':
    main()
