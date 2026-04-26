const fs = require('fs');
const styleFile = 'f:/BAO_SAPO/sapo_new/assets/style.css';
let css = fs.readFileSync(styleFile, 'utf8');

// 1. Update product card desc font size
// Previous CSS block for TASK 4:
/*
.product-card .card-desc {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
    min-height: 48px; 
}
*/
css = css.replace(/\.product-card \.card-desc \{[\s\S]*?\}/, `.product-card .card-desc {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
    min-height: 40px;
    font-size: 0.9rem;
    line-height: 1.4;
}`);

// 2. Update Khám phá button
const task1Regex = /\/\* TASK 1: Khám phá glow button \*\/[\s\S]*?\/\* TASK 1: Benefit slider \*\//;
const newTask1Css = `/* TASK 1: Khám phá glow button */
.hero-explore-btn-wrapper {
    position: absolute;
    bottom: -60px;
    left: 50%;
    transform: translateX(-50%);
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
    box-shadow: 0 10px 30px rgba(0, 240, 255, 0.2);
    z-index: 1;
    overflow: hidden;
    transition: 0.3s;
}
.btn-explore-glow:hover {
    color: white;
    transform: scale(1.05);
    box-shadow: 0 15px 40px rgba(0, 240, 255, 0.5);
}
.btn-explore-glow::before {
    content: '';
    position: absolute;
    inset: -3px;
    background: linear-gradient(90deg, #00f0ff, #3385ff, #ff003c, #00f0ff);
    background-size: 300% 100%;
    z-index: -1;
    animation: moveGradient 3s linear infinite;
}
.btn-explore-glow::after {
    content: '';
    position: absolute;
    inset: 2px;
    background: #020617;
    border-radius: var(--radius-pill);
    z-index: -1;
}
@keyframes moveGradient {
    0% { background-position: 0% 50%; }
    100% { background-position: 100% 50%; }
}

/* TASK 1: Benefit slider */`;

css = css.replace(task1Regex, newTask1Css);

fs.writeFileSync(styleFile, css);
console.log('Fixed feedback CSS');
