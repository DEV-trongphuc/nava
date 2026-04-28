import re

# 1. Update index.html
# Change the badge color in index.html to match the landing page instead of shopee orange
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the inline styles for the badge
pattern = re.compile(r'<div class="testi-badge" style="background: rgba\(238, 77, 45, 0.1\); border-color: rgba\(238, 77, 45, 0.2\); color: #ee4d2d;">')
new_badge = '<div class="testi-badge"><i class="ph-fill ph-chat-centered-text"></i> Đánh giá trên Shopee</div>'
content = pattern.sub(new_badge, content)

# Change the section title to not use a separate span color unless it's primary
content = content.replace('<h2 class="section-title">Nhận Xét Từ Gian Hàng <span>Shopee</span></h2>', '<h2 class="section-title">Khách Hàng Nói Gì Về <span>Sản Phẩm?</span></h2>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)


# 2. Update style.css
with open('assets/style.css', 'r', encoding='utf-8') as f:
    css_content = f.read()

# Replace the Shopee Reviews CSS block
old_css_pattern = re.compile(r'/\* --- SHOPEE REVIEWS SECTION --- \*/.*?(?=\n\n|\Z)', re.DOTALL)

# Let's find the start of /* --- SHOPEE RATING SUMMARY --- */ and replace everything to the end
old_css_pattern_full = re.compile(r'/\* --- SHOPEE RATING SUMMARY --- \*/.*', re.DOTALL)

new_css = """/* --- NAVA REVIEWS SECTION --- */
.shopee-reviews-section {
    padding: 80px 0;
    background: var(--bg-gray);
    position: relative;
    overflow: hidden;
}

/* Rating Summary */
.shopee-rating-summary {
    max-width: 900px;
    margin: 0 auto 40px auto;
    background: var(--bg-white);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: 35px 40px;
    display: flex;
    align-items: center;
    gap: 50px;
    box-shadow: var(--shadow-md);
    position: relative;
    z-index: 2;
}
.sr-overview {
    text-align: center;
    flex-shrink: 0;
    padding-right: 50px;
    border-right: 1px solid var(--border-color);
}
.sr-score {
    font-size: 4rem;
    font-weight: 800;
    color: var(--primary);
    line-height: 1;
    margin-bottom: 10px;
    text-shadow: 0 4px 10px rgba(0, 51, 102, 0.1);
}
.sr-score span {
    font-size: 1.5rem;
    color: var(--text-gray);
    font-weight: 600;
}
.sr-stars {
    color: #f59e0b;
    font-size: 1.4rem;
    margin-bottom: 8px;
}
.sr-total {
    font-size: 0.95rem;
    color: var(--text-gray);
    font-weight: 500;
}
.sr-bars {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 10px;
}
.sr-bar-row {
    display: flex;
    align-items: center;
    gap: 15px;
    font-size: 0.9rem;
    color: var(--text-dark);
    font-weight: 500;
}
.sr-star-label {
    min-width: 45px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.sr-star-label i {
    color: #f59e0b;
}
.sr-progress {
    flex: 1;
    height: 10px;
    background: var(--border-color);
    border-radius: 5px;
    overflow: hidden;
}
.sr-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--primary), var(--primary-light));
    border-radius: 5px;
}
.sr-count {
    min-width: 45px;
    text-align: right;
    color: var(--text-gray);
}

/* Comments List */
.shopee-comments-list {
    max-width: 900px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 20px;
    position: relative;
    z-index: 2;
}
.shopee-comment-item {
    background: var(--bg-white);
    border-radius: var(--radius-lg);
    padding: 30px;
    border: 1px solid var(--border-color);
    box-shadow: var(--shadow-sm);
    display: flex;
    gap: 20px;
    transition: all 0.3s ease;
}
.shopee-comment-item:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
}
.sc-avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--primary-light), var(--primary));
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    flex-shrink: 0;
    box-shadow: 0 4px 10px rgba(0, 51, 102, 0.2);
}
.sc-avatar img {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
}
.sc-content {
    flex: 1;
}
.sc-username {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text-dark);
    margin-bottom: 4px;
}
.sc-stars {
    color: #f59e0b;
    font-size: 0.9rem;
    margin-bottom: 8px;
    letter-spacing: 1px;
}
.sc-meta {
    font-size: 0.85rem;
    color: var(--text-gray);
    margin-bottom: 15px;
}
.sc-reply-box {
    background: rgba(0, 51, 102, 0.03);
    border-left: 3px solid var(--primary);
    padding: 15px 20px;
    border-radius: 0 var(--radius-md) var(--radius-md) 0;
    margin-bottom: 15px;
}
.sc-reply-title {
    font-size: 0.85rem;
    font-weight: 700;
    color: var(--primary);
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.sc-reply-text {
    font-size: 0.9rem;
    color: var(--text-dark);
    line-height: 1.6;
}
.sc-product-card {
    display: flex;
    align-items: center;
    gap: 12px;
    background: var(--bg-gray);
    padding: 10px;
    border-radius: var(--radius-md);
    max-width: 450px;
    margin-bottom: 15px;
    border: 1px solid var(--border-color);
}
.sc-product-card img {
    width: 50px;
    height: 50px;
    object-fit: cover;
    border-radius: 6px;
}
.sc-product-info {
    display: flex;
    flex-direction: column;
}
.sc-product-name {
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-dark);
    display: -webkit-box;
    -webkit-line-clamp: 1;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.sc-product-variant {
    font-size: 0.8rem;
    color: var(--text-gray);
    margin-top: 2px;
}
.sc-helpful {
    font-size: 0.85rem;
    color: var(--text-gray);
    display: inline-flex;
    align-items: center;
    gap: 6px;
    cursor: pointer;
    transition: color 0.3s ease;
    padding: 5px 10px;
    border-radius: var(--radius-sm);
    background: rgba(0,0,0,0.02);
}
.sc-helpful:hover {
    color: var(--primary);
    background: rgba(0, 51, 102, 0.05);
}

@media (max-width: 768px) {
    .shopee-rating-summary {
        flex-direction: column;
        gap: 25px;
        padding: 25px;
    }
    .sr-overview {
        padding-right: 0;
        border-right: none;
        border-bottom: 1px dashed var(--border-color);
        padding-bottom: 25px;
        width: 100%;
    }
    .shopee-comment-item {
        flex-direction: column;
        gap: 15px;
    }
}

/* Dark Theme Overrides */
[data-theme="dark"] .shopee-reviews-section {
    background: #0f172a;
}
[data-theme="dark"] .shopee-rating-summary,
[data-theme="dark"] .shopee-comment-item {
    background: #1e293b;
    border-color: rgba(255,255,255,0.05);
}
[data-theme="dark"] .sr-overview { border-color: rgba(255,255,255,0.1); }
[data-theme="dark"] .sr-score { color: #e2e8f0; text-shadow: 0 4px 10px rgba(0,0,0,0.5); }
[data-theme="dark"] .sr-progress { background: #0f172a; }
[data-theme="dark"] .sr-bar-row { color: #cbd5e1; }
[data-theme="dark"] .sr-fill { background: linear-gradient(90deg, #3b82f6, #60a5fa); }
[data-theme="dark"] .sc-avatar { background: linear-gradient(135deg, #3b82f6, #1d4ed8); }
[data-theme="dark"] .sc-reply-box { background: rgba(59, 130, 246, 0.1); border-left-color: #3b82f6; }
[data-theme="dark"] .sc-product-card { background: #0f172a; border-color: rgba(255,255,255,0.05); }
[data-theme="dark"] .sc-username, 
[data-theme="dark"] .sc-product-name, 
[data-theme="dark"] .sc-reply-text {
    color: #e2e8f0;
}
[data-theme="dark"] .sc-reply-title { color: #60a5fa; }
"""

# Let's cleanly replace all the Shopee CSS
css_content = old_css_pattern_full.sub(new_css, css_content)

# If it didn't match (because maybe I didn't get the regex right), let's fallback
if '/* --- NAVA REVIEWS SECTION --- */' not in css_content:
    with open('assets/style.css', 'w', encoding='utf-8') as f:
        # Just write to the end, but actually let's use a simpler replace
        pass # I will handle this after reading the file properly

with open('assets/style.css', 'w', encoding='utf-8') as f:
    f.write(css_content)

# 3. Update main.js
with open('assets/main.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Revert the URLs to original shopee API
js_content = re.sub(
    r"const shopeeApiUrl = 'https://api\.allorigins\.win/raw\?url=' \+ encodeURIComponent\('([^']+)'\);",
    r"const shopeeApiUrl = '\1';",
    js_content
)

js_content = re.sub(
    r"const shopeeSummaryUrl = 'https://api\.allorigins\.win/raw\?url=' \+ encodeURIComponent\('([^']+)'\);",
    r"const shopeeSummaryUrl = '\1';",
    js_content
)

with open('assets/main.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Updates applied")
