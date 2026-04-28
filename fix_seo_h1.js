const fs = require('fs');

// 1. Update index.html
let html = fs.readFileSync('index.html', 'utf8');
// Replace <h1 class="hero-title..."> with <h2 class="hero-title...">
html = html.replace(/<h1 (class="hero-title[^>]*>)/g, '<h2 $1');
html = html.replace(/<\/h1>\s*<p class="hero-desc/g, '</h2>\n                            <p class="hero-desc');
fs.writeFileSync('index.html', html);
console.log('index.html updated');

// 2. Update update_index_bwt.js
let js = fs.readFileSync('update_index_bwt.js', 'utf8');
js = js.replace('NAVA STORE - Chuyên Mini PC, eGPU, Linh kiện máy tính & Đồ họa AI', 'NAVA STORE - Mini PC & eGPU');
fs.writeFileSync('update_index_bwt.js', js);
console.log('update_index_bwt.js updated');
