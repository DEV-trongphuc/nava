const fs = require('fs');
const path = require('path');

const indexFile = 'f:/BAO_SAPO/sapo_new/index.html';
const styleFile = 'f:/BAO_SAPO/sapo_new/assets/style.css';

let html = fs.readFileSync(indexFile, 'utf8');

// 1. Remove span from mini-pc-menu
html = html.replace(/<a href="([^"]+)" class="mega-card"><img([^>]+)><span>Mini PC ([^<]+)<\/span><\/a>/g, '<a href="$1" class="mega-card"><img$2></a>');

// 2. Remove Slide Dots and add Khám phá button
const dotsRegex = /<!-- Slide Dots -->\s*<div class="hero-slide-dots" id="heroSlideDots">[\s\S]*?<\/div>/;
html = html.replace(dotsRegex, `<!-- Slide Dots Removed -->
                    <div class="hero-explore-btn-wrapper">
                        <a href="#products" class="btn-explore-glow">Khám phá</a>
                    </div>`);

// 3. Replace hero-cta and hero-socials with hero-benefits-slider
const heroFootRegex = /<div class="hero-cta">[\s\S]*?<\/div>\s*<\/div>/; // matches up to the end of hero-foot div
const newHeroFoot = `<div class="hero-benefits-slider" id="heroBenefitsSlider">
                        <div class="benefit-pair bp-active">
                            <div class="benefit-card-mini">
                                <div class="b-icon-mini"><i class="ph-fill ph-rocket"></i></div>
                                <div>
                                    <h4>Giao Hàng Hỏa Tốc</h4>
                                    <p>Nhận hàng trong 2H nội thành</p>
                                </div>
                            </div>
                            <div class="benefit-card-mini">
                                <div class="b-icon-mini"><i class="ph-fill ph-shield-check"></i></div>
                                <div>
                                    <h4>Bảo Hành Từ 12 Tháng</h4>
                                    <p>1 đổi 1 trong 30 ngày</p>
                                </div>
                            </div>
                        </div>
                        <div class="benefit-pair">
                            <div class="benefit-card-mini">
                                <div class="b-icon-mini"><i class="ph-fill ph-medal"></i></div>
                                <div>
                                    <h4>Cam Kết Chính Hãng</h4>
                                    <p>Sản phẩm ủy quyền</p>
                                </div>
                            </div>
                            <div class="benefit-card-mini">
                                <div class="b-icon-mini"><i class="ph-fill ph-headset"></i></div>
                                <div>
                                    <h4>Hỗ Trợ Trọn Đời</h4>
                                    <p>Kỹ thuật viên 24/7</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>`;
html = html.replace(/<div class="hero-cta">[\s\S]*?<\/div>\s*<\/div>/, newHeroFoot);

// 4. Remove benefits-section
html = html.replace(/<!-- Why Choose Us \(Benefits Block\) -->\s*<section class="benefits-section">[\s\S]*?<\/section>/, '');

// 5. Change section title
html = html.replace('<h2 class="section-title">SIÊU PHẨM CÔNG NGHỆ</h2>', '<h2 class="section-title">Hệ Sinh Thái Mini PC & eGPU Cao Cấp</h2>');

// 6. Update Product Cards
// Remove "Mini PC" from title
html = html.replace(/<h2 class="card-title">Mini PC ([^<]+)<\/h2>/g, '<h2 class="card-title">$1</h2>');
html = html.replace(/<h2 class="card-title">ASUS NUC Mini PC<\/h2>/g, '<h2 class="card-title">ASUS NUC</h2>');
html = html.replace(/<h2 class="card-title">Hệ thống eGPU<\/h2>/g, '<h2 class="card-title">eGPU</h2>');

// Replace card actions with single Khám phá button
html = html.replace(/<div class="card-actions">\s*<a href="([^"]+)" class="btn-pill btn-blue">Tìm hiểu thêm<\/a>\s*<a href="([^"]+)" class="btn-pill btn-outline">Mua ngay<\/a>\s*<\/div>/g, 
`<div class="card-actions">
                            <a href="$1" class="btn-pill btn-blue">Khám phá</a>
                        </div>`);

// 7. Add Floating Social Button at the end of body
const fabHtml = `
    <!-- Floating Social Button -->
    <div class="floating-social-wrapper">
        <button class="fab-main" id="fabMainBtn"><i class="ph-fill ph-share-network"></i></button>
        <div class="fab-menu" id="fabMenu">
            <a href="https://shopee.vn/navastore.vn" target="_blank" title="Shopee" class="fab-item"><img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/shopee.png?1774552524367" alt="Shopee"></a>
            <a href="https://www.lazada.vn/shop/nava-store" target="_blank" title="Lazada" class="fab-item"><img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/lazada.jpg?1774552524367" alt="Lazada"></a>
            <a href="https://www.tiktok.com/@navastore.vn" target="_blank" title="TikTok" class="fab-item"><img src="https://bizweb.dktcdn.net/100/543/817/files/tiktok_3247c513-7e3d-4fff-adec-fd98e4ee41c9.png?v=1774553003807" alt="TikTok"></a>
            <a href="https://www.facebook.com/navastore.vn/" target="_blank" title="Facebook" class="fab-item"><img src="https://bizweb.dktcdn.net/100/543/817/files/facebook.png?v=1774555111103" alt="Facebook"></a>
            <a href="https://www.youtube.com/@NAVASTORE-VN" target="_blank" title="YouTube" class="fab-item"><img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/logo_head_2.png?1775454528082" alt="YouTube"></a>
        </div>
    </div>
    
    <script>
        // Cycle benefit cards
        setInterval(() => {
            const active = document.querySelector('.bp-active');
            if (active) {
                const next = active.nextElementSibling || active.parentElement.firstElementChild;
                active.classList.remove('bp-active');
                next.classList.add('bp-active');
            }
        }, 4000);

        // Toggle FAB menu
        document.getElementById('fabMainBtn').addEventListener('click', function() {
            document.getElementById('fabMenu').classList.toggle('active');
        });
        
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.floating-social-wrapper')) {
                document.getElementById('fabMenu').classList.remove('active');
            }
        });
    </script>
</body>`;
html = html.replace('</body>', fabHtml);

fs.writeFileSync(indexFile, html);

let css = fs.readFileSync(styleFile, 'utf8');

// Fix Product Card Hover actions
// Also limit card-desc to 2 lines
const newCss = `
/* TASK 1: Khám phá glow button */
.hero-explore-btn-wrapper {
    position: absolute;
    bottom: -20px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 20;
}
.btn-explore-glow {
    position: relative;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 12px 40px;
    background: #003366;
    color: white;
    font-weight: 700;
    font-size: 1.1rem;
    border-radius: var(--radius-pill);
    text-transform: uppercase;
    letter-spacing: 1px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    z-index: 1;
}
.btn-explore-glow:hover {
    color: white;
}
.btn-explore-glow::before {
    content: '';
    position: absolute;
    top: -2px; left: -2px; right: -2px; bottom: -2px;
    background: linear-gradient(90deg, #00f0ff, #003366, #3385ff, #00f0ff);
    background-size: 400%;
    z-index: -1;
    border-radius: var(--radius-pill);
    animation: glowBorder 4s linear infinite;
}
.btn-explore-glow::after {
    content: '';
    position: absolute;
    top: 2px; left: 2px; right: 2px; bottom: 2px;
    background: var(--primary);
    border-radius: var(--radius-pill);
    z-index: -1;
}
@keyframes glowBorder {
    0% { background-position: 0% 50%; }
    100% { background-position: 400% 50%; }
}

/* TASK 1: Benefit slider */
.hero-benefits-slider {
    position: relative;
    height: 100px;
    margin-top: 20px;
    width: 100%;
    max-width: 500px;
}
.benefit-pair {
    position: absolute;
    top: 0; left: 0; right: 0;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.5s ease;
}
.benefit-pair.bp-active {
    opacity: 1;
    visibility: visible;
}
.benefit-card-mini {
    display: flex;
    align-items: center;
    gap: 12px;
    background: var(--bg-white);
    padding: 12px 15px;
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border-color);
}
.b-icon-mini {
    font-size: 1.8rem;
    color: var(--primary);
    background: rgba(0, 51, 102, 0.1);
    width: 40px; height: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 50%;
    flex-shrink: 0;
}
.benefit-card-mini h4 {
    font-size: 0.95rem;
    font-weight: 700;
    margin-bottom: 2px;
    line-height: 1.2;
}
.benefit-card-mini p {
    font-size: 0.75rem;
    color: var(--text-gray);
    margin: 0;
    line-height: 1.2;
}

/* TASK 2: FAB Menu */
.floating-social-wrapper {
    position: fixed;
    bottom: 80px;
    right: 20px;
    z-index: 999;
    display: flex;
    flex-direction: column-reverse;
    align-items: center;
    gap: 10px;
}
.fab-main {
    width: 50px; height: 50px;
    border-radius: 50%;
    background: var(--primary);
    color: white;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    box-shadow: var(--shadow-lg);
    transition: 0.3s;
    display: flex;
    justify-content: center;
    align-items: center;
}
.fab-main:hover {
    transform: scale(1.1);
    background: var(--primary-light);
}
.fab-menu {
    display: flex;
    flex-direction: column;
    gap: 10px;
    opacity: 0;
    visibility: hidden;
    transform: translateY(20px);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.fab-menu.active {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
}
.fab-item {
    width: 40px; height: 40px;
    border-radius: 50%;
    background: var(--bg-white);
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: var(--shadow-md);
    transition: 0.3s;
    border: 1px solid var(--border-color);
}
.fab-item img {
    width: 24px; height: 24px;
    object-fit: contain;
}
.fab-item:hover {
    transform: scale(1.1) translateX(-5px);
}

/* TASK 3: Drop Mini PC logo center */
.mini-pc-menu .mega-card {
    justify-content: center;
}
.mini-pc-menu .mega-card img {
    width: 100px;
    height: 40px;
    object-fit: contain;
}

/* TASK 4: Products */
.product-card .card-actions {
    position: absolute;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%) translateY(20px);
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
    width: 100%;
    display: flex;
    justify-content: center;
    z-index: 20;
}
.product-card:hover .card-actions {
    opacity: 1;
    visibility: visible;
    transform: translateX(-50%) translateY(0);
}
.product-card .card-desc {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
    min-height: 48px; /* 2 lines ~ 24px each */
}
`;

fs.writeFileSync(styleFile, css + newCss);
console.log('Done');
