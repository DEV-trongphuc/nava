const fs = require('fs');

// 1. Update index.html links
let html = fs.readFileSync('index.html', 'utf8');

// Update YouTube links
html = html.replace(/<a href="#" target="_blank" title="YouTube" class="social-btn">/g, '<a href="https://www.youtube.com/@NAVASTORE-VN" target="_blank" title="YouTube" class="social-btn">');
html = html.replace(/<a href="#"><img\s*src="https:\/\/bizweb\.dktcdn\.net\/100\/543\/817\/themes\/1000289\/assets\/logo_head_2\.png/g, '<a href="https://www.youtube.com/@NAVASTORE-VN" target="_blank"><img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/logo_head_2.png');

// Update Floating Zalo Link
html = html.replace(/<a href="https:\/\/zalo\.me\/0972178527" target="_blank" class="sub-btn zalo" title="Chat Zalo">/g, '<a href="https://zalo.me/3182872871563786385" target="_blank" class="sub-btn zalo" title="Chat Zalo">');
fs.writeFileSync('index.html', html);

// 2. Fix the jumping CSS bug
let css = fs.readFileSync('assets/style.css', 'utf8');

css = css.replace('.sub-btn:hover {\n    transform: scale(1.15) !important;\n    z-index: 15;\n}', `.sub-btn:hover { z-index: 15; }
.floating-contact.active .sub-btn.call:hover { transform: translate(-80px, 0) scale(1.15); }
.floating-contact.active .sub-btn.zalo:hover { transform: translate(-60px, -60px) scale(1.15); }
.floating-contact.active .sub-btn.mess:hover { transform: translate(0, -80px) scale(1.15); }`);

fs.writeFileSync('assets/style.css', css);
console.log('done fixing floating buttons');
