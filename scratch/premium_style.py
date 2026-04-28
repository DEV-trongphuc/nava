import re

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

/* Rating Summary */
.shopee-rating-summary {
    max-width: 900px;
    margin: 0 auto 50px auto;
    background: linear-gradient(145deg, #ffffff, #f8fafc);
    border: 1px solid rgba(0, 51, 102, 0.08);
    border-radius: var(--radius-lg);
    padding: 40px 50px;
    display: flex;
    align-items: center;
    gap: 60px;
    box-shadow: 0 20px 40px rgba(0, 51, 102, 0.06), 0 1px 3px rgba(0,0,0,0.05);
    position: relative;
    z-index: 2;
    backdrop-filter: blur(10px);
}
.sr-overview {
    text-align: center;
    flex-shrink: 0;
    padding-right: 60px;
    border-right: 1px solid rgba(0, 51, 102, 0.1);
}
.sr-score {
    font-size: 5rem;
    font-weight: 900;
    background: linear-gradient(135deg, var(--primary-light), var(--primary-dark));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
    margin-bottom: 5px;
    letter-spacing: -2px;
}
.sr-score span {
    font-size: 1.5rem;
    color: var(--text-gray);
    font-weight: 700;
    -webkit-text-fill-color: var(--text-gray);
    letter-spacing: normal;
}
.sr-stars {
    color: #f59e0b;
    font-size: 1.5rem;
    margin-bottom: 8px;
    filter: drop-shadow(0 2px 4px rgba(245, 158, 11, 0.3));
}
.sr-total {
    font-size: 1rem;
    color: var(--text-gray);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.sr-bars {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 12px;
}
.sr-bar-row {
    display: flex;
    align-items: center;
    gap: 20px;
    font-size: 0.95rem;
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
    height: 12px;
    background: rgba(0, 51, 102, 0.05);
    border-radius: 6px;
    overflow: hidden;
    position: relative;
}
.sr-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--primary-light), var(--primary));
    border-radius: 6px;
    position: relative;
    box-shadow: 0 0 10px rgba(0, 76, 153, 0.4);
}
.sr-count {
    min-width: 50px;
    text-align: right;
    color: var(--text-gray);
    font-variant-numeric: tabular-nums;
}

/* Comments List */
.shopee-comments-list {
    max-width: 900px;
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
    padding: 35px;
    border: 1px solid rgba(0, 51, 102, 0.05);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03);
    display: flex;
    gap: 25px;
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
.shopee-comment-item:hover {
    box-shadow: 0 20px 40px rgba(0, 51, 102, 0.08);
    transform: translateY(-4px);
    border-color: rgba(0, 51, 102, 0.15);
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
    box-shadow: 0 8px 15px rgba(0, 51, 102, 0.25);
    border: 2px solid var(--bg-white);
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
    margin-bottom: 2px;
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
    background: linear-gradient(135deg, rgba(0, 76, 153, 0.04), rgba(0, 76, 153, 0.01));
    border-left: 4px solid var(--primary);
    padding: 18px 24px;
    border-radius: 0 var(--radius-md) var(--radius-md) 0;
    margin-bottom: 18px;
    position: relative;
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
    margin-bottom: 18px;
    border: 1px solid rgba(0, 51, 102, 0.08);
    box-shadow: 0 4px 10px rgba(0,0,0,0.02);
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
.sc-helpful {
    font-size: 0.85rem;
    color: var(--text-gray);
    display: inline-flex;
    align-items: center;
    gap: 6px;
    cursor: pointer;
    transition: all 0.3s ease;
    padding: 6px 14px;
    border-radius: var(--radius-pill);
    background: rgba(0,0,0,0.03);
    font-weight: 600;
}
.sc-helpful:hover {
    color: var(--bg-white);
    background: var(--primary);
    box-shadow: 0 4px 10px rgba(0, 51, 102, 0.2);
}

@media (max-width: 768px) {
    .shopee-rating-summary {
        flex-direction: column;
        gap: 30px;
        padding: 30px;
    }
    .sr-overview {
        padding-right: 0;
        border-right: none;
        border-bottom: 1px solid rgba(0, 51, 102, 0.1);
        padding-bottom: 30px;
        width: 100%;
    }
    .shopee-comment-item {
        flex-direction: column;
        gap: 20px;
        padding: 25px;
    }
    .sc-avatar {
        width: 45px;
        height: 45px;
        font-size: 1.4rem;
    }
}

/* Dark Theme Overrides */
[data-theme="dark"] .shopee-reviews-section {
    background: #0b1120;
}
[data-theme="dark"] .shopee-reviews-section::before {
    background: radial-gradient(ellipse at center, rgba(59, 130, 246, 0.1) 0%, transparent 70%);
}
[data-theme="dark"] .shopee-rating-summary {
    background: linear-gradient(145deg, #1e293b, #0f172a);
    border-color: rgba(255,255,255,0.05);
    box-shadow: 0 20px 40px rgba(0,0,0,0.5);
}
[data-theme="dark"] .shopee-comment-item {
    background: #1e293b;
    border-color: rgba(255,255,255,0.05);
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}
[data-theme="dark"] .shopee-comment-item:hover {
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    border-color: rgba(255,255,255,0.1);
}
[data-theme="dark"] .sr-overview { border-color: rgba(255,255,255,0.1); }
[data-theme="dark"] .sr-score { 
    background: linear-gradient(135deg, #60a5fa, #3b82f6);
    -webkit-background-clip: text;
}
[data-theme="dark"] .sr-progress { background: rgba(0,0,0,0.3); }
[data-theme="dark"] .sr-bar-row { color: #cbd5e1; }
[data-theme="dark"] .sr-fill { background: linear-gradient(90deg, #3b82f6, #60a5fa); box-shadow: 0 0 10px rgba(59, 130, 246, 0.5); }
[data-theme="dark"] .sc-avatar { border-color: #1e293b; background: linear-gradient(135deg, #3b82f6, #1d4ed8); }
[data-theme="dark"] .sc-reply-box { background: rgba(59, 130, 246, 0.05); border-left-color: #3b82f6; }
[data-theme="dark"] .sc-product-card { background: #0f172a; border-color: rgba(255,255,255,0.05); }
[data-theme="dark"] .sc-username, 
[data-theme="dark"] .sc-product-name, 
[data-theme="dark"] .sc-reply-text {
    color: #f8fafc;
}
[data-theme="dark"] .sc-reply-title { color: #60a5fa; }
[data-theme="dark"] .sc-helpful { background: rgba(255,255,255,0.05); }
[data-theme="dark"] .sc-helpful:hover { background: #3b82f6; color: #fff; box-shadow: 0 4px 10px rgba(59, 130, 246, 0.3); }
"""

css_content = old_css_pattern.sub(new_css, css_content)
with open('assets/style.css', 'w', encoding='utf-8') as f:
    f.write(css_content)

print("CSS Upgraded to Premium Style")
