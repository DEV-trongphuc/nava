import urllib.parse
with open('assets/main.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Replace the URLs in main.js
old_shopee_api_url = "const shopeeApiUrl = 'https://shopee.vn/api/v4/seller_operation/get_shop_ratings_new?userid=65858058&shopid=65856601&limit=10&offset=0&replied=undefined';"
old_shopee_summary_url = "const shopeeSummaryUrl = 'https://shopee.vn/api/v4/seller_operation/get_rating_summary_new?shop_id=65856601&userid=65858058';"

new_shopee_api_url = "const shopeeApiUrl = 'https://api.allorigins.win/raw?url=' + encodeURIComponent('https://shopee.vn/api/v4/seller_operation/get_shop_ratings_new?userid=65858058&shopid=65856601&limit=10&offset=0&replied=undefined');"
new_shopee_summary_url = "const shopeeSummaryUrl = 'https://api.allorigins.win/raw?url=' + encodeURIComponent('https://shopee.vn/api/v4/seller_operation/get_rating_summary_new?shop_id=65856601&userid=65858058');"

if old_shopee_api_url in js_content:
    js_content = js_content.replace(old_shopee_api_url, new_shopee_api_url)
    js_content = js_content.replace(old_shopee_summary_url, new_shopee_summary_url)
else:
    # Try another matching
    js_content = js_content.replace(
        "const shopeeApiUrl = 'https://shopee.vn/api/v4/seller_operation/get_shop_ratings_new?userid=65858058&shopid=65856601&limit=10&offset=0&replied=undefined';", 
        new_shopee_api_url
    )
    js_content = js_content.replace(
        "const shopeeSummaryUrl = 'https://shopee.vn/api/v4/seller_operation/get_rating_summary_new?shop_id=65856601&userid=65858058';", 
        new_shopee_summary_url
    )

with open('assets/main.js', 'w', encoding='utf-8') as f:
    f.write(js_content)
print("Updated CORS proxy URLs")
