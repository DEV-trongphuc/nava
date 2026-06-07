import re
import json

def test_json():
    with open(r'f:\BAO_SAPO\sapo_new\sapo_BWT_new\snippets\schema_product.bwt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Strip script tags
    content = content.replace('<script type="application/ld+json">', '').replace('</script>', '').strip()
    
    # Mock liquid structures
    # 1. replace {% if ... %}...{% else %}...{% endif %}
    # Let's assume price_max > price_min is false, so it goes to else.
    # Also assume compare_at_price > 0 is true.
    # Let's replace the offers condition
    offers_block = """
    "priceCurrency": "VND",
      "price": "15000",
      "priceValidUntil": "2099-12-31",
      "priceSpecification": {
        "@type": "PriceSpecification",
        "price": "20000",
        "priceCurrency": "VND"
      },
    "availability": "https://schema.org/InStock",
    """
    
    # Let's clean up all liquid syntax by regex
    # Replace the offers block logic
    content = re.sub(r'"offers":\s*\{.*?"availability":', f'"offers": {{\n    "@type": "Offer",\n{offers_block}"availability":', content, flags=re.DOTALL)
    
    # Replace other logic blocks like {% if product.type != null %} ... {% endif %}
    content = re.sub(r'\{%- if product\.type != null -%\}\s*"model":\s*".*?",\s*\{%- endif -%\}', '"model": "TestModel",', content)
    
    # Replace image loop
    content = re.sub(r'"image":\s*\[.*?\],', '"image": ["https://test.img/1.jpg", "https://test.img/2.jpg"],', content, flags=re.DOTALL)
    
    # Replace metafields ratings block
    # Case 1: ratings.value is present
    rating_block = """
    ,"aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "5",
    "reviewCount": "10"
    }
    """
    content_case1 = re.sub(r'\{%- if product\.metafields\.ratings\.value -%\}.*?\{%- endif -%\}', rating_block, content, flags=re.DOTALL)
    
    # Case 2: bpr.votes is present (so ratings.value is absent)
    bpr_block = """
    ,"aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.5",
    "reviewCount": "20"
    }
    """
    content_case2 = re.sub(r'\{%- if product\.metafields\.ratings\.value -%\}.*?\{%- endif -%\}', bpr_block, content, flags=re.DOTALL)

    # Case 3: neither is present
    content_case3 = re.sub(r'\{%- if product\.metafields\.ratings\.value -%\}.*?\{%- endif -%\}', '', content, flags=re.DOTALL)
    
    # Now replace remaining liquid variables: {{ ... }}
    def clean_liquid_vars(text):
        return re.sub(r'\{\{.*?\}\}', 'dummy_value', text)
    
    json1 = clean_liquid_vars(content_case1)
    json2 = clean_liquid_vars(content_case2)
    json3 = clean_liquid_vars(content_case3)
    
    print("Testing Case 1:")
    try:
        json.loads(json1)
        print("Success Case 1")
    except Exception as e:
        print("Failed Case 1:", e)
        print("JSON contents:")
        print(json1)
        
    print("\nTesting Case 2:")
    try:
        json.loads(json2)
        print("Success Case 2")
    except Exception as e:
        print("Failed Case 2:", e)
        print("JSON contents:")
        print(json2)

    print("\nTesting Case 3:")
    try:
        json.loads(json3)
        print("Success Case 3")
    except Exception as e:
        print("Failed Case 3:", e)
        print("JSON contents:")
        print(json3)

if __name__ == '__main__':
    test_json()
