const fs = require('fs');

let html = fs.readFileSync('f:/BAO_SAPO/sapo_new/index.html', 'utf8');

// replace style.css link with a new version query to force reload
html = html.replace(/assets\/style\.css(\?[^"]*)?/, 'assets/style.css?v=' + Date.now());

fs.writeFileSync('f:/BAO_SAPO/sapo_new/index.html', html);
console.log('Bumped CSS version');
