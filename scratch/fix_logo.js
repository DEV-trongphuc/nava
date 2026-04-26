const fs = require('fs');
const styleFile = 'f:/BAO_SAPO/sapo_new/assets/style.css';
let css = fs.readFileSync(styleFile, 'utf8');

// Replace the logo size css
css = css.replace(/\.mini-pc-menu \.mega-card img\s*\{[^}]+\}/, `.mini-pc-menu .mega-card img {
    width: 150px;
    height: 60px;
    object-fit: contain;
}`);

fs.writeFileSync(styleFile, css);
console.log('Fixed logo size');
