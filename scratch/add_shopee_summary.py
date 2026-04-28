import re

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Insert the shopee-rating-summary before shopeeCommentsList
pattern = re.compile(r'(<div class="shopee-comments-list" id="shopeeCommentsList">)')
summary_html = '''<div class="shopee-rating-summary" id="shopeeRatingSummary" style="display: none;">
                    <!-- JS will populate rating summary here -->
                </div>
                '''
new_content = pattern.sub(summary_html + r'\1', content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

# 2. Update style.css
css = """
/* --- SHOPEE RATING SUMMARY --- */
.shopee-rating-summary {
    max-width: 900px;
    margin: 0 auto 30px auto;
    background: var(--bg-white);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 30px;
    display: flex;
    align-items: center;
    gap: 40px;
}
.sr-overview {
    text-align: center;
    flex-shrink: 0;
    padding-right: 40px;
    border-right: 1px solid var(--border-color);
}
.sr-score {
    font-size: 3.5rem;
    font-weight: 800;
    color: #ee4d2d;
    line-height: 1;
    margin-bottom: 8px;
}
.sr-score span {
    font-size: 1.5rem;
    color: #ee4d2d;
}
.sr-stars {
    color: #ee4d2d;
    font-size: 1.2rem;
    margin-bottom: 5px;
}
.sr-total {
    font-size: 0.9rem;
    color: var(--text-gray);
}
.sr-bars {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 8px;
}
.sr-bar-row {
    display: flex;
    align-items: center;
    gap: 15px;
    font-size: 0.85rem;
    color: var(--text-dark);
}
.sr-star-label {
    min-width: 45px;
    display: flex;
    align-items: center;
    gap: 4px;
}
.sr-star-label i {
    color: #f59e0b;
}
.sr-progress {
    flex: 1;
    height: 8px;
    background: #f1f5f9;
    border-radius: 4px;
    overflow: hidden;
}
.sr-fill {
    height: 100%;
    background: #ee4d2d;
    border-radius: 4px;
}
.sr-count {
    min-width: 40px;
    text-align: right;
    color: var(--text-gray);
}

@media (max-width: 600px) {
    .shopee-rating-summary {
        flex-direction: column;
        gap: 20px;
        padding: 20px;
    }
    .sr-overview {
        padding-right: 0;
        border-right: none;
        border-bottom: 1px solid var(--border-color);
        padding-bottom: 20px;
        width: 100%;
    }
}
[data-theme="dark"] .shopee-rating-summary {
    background: #1e293b;
    border-color: rgba(255,255,255,0.05);
}
[data-theme="dark"] .sr-overview { border-color: rgba(255,255,255,0.05); }
[data-theme="dark"] .sr-progress { background: #0f172a; }
[data-theme="dark"] .sr-bar-row { color: #e2e8f0; }
"""

with open('assets/style.css', 'a', encoding='utf-8') as f:
    f.write(css)

# 3. Update main.js
with open('assets/main.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Add the rating summary fetch logic to fetchShopeeReviews
old_js_fetch = """        async function fetchShopeeReviews() {
            try {
                // Fetching realtime from shopee API
                const response = await fetch(shopeeApiUrl, {
                    headers: { 'Accept': 'application/json' }
                });
                if (!response.ok) throw new Error('Network error');
                const data = await response.json();
                
                if (data && data.data && data.data.items) {
                    renderShopeeReviews(data.data.items);
                } else {
                    throw new Error('Invalid data');
                }
            } catch (error) {
                console.warn("Shopee API blocked by CORS. Using fallback data.", error);
                renderShopeeReviews(getMockShopeeData());
            }
        }"""

new_js_fetch = """        const shopeeSummaryUrl = 'https://shopee.vn/api/v4/seller_operation/get_rating_summary_new?shop_id=65856601&userid=65858058';
        const summaryEl = document.getElementById('shopeeRatingSummary');

        async function fetchShopeeReviews() {
            try {
                // Fetch reviews and summary concurrently
                const [resReviews, resSummary] = await Promise.all([
                    fetch(shopeeApiUrl, { headers: { 'Accept': 'application/json' } }).catch(() => null),
                    fetch(shopeeSummaryUrl, { headers: { 'Accept': 'application/json' } }).catch(() => null)
                ]);

                if (resSummary && resSummary.ok) {
                    const dataSum = await resSummary.json();
                    if (dataSum && dataSum.data && dataSum.data.seller_rating_summary) {
                        renderShopeeSummary(dataSum.data.seller_rating_summary);
                    }
                } else {
                    throw new Error("Summary fetch failed");
                }

                if (resReviews && resReviews.ok) {
                    const dataRev = await resReviews.json();
                    if (dataRev && dataRev.data && dataRev.data.items) {
                        renderShopeeReviews(dataRev.data.items);
                    }
                } else {
                    throw new Error("Reviews fetch failed");
                }
            } catch (error) {
                console.warn("Shopee API blocked by CORS or error. Using fallback data.", error);
                renderShopeeSummary(getMockShopeeSummary());
                renderShopeeReviews(getMockShopeeData());
            }
        }

        function renderShopeeSummary(summary) {
            if (!summaryEl) return;
            const total = summary.rating_total || 2419;
            const starStr = Number(summary.rating_star || 4.97).toFixed(1);
            // array mapping to 1, 2, 3, 4, 5 stars
            const counts = summary.rating_count || [3, 1, 7, 23, 2385];
            
            // Build bars (from 5 down to 1)
            let barsHtml = '';
            for (let i = 5; i >= 1; i--) {
                const count = counts[i-1] || 0;
                const percent = total > 0 ? (count / total) * 100 : 0;
                barsHtml += `
                <div class="sr-bar-row">
                    <span class="sr-star-label">${i} <i class="ph-fill ph-star"></i></span>
                    <div class="sr-progress"><div class="sr-fill" style="width: ${percent}%"></div></div>
                    <span class="sr-count">${count}</span>
                </div>`;
            }

            // Overview stars
            const scoreNum = parseFloat(starStr);
            let starsHtml = '';
            for(let i=1; i<=5; i++) {
                if (i <= scoreNum) {
                    starsHtml += '<i class="ph-fill ph-star"></i>';
                } else if (i - 0.5 <= scoreNum) {
                    starsHtml += '<i class="ph-fill ph-star-half"></i>';
                } else {
                    starsHtml += '<i class="ph ph-star"></i>'; // empty star
                }
            }

            summaryEl.innerHTML = `
                <div class="sr-overview">
                    <div class="sr-score">${starStr} <span>/ 5</span></div>
                    <div class="sr-stars">${starsHtml}</div>
                    <div class="sr-total">${total.toLocaleString()} đánh giá</div>
                </div>
                <div class="sr-bars">
                    ${barsHtml}
                </div>
            `;
            summaryEl.style.display = 'flex';
        }

        function getMockShopeeSummary() {
            return {
                rating_total: 2419,
                rating_count: [3, 1, 7, 23, 2385],
                rating_star: 4.9791485664639445
            };
        }
"""

js_content = js_content.replace(old_js_fetch, new_js_fetch)
with open('assets/main.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Summary added successfully.")
