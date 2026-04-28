import re

with open('assets/main.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Replace allorigins with codetabs
old_api_pattern = r"const shopeeApiUrl = 'https://api\.allorigins\.win/raw\?url=' \+ encodeURIComponent\('https://shopee\.vn/api/v4/seller_operation/get_shop_ratings_new\?userid=65858058&shopid=65856601&limit=10&offset=0&replied=undefined'\);"
new_api = "const shopeeApiUrl = 'https://api.codetabs.com/v1/proxy?quest=https://shopee.vn/api/v4/seller_operation/get_shop_ratings_new?userid=65858058&shopid=65856601&limit=10&offset=0&replied=undefined';"

old_summary_pattern = r"const shopeeSummaryUrl = 'https://api\.allorigins\.win/raw\?url=' \+ encodeURIComponent\('https://shopee\.vn/api/v4/seller_operation/get_rating_summary_new\?shop_id=65856601&userid=65858058'\);"
new_summary = "const shopeeSummaryUrl = 'https://api.codetabs.com/v1/proxy?quest=https://shopee.vn/api/v4/seller_operation/get_rating_summary_new?shop_id=65856601&userid=65858058';"

js_content = re.sub(old_api_pattern, new_api, js_content)
js_content = re.sub(old_summary_pattern, new_summary, js_content)

with open('assets/main.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Updated proxy to codetabs.")
