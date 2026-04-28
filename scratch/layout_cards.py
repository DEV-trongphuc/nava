import re

# 1. Update main.js
with open('assets/main.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Remove 'Hữu ích?'
js_content = js_content.replace('<div class="sc-helpful"><i class="ph-fill ph-thumbs-up"></i> Hữu ích?</div>', '')

# Update the rating summary inner HTML
old_summary_html = """            summaryEl.innerHTML = `
                <div class="sr-overview">
                    <div class="sr-score">${starStr} <span>/ 5</span></div>
                    <div class="sr-stars">${starsHtml}</div>
                    <div class="sr-total">${total.toLocaleString()} đánh giá</div>
                </div>
                <div class="sr-bars">
                    ${barsHtml}
                </div>
            `;"""

new_summary_html = """            summaryEl.innerHTML = `
                <div class="sr-overview-card">
                    <div class="sr-card-title">ĐIỂM TRUNG BÌNH</div>
                    <div class="sr-score">${starStr}</div>
                    <div class="sr-stars">${starsHtml}</div>
                    <div class="sr-total">${total.toLocaleString()} đánh giá</div>
                </div>
                <div class="sr-bars-card">
                    <div class="sr-card-title">PHÂN BỐ ĐÁNH GIÁ</div>
                    <div class="sr-bars">
                        ${barsHtml}
                    </div>
                </div>
            `;"""

js_content = js_content.replace(old_summary_html, new_summary_html)

with open('assets/main.js', 'w', encoding='utf-8') as f:
    f.write(js_content)


# 2. Update style.css
with open('assets/style.css', 'r', encoding='utf-8') as f:
    css_content = f.read()

# Replace the NAVA REVIEWS SECTION
old_css_pattern = re.compile(r'/\* --- NAVA REVIEWS SECTION --- \*/.*', re.DOTALL)

new_css = """/* --- NAVA REVIEWS SECTION --- */
.shopee-reviews-section {
    padding: 100px 0;
    background: var(--bg-gray);
    position: relative;
    overflow: hidden;
}

/* Add a subtle glow behind the reviews section */
.shopee-reviews-section::before {
    content: '';
    position: absolute;
    top: -10%;
    left: 50%;
    transform: translateX(-50%);
    width: 800px;
    height: 400px;
    background: radial-gradient(ellipse at center, rgba(0, 51, 102, 0.05) 0%, transparent 70%);
    z-index: 1;
    pointer-events: none;
}

/* Rating Summary: 2 Cards Layout */
.shopee-rating-summary {
    width: 100%;
    margin: 0 auto 50px auto;
    display: flex;
    gap: 30px;
    position: relative;
    z-index: 2;
    background: transparent;
    border: none;
    padding: 0;
    box-shadow: none;
}

.sr-overview-card, .sr-bars-card {
    background: var(--bg-white);
    border: 1px solid rgba(0, 51, 102, 0.1);
    border-radius: var(--radius-lg);
    padding: 40px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03);
    transition: transform 0.3s ease;
}

.sr-overview-card {
    flex: 0 0 35%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.sr-bars-card {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.sr-card-title {
    font-size: 0.9rem;
    font-weight: 700;
    color: var(--text-gray);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 20px;
    text-align: center;
}
.sr-bars-card .sr-card-title {
    text-align: left;
    margin-bottom: 25px;
}

.sr-score {
    font-size: 5rem;
    font-weight: 800;
    color: var(--primary);
    line-height: 1;
    margin-bottom: 10px;
    letter-spacing: -2px;
}

.sr-stars {
    color: #f59e0b;
    font-size: 1.5rem;
    margin-bottom: 10px;
    filter: drop-shadow(0 2px 4px rgba(245, 158, 11, 0.3));
}

.sr-total {
    font-size: 0.95rem;
    color: var(--text-gray);
    font-weight: 500;
    font-style: italic;
}

.sr-bars {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.sr-bar-row {
    display: flex;
    align-items: center;
    gap: 20px;
    font-size: 1rem;
    color: var(--text-dark);
    font-weight: 600;
}

.sr-star-label {
    min-width: 50px;
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
    background: rgba(0, 51, 102, 0.05);
    border-radius: 5px;
    overflow: hidden;
    position: relative;
}

.sr-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--primary-light), var(--primary));
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 76, 153, 0.4);
}

.sr-count {
    min-width: 50px;
    text-align: right;
    color: var(--text-gray);
    font-variant-numeric: tabular-nums;
}

/* Comments List: Fullwidth */
.shopee-comments-list {
    width: 100%;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 25px;
    position: relative;
    z-index: 2;
}

.shopee-comment-item {
    background: var(--bg-white);
    border-radius: var(--radius-lg);
    padding: 35px 40px;
    border: 1px solid rgba(0, 51, 102, 0.05);
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.02);
    display: flex;
    gap: 25px;
    transition: all 0.3s ease;
    width: 100%;
}

.shopee-comment-item:hover {
    box-shadow: 0 15px 30px rgba(0, 51, 102, 0.06);
    transform: translateY(-2px);
    border-color: rgba(0, 51, 102, 0.1);
}

.sc-avatar {
    width: 55px;
    height: 55px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--primary-light), var(--primary));
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.8rem;
    flex-shrink: 0;
    box-shadow: 0 8px 15px rgba(0, 51, 102, 0.2);
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
    font-size: 1.15rem;
    font-weight: 800;
    color: var(--text-dark);
    margin-bottom: 4px;
    letter-spacing: -0.3px;
}

.sc-stars {
    color: #f59e0b;
    font-size: 0.95rem;
    margin-bottom: 10px;
    letter-spacing: 2px;
}

.sc-meta {
    font-size: 0.85rem;
    color: var(--text-gray);
    margin-bottom: 18px;
    font-weight: 500;
}

.sc-reply-box {
    background: rgba(0, 51, 102, 0.02);
    border-left: 3px solid var(--primary);
    padding: 18px 24px;
    border-radius: 0 var(--radius-md) var(--radius-md) 0;
    margin-bottom: 18px;
    max-width: 90%;
}

.sc-reply-title {
    font-size: 0.85rem;
    font-weight: 800;
    color: var(--primary);
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.sc-reply-text {
    font-size: 0.95rem;
    color: var(--text-dark);
    line-height: 1.7;
}

.sc-product-card {
    display: flex;
    align-items: center;
    gap: 15px;
    background: var(--bg-white);
    padding: 12px;
    border-radius: var(--radius-md);
    max-width: 500px;
    border: 1px solid rgba(0, 51, 102, 0.08);
}
.sc-product-card img {
    width: 55px;
    height: 55px;
    object-fit: cover;
    border-radius: 8px;
}
.sc-product-info {
    display: flex;
    flex-direction: column;
}
.sc-product-name {
    font-size: 0.9rem;
    font-weight: 700;
    color: var(--text-dark);
    display: -webkit-box;
    -webkit-line-clamp: 1;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.sc-product-variant {
    font-size: 0.85rem;
    color: var(--text-gray);
    margin-top: 4px;
}

@media (max-width: 768px) {
    .shopee-rating-summary {
        flex-direction: column;
        gap: 20px;
    }
    .sr-overview-card {
        flex: auto;
    }
    .shopee-comment-item {
        flex-direction: column;
        gap: 20px;
        padding: 25px;
    }
    .sc-reply-box {
        max-width: 100%;
    }
}

/* Dark Theme Overrides */
[data-theme="dark"] .shopee-reviews-section {
    background: #0b1120;
}
[data-theme="dark"] .shopee-reviews-section::before {
    background: radial-gradient(ellipse at center, rgba(59, 130, 246, 0.1) 0%, transparent 70%);
}
[data-theme="dark"] .sr-overview-card, [data-theme="dark"] .sr-bars-card, [data-theme="dark"] .shopee-comment-item {
    background: #1e293b;
    border-color: rgba(255,255,255,0.05);
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}
[data-theme="dark"] .sr-card-title { color: #94a3b8; }
[data-theme="dark"] .sr-score { 
    background: linear-gradient(135deg, #f59e0b, #fbbf24);
    -webkit-background-clip: text;
}
[data-theme="dark"] .sr-progress { background: rgba(0,0,0,0.3); }
[data-theme="dark"] .sr-bar-row { color: #cbd5e1; }
[data-theme="dark"] .sr-fill { background: linear-gradient(90deg, #f59e0b, #fbbf24); box-shadow: 0 0 10px rgba(245, 158, 11, 0.3); }
[data-theme="dark"] .sc-avatar { border-color: #1e293b; background: linear-gradient(135deg, #3b82f6, #1d4ed8); }
[data-theme="dark"] .sc-reply-box { background: rgba(255, 255, 255, 0.02); border-left-color: #3b82f6; }
[data-theme="dark"] .sc-product-card { background: #0f172a; border-color: rgba(255,255,255,0.05); }
[data-theme="dark"] .sc-username, 
[data-theme="dark"] .sc-product-name, 
[data-theme="dark"] .sc-reply-text {
    color: #f8fafc;
}
[data-theme="dark"] .sc-reply-title { color: #60a5fa; }
"""

css_content = old_css_pattern.sub(new_css, css_content)
with open('assets/style.css', 'w', encoding='utf-8') as f:
    f.write(css_content)

print("Updates applied")
