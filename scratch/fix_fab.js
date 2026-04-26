const fs = require('fs');

// 1. HTML
const indexFile = 'f:/BAO_SAPO/sapo_new/index.html';
let html = fs.readFileSync(indexFile, 'utf8');

const oldFab = '<button class="fab-main" id="fabMainBtn"><i class="ph-fill ph-share-network"></i></button>';
const newFab = `<button class="fab-main" id="fabMainBtn">
            <img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/shopee.png?1774552524367" alt="Shopee" class="fab-cycle-img active">
            <img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/lazada.jpg?1774552524367" alt="Lazada" class="fab-cycle-img">
            <img src="https://bizweb.dktcdn.net/100/543/817/files/tiktok_3247c513-7e3d-4fff-adec-fd98e4ee41c9.png?v=1774553003807" alt="TikTok" class="fab-cycle-img">
            <img src="https://bizweb.dktcdn.net/100/543/817/files/facebook.png?v=1774555111103" alt="Facebook" class="fab-cycle-img">
            <img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/logo_head_2.png?1775454528082" alt="YouTube" class="fab-cycle-img">
        </button>`;
html = html.replace(oldFab, newFab);

const newJs = `        // Cycle FAB images
        setInterval(() => {
            const imgs = document.querySelectorAll('.fab-cycle-img');
            if(imgs.length > 0) {
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

        // Toggle FAB menu`;
html = html.replace('        // Toggle FAB menu', newJs);
fs.writeFileSync(indexFile, html);

// 2. CSS
const styleFile = 'f:/BAO_SAPO/sapo_new/assets/style.css';
let css = fs.readFileSync(styleFile, 'utf8');

// Replace .floating-social-wrapper and .fab-main
css = css.replace(/\.floating-social-wrapper\s*\{[^}]+\}/, `.floating-social-wrapper {
    position: fixed;
    bottom: 110px;
    right: 20px;
    z-index: 999;
    display: flex;
    flex-direction: column-reverse;
    align-items: center;
    gap: 10px;
}`);

css = css.replace(/\.fab-main\s*\{[^}]+\}/, `.fab-main {
    width: 50px; height: 50px;
    border-radius: 50%;
    background: var(--bg-white);
    color: var(--primary);
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    box-shadow: 0 5px 15px rgba(0,0,0,0.15);
    transition: 0.3s;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
}`);

const fabImgCss = `
.fab-cycle-img {
    position: absolute;
    width: 30px; height: 30px;
    object-fit: contain;
    opacity: 0;
    transform: scale(0.5);
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}
.fab-cycle-img.active {
    opacity: 1;
    transform: scale(1);
}
.fab-menu`;
css = css.replace('.fab-menu', fabImgCss);

fs.writeFileSync(styleFile, css);
console.log('Fixed FAB');
