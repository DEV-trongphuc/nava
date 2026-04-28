import re
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_hero = """        <!-- Hero Section Clean -->
        <section class="hero-clean">
            <div class="container hero-clean-container">
                <div class="hero-clean-left reveal">
                    <h1 class="hero-clean-title">
                        <span class="blue-text">ĐỊNH NGHĨA LẠI</span>
                        <span class="dark-text">SỨC MẠNH ĐIỆN TOÁN</span>
                    </h1>
                    <div class="hero-clean-benefits">
                        <div class="hero-clean-benefit-card">
                            <i class="ph-fill ph-rocket" style="font-size: 24px; color: #0b60d4; margin-bottom: 10px;"></i>
                            <h4>Giao Hàng Hỏa Tốc</h4>
                            <p>Nhận hàng trong 2H nội thành</p>
                        </div>
                        <div class="hero-clean-benefit-card">
                            <i class="ph-fill ph-shield-check" style="font-size: 24px; color: #0b60d4; margin-bottom: 10px;"></i>
                            <h4>Bảo Hành Từ 12 Tháng</h4>
                            <p>1 đổi 1 trong 30 ngày</p>
                        </div>
                    </div>
                </div>

                <div class="hero-clean-right reveal delay-1">
                    <div class="hero-clean-circle"></div>
                    
                    <div class="hero-clean-badge top-left">
                        <i class="ph-fill ph-game-controller" style="font-size: 24px; color: #0b60d4;"></i>
                        <div class="hero-clean-badge-text">
                            <h5>ROG Gaming</h5>
                            <p>Hiệu năng đỉnh</p>
                        </div>
                    </div>

                    <div class="hero-clean-images">
                        <!-- ASUS NUC Standing -->
                        <img src="https://bizweb.dktcdn.net/thumb/large/100/543/817/products/rog-nuc2.png?v=1762858052317" alt="ROG NUC" class="hero-img-1 floating-pc-1">
                        <!-- ASUS NUC Flat -->
                        <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_1_1.png?1775454528082" alt="ASUS NUC" class="hero-img-2 floating-pc-2">
                    </div>

                    <div class="hero-clean-badge bottom-right">
                        <img src="https://images.seeklogo.com/logo-png/66/1/openclaw-logo-png_seeklogo-665449.png" alt="Openclaw">
                        <div class="hero-clean-badge-text">
                            <h5>Openclaw</h5>
                            <p>Sức mạnh vượt trội</p>
                        </div>
                    </div>

                    <div class="hero-clean-dots">
                        <div class="hero-clean-dot"></div>
                        <div class="hero-clean-dot active"></div>
                        <div class="hero-clean-dot"></div>
                        <div class="hero-clean-dot"></div>
                    </div>
                </div>
            </div>
        </section>"""

# Find the block from <!-- Hero Section 3D (Z-Layout) --> to the closing </section>
pattern = re.compile(r'<!-- Hero Section 3D \(Z-Layout\) -->.*?</section>', re.DOTALL)
new_content = pattern.sub(new_hero, content, count=1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
print("Replaced successfully!")
