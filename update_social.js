const fs = require('fs');

function processFile(filename) {
    if (!fs.existsSync(filename)) return;
    let content = fs.readFileSync(filename, 'utf8');

    // 1. Remove floating-contact completely
    content = content.replace(/<!-- Floating Contact Buttons -->[\s\S]*?<\/div>\s*<\/div>/, '');

    // 2. Replace Floating Social Button with the new stack
    const newSocialHtml = `<!-- Floating Social Stack -->
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
        </style>`;

    content = content.replace(/<!-- Floating Social Button -->[\s\S]*?<\/div>\s*<\/div>/, newSocialHtml);

    // Also remove the JavaScript that was animating the old FAB
    content = content.replace(/\/\/ Cycle FAB images[\s\S]*?\/\/ Toggle FAB menu[\s\S]*?\}\);/g, '');

    // Finally, remove the .floating-social-wrapper override that was hiding it
    content = content.replace(/\.floating-social-wrapper\s*\{\s*bottom:\s*-235px\s*!important;\s*\}/g, '');

    fs.writeFileSync(filename, content);
    console.log(filename + ' updated.');
}

processFile('index.html');
processFile('index.bwt');
processFile('update_index_bwt.js');
