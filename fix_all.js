const fs = require('fs');

function processBwt(filename) {
    if (!fs.existsSync(filename)) return;
    let content = fs.readFileSync(filename, 'utf8');

    // 1. Inject Floating Social Stack and Video AutoPlay Script
    const injectHtml = `
        <!-- Floating Social Stack -->
        <div class="floating-social-stack">
            <a href="https://www.youtube.com/@NavaStore-MiniPC-eGPU" target="_blank" class="social-btn" title="YouTube">
                <img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/logo_head_2.png?1775454528082" alt="YouTube">
            </a>
            <a href="https://www.facebook.com/navastore.vn" target="_blank" class="social-btn" title="Facebook">
                <img src="https://bizweb.dktcdn.net/100/543/817/files/facebook.png?v=1774555111103" alt="Facebook">
            </a>
            <a href="https://www.tiktok.com/@navastore.vn" target="_blank" class="social-btn" title="TikTok">
                <img src="https://bizweb.dktcdn.net/100/543/817/files/tiktok_3247c513-7e3d-4fff-adec-fd98e4ee41c9.png?v=1774553003807" alt="TikTok">
            </a>
            <a href="https://www.lazada.vn/shop/nava-store" target="_blank" class="social-btn" title="Lazada">
                <img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/lazada.jpg?1774552524367" alt="Lazada">
            </a>
            <a href="https://shopee.vn/navastore.vn" target="_blank" class="social-btn" title="Shopee">
                <img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/shopee.png?1774552524367" alt="Shopee">
            </a>
        </div>
        <style>
        .floating-social-stack {
            position: fixed;
            bottom: 30px;
            right: 20px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            z-index: 50;
        }
        .floating-social-stack .social-btn {
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background: white;
            box-shadow: 0 4px 10px rgba(0,0,0,0.15);
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.3s ease;
            overflow: hidden;
            border: 2px solid white;
        }
        .floating-social-stack .social-btn:hover {
            transform: scale(1.1) translateY(-2px);
        }
        .floating-social-stack .social-btn img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        @media (max-width: 768px) {
            .floating-social-stack {
                bottom: 20px;
                right: 15px;
            }
            .floating-social-stack .social-btn {
                width: 38px;
                height: 38px;
            }
        }
        </style>

        <!-- Auto-play first video -->
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                const firstVideoThumb = document.getElementById('first-video-thumb');
                if (firstVideoThumb) {
                    const observer = new IntersectionObserver((entries) => {
                        if(entries[0].isIntersecting) {
                            firstVideoThumb.innerHTML = '<iframe width="100%" height="100%" src="https://www.youtube.com/embed/Syk0rwciis4?autoplay=1&mute=1&controls=1&rel=0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen style="position:absolute; top:0; left:0; width:100%; height:100%; z-index: 10;"></iframe>';
                            observer.disconnect();
                        }
                    }, { threshold: 0.5 });
                    observer.observe(firstVideoThumb);
                }
            });
        </script>
    `;

    if (!content.includes('floating-social-stack')) {
        content = content.replace('<!-- /MASTER SAPO ESCAPE WRAPPER -->', injectHtml + '\n        <!-- /MASTER SAPO ESCAPE WRAPPER -->');
    }

    // 2. Fix CSS for .benefit-card-mini 3D hover and .benefit-pair transition
    const benefitCSS = `
/* Benefit 3D Hover & Slower Track */
.benefit-card-mini {
    transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease !important;
    transform-style: preserve-3d;
    perspective: 1000px;
}
.benefit-card-mini:hover {
    transform: translateY(-8px) rotateX(4deg) rotateY(-4deg) scale(1.03) !important;
    box-shadow: -5px 15px 30px rgba(0, 51, 102, 0.15) !important;
    z-index: 10;
}
.benefit-pair {
    transition: opacity 1s ease-in-out !important;
}
`;
    if (!content.includes('.benefit-card-mini:hover')) {
        content = content.replace('/* Policy 3D Hover & Slower Track */', benefitCSS + '\n/* Policy 3D Hover & Slower Track */');
    }

    // 3. Update Vercel Script Version
    content = content.replace(/assets\/main\.js\?v=[^"]+/, 'assets/main.js?v=' + Date.now());

    fs.writeFileSync(filename, content);
    console.log(filename + ' updated.');
}

function processMainJs() {
    const filename = 'assets/main.js';
    if (!fs.existsSync(filename)) return;
    let content = fs.readFileSync(filename, 'utf8');

    // Add limit=6 to shopee API
    if (!content.includes('limit=6')) {
        content = content.replace(/shopee_proxy\.php\?type=reviews/g, 'shopee_proxy.php?type=reviews&limit=6');
    }

    fs.writeFileSync(filename, content);
    console.log(filename + ' updated.');
}

processBwt('index.bwt');
processBwt('index.html');
processBwt('update_index_bwt.js');
processMainJs();
