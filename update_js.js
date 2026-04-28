const fs = require('fs');
let content = fs.readFileSync('assets/main.js', 'utf8');
content = content.replace(/['"]assets\/([^'"]+)['"]/g, '"https://nava-one.vercel.app/assets/$1"');
fs.writeFileSync('assets/main.js', content, 'utf8');
console.log('assets/main.js updated');
