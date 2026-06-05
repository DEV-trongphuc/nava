import os
import re

html_path = 'demo_product.html'
if not os.path.exists(html_path):
    print("demo_product.html does not exist!")
    exit(1)

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Check for Buy Now button ID
buy_now_match = re.search(r'id=["\']btn-buy-now-main["\']', content)
if buy_now_match:
    print("[SUCCESS] Found 'btn-buy-now-main' ID!")
else:
    print("[FAIL] Could NOT find 'btn-buy-now-main' ID!")

# Check for Add to Cart button ID
add_cart_match = re.search(r'id=["\']btn-add-to-cart-main["\']', content)
if add_cart_match:
    print("[SUCCESS] Found 'btn-add-to-cart-main' ID!")
else:
    print("[FAIL] Could NOT find 'btn-add-to-cart-main' ID!")

# Check for Installment button ID
installment_match = re.search(r'id=["\']btn-installment-main["\']', content)
if installment_match:
    print("[SUCCESS] Found 'btn-installment-main' ID!")
else:
    print("[FAIL] Could NOT find 'btn-installment-main' ID!")

# Check for the JS logic mapping IDs to class queries
js_path = 'assets/main.js'
if os.path.exists(js_path):
    with open(js_path, 'r', encoding='utf-8') as f:
        js_content = f.read()
    
    # Check for the click handlers added to the IDs
    buy_now_js = 'btn-buy-now-main' in js_content
    add_cart_js = 'btn-add-to-cart-main' in js_content
    installment_js = 'btn-installment-main' in js_content

    if buy_now_js:
        print("[SUCCESS] Found JS logic referencing 'btn-buy-now-main'!")
    else:
        print("[FAIL] Could NOT find JS logic referencing 'btn-buy-now-main'!")
        
    if add_cart_js:
        print("[SUCCESS] Found JS logic referencing 'btn-add-to-cart-main'!")
    else:
        print("[FAIL] Could NOT find JS logic referencing 'btn-add-to-cart-main'!")

    if installment_js:
        print("[SUCCESS] Found JS logic referencing 'btn-installment-main'!")
    else:
        print("[FAIL] Could NOT find JS logic referencing 'btn-installment-main'!")
else:
    print("[FAIL] assets/main.js not found!")
