const fs = require('fs');
let content = fs.readFileSync('index.bwt', 'utf8');
content = content.replace(/\{\{\s*'main\.js'\s*\|\s*asset_url\s*\}\}/g, 'https://nava-one.vercel.app/assets/main.js?v=20260426_v1');
fs.writeFileSync('index.bwt', content, 'utf8');
console.log('Replaced in index.bwt');
