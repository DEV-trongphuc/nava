import re
import os

# 1. Update main.js
with open('assets/main.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Replace Vercel URLs with allorigins CORS proxy
old_api = "const shopeeApiUrl = '/api/shopee-reviews';"
new_api = "const shopeeApiUrl = 'https://api.allorigins.win/raw?url=' + encodeURIComponent('https://shopee.vn/api/v4/seller_operation/get_shop_ratings_new?userid=65858058&shopid=65856601&limit=10&offset=0&replied=undefined');"

old_summary = "const shopeeSummaryUrl = '/api/shopee-summary';"
new_summary = "const shopeeSummaryUrl = 'https://api.allorigins.win/raw?url=' + encodeURIComponent('https://shopee.vn/api/v4/seller_operation/get_rating_summary_new?shop_id=65856601&userid=65858058');"

js_content = js_content.replace(old_api, new_api)
js_content = js_content.replace(old_summary, new_summary)

with open('assets/main.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

# 2. Remove vercel.json
if os.path.exists('vercel.json'):
    os.remove('vercel.json')

print("Reverted to allorigins proxy and removed vercel.json")
