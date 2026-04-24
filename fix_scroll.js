const fs = require('fs');

// Update style.css
let css = fs.readFileSync('assets/style.css', 'utf8');
css = css.replace('transform: translateY(-110px);', 'transform: translateY(calc(-1 * var(--top-bar-height, 81px)));');
css = css.replace('transform: translateY(-115px);', 'transform: translateY(calc(-1 * var(--top-bar-height, 150px)));');
fs.writeFileSync('assets/style.css', css);

// Update main.js
let js = fs.readFileSync('assets/main.js', 'utf8');
const heightLogic = `
    // Dynamic top-bar height calculation for sticky header
    const updateTopBarHeight = () => {
        const topBar = document.querySelector('.top-bar');
        if (topBar && header) {
            header.style.setProperty('--top-bar-height', \`\${topBar.offsetHeight}px\`);
        }
    };
    updateTopBarHeight();
    window.addEventListener('resize', updateTopBarHeight);
`;

js = js.replace("const header = document.querySelector('.header');", "const header = document.querySelector('.header');\n" + heightLogic);
fs.writeFileSync('assets/main.js', js);
console.log('done fixing scroll height');
