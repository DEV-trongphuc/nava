import re

with open('assets/main.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Replace the API URLs with the new PHP proxy URLs
old_api_pattern = r"const shopeeApiUrl = 'https://api\.codetabs\.com/v1/proxy\?quest=https://shopee\.vn/api/v4/seller_operation/get_shop_ratings_new\?userid=65858058&shopid=65856601&limit=6&offset=0&replied=undefined';"
new_api = "const shopeeApiUrl = 'https://automation.ideas.edu.vn/meta_report/shopee_proxy.php?type=reviews';"

old_summary_pattern = r"const shopeeSummaryUrl = 'https://api\.codetabs\.com/v1/proxy\?quest=https://shopee\.vn/api/v4/seller_operation/get_rating_summary_new\?shop_id=65856601&userid=65858058';"
new_summary = "const shopeeSummaryUrl = 'https://automation.ideas.edu.vn/meta_report/shopee_proxy.php?type=summary';"

js_content = re.sub(old_api_pattern, new_api, js_content)
js_content = re.sub(old_summary_pattern, new_summary, js_content)

with open('assets/main.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Updated URLs to point to automation.ideas.edu.vn proxy.")
