import re

with open('assets/main.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Add filtering logic inside renderShopeeReviews
old_code = """        function renderShopeeReviews(items) {
            shopeeList.innerHTML = '';
            
            items.forEach(item => {"""

new_code = """        function renderShopeeReviews(items) {
            shopeeList.innerHTML = '';
            
            // Only show 4-star and 5-star reviews
            const goodItems = items.filter(item => (item.rating_star || 5) >= 4);
            
            goodItems.forEach(item => {"""

js_content = js_content.replace(old_code, new_code)

with open('assets/main.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Filtering added.")
