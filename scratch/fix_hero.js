const fs = require('fs');

// 1. Update HTML
const indexFile = 'f:/BAO_SAPO/sapo_new/index.html';
let html = fs.readFileSync(indexFile, 'utf8');

const btnHtml = `<div class="hero-explore-btn-wrapper">
                        <a href="#products" class="btn-explore-glow">Khám phá</a>
                    </div>`;

// Remove the button wrapper from its current location
html = html.replace(/<!-- Slide Dots Removed -->\s*<div class="hero-explore-btn-wrapper">[\s\S]*?<\/div>/, '<!-- Slide Dots Removed -->');

// Insert it at the end of hero-3d-container
// Look for the end of hero-foot which is </div> </div> </div> 
// Wait, the structure in hero-3d is:
// <div class="container hero-3d-container">
//   <div class="hero-head">...</div>
//   <div class="hero-image">...</div>
//   <div class="hero-foot">...</div>
// </div>
// Let's just insert it right after the hero-foot div closes
html = html.replace(/(<div class="hero-benefits-slider" id="heroBenefitsSlider">[\s\S]*?<\/div>\s*<\/div>)/, `$1\n                    ${btnHtml}`);

fs.writeFileSync(indexFile, html);

// 2. Update CSS
const styleFile = 'f:/BAO_SAPO/sapo_new/assets/style.css';
let css = fs.readFileSync(styleFile, 'utf8');

// Update .floating-pc
css = css.replace(/\.floating-pc\s*\{[^}]+\}/, `.floating-pc {
    position: relative;
    max-width: 110%;
    max-height: 110%;
    z-index: 10;
    transform: scale(1.05) translate(0, 5%);
    animation: float 6s ease-in-out infinite;
    filter: drop-shadow(0 30px 40px rgba(0, 0, 0, 0.15));
}`);

// Update TASK 1 CSS Block
const task1Regex = /\/\* TASK 1: Khám phá glow button \*\/[\s\S]*?\/\* TASK 2: FAB Menu \*\//;
const newTask1Css = `/* TASK 1: Khám phá glow button */
.hero-explore-btn-wrapper {
    grid-column: 1 / -1;
    display: flex;
    justify-content: center;
    margin-top: 40px;
    z-index: 20;
}
.btn-explore-glow {
    position: relative;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 16px 60px;
    background: #020617;
    color: white;
    font-weight: 800;
    font-size: 1.25rem;
    border-radius: var(--radius-pill);
    text-transform: uppercase;
    letter-spacing: 2px;
    box-shadow: 0 10px 30px rgba(0,51,102,0.3);
    z-index: 1;
    overflow: hidden;
    transition: 0.3s;
}
.btn-explore-glow:hover {
    color: white;
    transform: scale(1.05);
    box-shadow: 0 15px 40px rgba(0,240,255,0.4);
}
.btn-explore-glow::before {
    content: '';
    position: absolute;
    width: 250%;
    height: 250%;
    background: conic-gradient(
        transparent 0deg,
        transparent 90deg,
        #00f0ff 180deg,
        transparent 180deg,
        transparent 270deg,
        #3385ff 360deg
    );
    z-index: -1;
    animation: spinClockwise 2.5s linear infinite;
    left: -75%;
    top: -75%;
}
.btn-explore-glow::after {
    content: '';
    position: absolute;
    top: 2px; left: 2px; right: 2px; bottom: 2px;
    background: #020617;
    border-radius: var(--radius-pill);
    z-index: -1;
}
@keyframes spinClockwise {
    100% { transform: rotate(360deg); }
}

/* TASK 1: Benefit slider */
.hero-benefits-slider {
    position: relative;
    height: 180px;
    margin-top: 40px;
    width: 100%;
    max-width: 550px; /* Rộng bằng chữ SỨC MẠNH ĐIỆN TOÁN */
}
.benefit-pair {
    position: absolute;
    top: 0; left: 0; right: 0;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
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
    flex-direction: column;
    align-items: center;
    text-align: center;
    background: var(--bg-white);
    padding: 25px 20px;
    border-radius: var(--radius-md);
    box-shadow: 0 8px 20px rgba(0,0,0,0.06);
    border: 1px solid var(--border-color);
}
.b-icon-mini {
    font-size: 2rem;
    color: var(--primary);
    background: rgba(0, 51, 102, 0.05);
    width: 55px; height: 55px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 50%;
    flex-shrink: 0;
    margin-bottom: 15px;
}
.benefit-card-mini h4 {
    font-size: 1.05rem;
    font-weight: 800;
    margin-bottom: 6px;
    line-height: 1.3;
}
.benefit-card-mini p {
    font-size: 0.85rem;
    color: var(--text-gray);
    margin: 0;
    line-height: 1.3;
}

/* TASK 2: FAB Menu */`;

css = css.replace(task1Regex, newTask1Css);

fs.writeFileSync(styleFile, css);
console.log('Fixed CSS & HTML');
