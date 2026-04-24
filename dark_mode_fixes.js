const fs = require('fs');
let css = fs.readFileSync('assets/style.css', 'utf8');

// 1. Update header-callout-pill to support dark mode
css = css.replace('.header-callout-pill {\n    display: flex;\n    align-items: center;\n    gap: 15px;\n    background: white;', '.header-callout-pill {\n    display: flex;\n    align-items: center;\n    gap: 15px;\n    background: var(--bg-white);');

// 2. Add dark mode overrides for cat-card and btn-white
const darkModeOverrides = `

/* --- DARK MODE OVERRIDES --- */
[data-theme="dark"] .cat-card {
    background: rgba(255, 255, 255, 0.05);
    border-color: rgba(255, 255, 255, 0.05);
}

[data-theme="dark"] .cat-card:hover {
    background: rgba(255, 255, 255, 0.1);
}

[data-theme="dark"] .cta-neon-box .btn-white {
    background: var(--primary);
    color: #fff;
    box-shadow: 0 4px 15px rgba(51, 133, 255, 0.4);
}

[data-theme="dark"] .cta-neon-box .btn-white:hover {
    background: var(--primary-light);
    transform: translateY(-3px);
}
`;

if (!css.includes('[data-theme="dark"] .cat-card {')) {
    css += darkModeOverrides;
}

fs.writeFileSync('assets/style.css', css);
console.log('done updating dark mode');
