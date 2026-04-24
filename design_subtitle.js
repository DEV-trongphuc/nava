const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

const oldHeader = `<div class="section-header text-center mb-5" style="margin-bottom: 40px; text-align: center;">
                <h2 class="section-title">NHU CẦU CỦA BẠN LÀ GÌ?</h2>
                <p class="bento-subtitle" style="color: var(--text-gray);">Các giải pháp chuyên biệt từ NAVA STORE đáp
                    ứng hoàn hảo hai nhóm nhu cầu lớn nhất</p>
            </div>`;

const newHeader = `<div class="section-header" style="margin-bottom: 40px; align-items: center;">
                <h2 class="section-title">NHU CẦU CỦA BẠN LÀ GÌ?</h2>
                <div class="header-callout-pill" style="display: flex; align-items: center; gap: 15px; background: white; padding: 12px 25px; border-radius: 9999px; border: 1px dashed var(--border-color); box-shadow: 0 4px 15px rgba(0,0,0,0.03); max-width: 500px; text-align: left;">
                    <div style="background: rgba(0, 51, 102, 0.08); padding: 10px; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                        <i class="ph-fill ph-target" style="font-size: 1.4rem; color: var(--primary);"></i>
                    </div>
                    <p style="margin: 0; font-size: 0.95rem; color: var(--text-gray); line-height: 1.5;">Các giải pháp chuyên biệt từ <strong style="color: var(--primary); font-weight: 800;">NAVA STORE</strong> đáp ứng hoàn hảo hai nhóm nhu cầu lớn nhất.</p>
                </div>
            </div>`;

html = html.replace(oldHeader, newHeader);
fs.writeFileSync('index.html', html);
console.log('done fixing header');
