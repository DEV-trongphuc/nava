const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

// Replace Top Header Social Links
html = html.replace(/<a href="#" target="_blank" title="Shopee" class="social-btn">/g, '<a href="https://shopee.vn/navastore.vn" target="_blank" title="Shopee" class="social-btn">');
html = html.replace(/<a href="#" target="_blank" title="Lazada" class="social-btn">/g, '<a href="https://www.lazada.vn/shop/nava-store" target="_blank" title="Lazada" class="social-btn">');
html = html.replace(/<a href="#" target="_blank" title="TikTok" class="social-btn">/g, '<a href="https://www.tiktok.com/@navastore.vn" target="_blank" title="TikTok" class="social-btn">');
html = html.replace(/<a href="#" target="_blank" title="Facebook" class="social-btn">/g, '<a href="https://www.facebook.com/navastore.vn/" target="_blank" title="Facebook" class="social-btn">');

// Replace Footer Social Links
html = html.replace(/<a href="#">\s*<img\s*src="https:\/\/bizweb\.dktcdn\.net\/100\/543\/817\/themes\/1000289\/assets\/shopee\.png/g, '<a href="https://shopee.vn/navastore.vn" target="_blank"><img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/shopee.png');

html = html.replace(/<a href="#">\s*<img\s*src="https:\/\/bizweb\.dktcdn\.net\/100\/543\/817\/themes\/1000289\/assets\/lazada\.jpg/g, '<a href="https://www.lazada.vn/shop/nava-store" target="_blank"><img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/lazada.jpg');

html = html.replace(/<a href="#">\s*<img\s*src="https:\/\/bizweb\.dktcdn\.net\/100\/543\/817\/files\/tiktok_3247c513-7e3d-4fff-adec-fd98e4ee41c9\.png/g, '<a href="https://www.tiktok.com/@navastore.vn" target="_blank"><img src="https://bizweb.dktcdn.net/100/543/817/files/tiktok_3247c513-7e3d-4fff-adec-fd98e4ee41c9.png');

html = html.replace(/<a href="#">\s*<img src="https:\/\/bizweb\.dktcdn\.net\/100\/543\/817\/files\/facebook\.png/g, '<a href="https://www.facebook.com/navastore.vn/" target="_blank"><img src="https://bizweb.dktcdn.net/100/543/817/files/facebook.png');

// Replace Facebook link inside the modal
html = html.replace(/<a href="https:\/\/facebook\.com\/navastore" target="_blank" class="contact-item fb">/g, '<a href="https://www.facebook.com/navastore.vn/" target="_blank" class="contact-item fb">');

fs.writeFileSync('index.html', html);
console.log('done updating links');
