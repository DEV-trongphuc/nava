import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

path = "scratch/product.json"

try:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    print(f"Product ID: {data.get('id')}")
    print(f"Product Name: {data.get('name')}")
    print(f"Price range: {data.get('price_min')} - {data.get('price_max')}")
    print(f"Price: {data.get('price')}")
    print(f"Price Varies: {data.get('price_varies')}")
    
    print("\nVariants:")
    variants = data.get('variants', [])
    print(f"Number of variants: {len(variants)}")
    for v in variants:
        print(f"- ID: {v['id']}")
        print(f"  Title: {v['title']}")
        print(f"  Price: {v['price']}")
        print(f"  Compare At Price: {v.get('compare_at_price')}")
        print(f"  Available: {v['available']}")
        print(f"  Options: {[v.get('option1'), v.get('option2'), v.get('option3')]}")
        
    print("\nOptions:")
    for opt in data.get('options', []):
        print(f"- Option {opt.get('position')}: {opt.get('name')}")
        print(f"  Values: {opt.get('values')}")
except Exception as e:
    print("Error parsing product.json:", e)
