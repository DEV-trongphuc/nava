const fs = require('fs');

function processBwt(filename) {
    if (!fs.existsSync(filename)) return;
    let content = fs.readFileSync(filename, 'utf8');

    // 1. Inject first-video-thumb ID
    content = content.replace(
        /(<a href="[^"]*Syk0rwciis4"[^>]*>[\s]*<div class=")video-thumb(")/,
        '$1video-thumb" id="first-video-thumb"'
    );

    // 2. Replace floating-social-stack with the old expandable floating-social-wrapper
    const oldSocialHtml = `
        <!-- Floating Social Button -->
        <div class="floating-social-wrapper">
            <button class="fab-main" id="fabMainBtn">
                <img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/shopee.png?1774552524367" alt="Shopee" class="fab-cycle-img active">
                <img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/lazada.jpg?1774552524367" alt="Lazada" class="fab-cycle-img">
                <img src="https://bizweb.dktcdn.net/100/543/817/files/tiktok_3247c513-7e3d-4fff-adec-fd98e4ee41c9.png?v=1774553003807" alt="TikTok" class="fab-cycle-img">
                <img src="https://bizweb.dktcdn.net/100/543/817/files/facebook.png?v=1774555111103" alt="Facebook" class="fab-cycle-img">
                <img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/logo_head_2.png?1775454528082" alt="YouTube" class="fab-cycle-img">
            </button>
            <div class="fab-menu" id="fabMenu">
                <a href="https://shopee.vn/navastore.vn" target="_blank" title="Shopee" class="fab-item"><img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/shopee.png?1774552524367" alt="Shopee"></a>
                <a href="https://www.lazada.vn/shop/nava-store" target="_blank" title="Lazada" class="fab-item"><img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/lazada.jpg?1774552524367" alt="Lazada"></a>
                <a href="https://www.tiktok.com/@navastore.vn" target="_blank" title="TikTok" class="fab-item"><img src="https://bizweb.dktcdn.net/100/543/817/files/tiktok_3247c513-7e3d-4fff-adec-fd98e4ee41c9.png?v=1774553003807" alt="TikTok"></a>
                <a href="https://www.facebook.com/navastore.vn/" target="_blank" title="Facebook" class="fab-item"><img src="https://bizweb.dktcdn.net/100/543/817/files/facebook.png?v=1774555111103" alt="Facebook"></a>
                <a href="https://www.youtube.com/@NAVASTORE-VN" target="_blank" title="YouTube" class="fab-item"><img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/logo_head_2.png?1775454528082" alt="YouTube"></a>
            </div>
        </div>
        <style>
        .floating-social-wrapper {
            position: fixed;
            bottom: 30px;
            right: 20px;
            z-index: 50;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .fab-main {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            border: 2px solid white;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            cursor: pointer;
            position: relative;
            z-index: 51;
            overflow: hidden;
            padding: 0;
            background: white;
            transition: transform 0.3s ease;
        }
        .fab-main:hover {
            transform: scale(1.05);
        }
        .fab-cycle-img {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            object-fit: cover;
            opacity: 0;
            transition: opacity 0.5s ease;
        }
        .fab-cycle-img.active {
            opacity: 1;
        }
        .fab-menu {
            position: absolute;
            bottom: 60px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            opacity: 0;
            visibility: hidden;
            transform: translateY(20px);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            pointer-events: none;
        }
        .fab-menu.active {
            opacity: 1;
            visibility: visible;
            transform: translateY(0);
            pointer-events: auto;
        }
        .fab-item {
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
        .fab-item:hover {
            transform: scale(1.1) translateY(-2px);
        }
        .fab-item img {
            width: 100%; height: 100%; object-fit: cover;
        }
        </style>
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Cycle FAB images
            setInterval(() => {
                const imgs = document.querySelectorAll('.fab-cycle-img');
                if (imgs.length > 0) {
                    let activeIdx = -1;
                    imgs.forEach((img, idx) => {
                        if (img.classList.contains('active')) activeIdx = idx;
                        img.classList.remove('active');
                    });
                    if (activeIdx !== -1) {
                        const nextIdx = (activeIdx + 1) % imgs.length;
                        imgs[nextIdx].classList.add('active');
                    } else {
                        imgs[0].classList.add('active');
                    }
                }
            }, 2500);

            // Toggle FAB menu
            const fabMainBtn = document.getElementById('fabMainBtn');
            if(fabMainBtn) {
                fabMainBtn.addEventListener('click', function () {
                    const fabMenu = document.getElementById('fabMenu');
                    if(fabMenu) fabMenu.classList.toggle('active');
                });
            }

            document.addEventListener('click', function (e) {
                if (!e.target.closest('.floating-social-wrapper')) {
                    const fabMenu = document.getElementById('fabMenu');
                    if(fabMenu) fabMenu.classList.remove('active');
                }
            });
        });
        </script>
`;

    // Remove the floating-social-stack
    content = content.replace(/<!-- Floating Social Stack -->[\s\S]*?<\/style>/, oldSocialHtml);

    // 3. Fix Benefit Slider transition
    const newSliderCSS = `
/* Benefit 3D Hover & Slower Track */
.hero-benefits-slider {
    position: relative;
    overflow: hidden;
}
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
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    transition: transform 0.8s cubic-bezier(0.25, 1, 0.5, 1), opacity 0.8s ease-in-out !important;
    transform: translateX(100%);
    opacity: 0;
    visibility: hidden;
}
.benefit-pair.bp-active {
    transform: translateX(0);
    opacity: 1;
    visibility: visible;
}
.benefit-pair.bp-exit {
    transform: translateX(-100%);
    opacity: 0;
    visibility: hidden;
}
`;

    content = content.replace(/\/\* Benefit 3D Hover & Slower Track \*\/[\s\S]*?\.benefit-pair \{[\s\S]*?\}/, newSliderCSS);

    // Also update JS for bp-exit
    const oldJs = `
        // Cycle benefit cards
        setInterval(() => {
            const active = document.querySelector('.bp-active');
            if (active) {
                const next = active.nextElementSibling || active.parentElement.firstElementChild;
                active.classList.remove('bp-active');
                next.classList.add('bp-active');
            }
        }, 4000);`;
        
    const newJs = `
        // Cycle benefit cards
        setInterval(() => {
            const active = document.querySelector('.bp-active');
            if (active) {
                const next = active.nextElementSibling || active.parentElement.firstElementChild;
                active.classList.remove('bp-active');
                active.classList.add('bp-exit');
                setTimeout(() => { 
                    if(active) active.classList.remove('bp-exit'); 
                }, 800);
                next.classList.add('bp-active');
            }
        }, 5000);`;

    content = content.replace(oldJs, newJs);

    fs.writeFileSync(filename, content);
    console.log(filename + ' updated.');
}

processBwt('index.bwt');
processBwt('index.html');
processBwt('update_index_bwt.js');
