const fs = require('fs');

// 1. Update HTML
const indexFile = 'f:/BAO_SAPO/sapo_new/index.html';
let html = fs.readFileSync(indexFile, 'utf8');

// Remove the broken Khám phá button
html = html.replace(/<div class="hero-explore-btn-wrapper">[\s\S]*?<\/div>/, '');

// Restore Slide Dots
const slideDotsHtml = `                    <!-- Slide Dots -->
                    <div class="hero-slide-dots" id="heroSlideDots">
                        <button class="h-dot active" data-slide="0"></button>
                        <button class="h-dot" data-slide="1"></button>
                        <button class="h-dot" data-slide="2"></button>
                        <button class="h-dot" data-slide="3"></button>
                        <button class="h-dot" data-slide="4"></button>
                    </div>`;
html = html.replace('<!-- Slide Dots Removed -->', slideDotsHtml);

// Add Scroll Indicator
const scrollIndicatorHtml = `                    <!-- Scroll Indicator -->
                    <div class="hero-scroll-indicator">
                        <span>Khám phá</span>
                        <div class="mouse-icon">
                            <div class="wheel"></div>
                        </div>
                    </div>`;
// Place it just before the end of hero-3d-container
// Look for <div class="hero-benefits-slider"...  and put scrollIndicator just before the closing tag of section hero-3d
// The closing tag of hero-3d-container is just before </section>
html = html.replace(/(<\/div>\s*<\/div>\s*<\/section>)/, `    ${scrollIndicatorHtml}\n            $1`);

fs.writeFileSync(indexFile, html);

// 2. Update CSS
const styleFile = 'f:/BAO_SAPO/sapo_new/assets/style.css';
let css = fs.readFileSync(styleFile, 'utf8');

// Replace the TASK 1: Khám phá glow button section with the scroll indicator styles
const task1Regex = /\/\* TASK 1: Khám phá glow button \*\/[\s\S]*?\/\* TASK 1: Benefit slider \*\//;
const newScrollCss = `/* TASK 1: Khám phá scroll indicator */
.hero-scroll-indicator {
    position: absolute;
    bottom: -60px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    z-index: 20;
    color: var(--primary);
    font-weight: 600;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    animation: bounce 2s infinite;
}
.mouse-icon {
    width: 24px;
    height: 36px;
    border: 2px solid var(--primary);
    border-radius: 12px;
    position: relative;
    display: flex;
    justify-content: center;
}
.wheel {
    width: 4px;
    height: 8px;
    background: var(--primary);
    border-radius: 2px;
    margin-top: 6px;
    animation: scroll 1.5s infinite;
}
@keyframes scroll {
    0% { transform: translateY(0); opacity: 1; }
    100% { transform: translateY(12px); opacity: 0; }
}
@keyframes bounce {
    0%, 20%, 50%, 80%, 100% { transform: translateX(-50%) translateY(0); }
    40% { transform: translateX(-50%) translateY(-10px); }
    60% { transform: translateX(-50%) translateY(-5px); }
}

/* TASK 1: Benefit slider */`;

css = css.replace(task1Regex, newScrollCss);

fs.writeFileSync(styleFile, css);
console.log('Fixed scroll indicator');
