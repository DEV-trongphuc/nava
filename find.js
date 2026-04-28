const fs = require('fs');
let content = fs.readFileSync('index.bwt', 'utf8');
const matches = content.match(/src="([^"]+)"/g);
const localPaths = matches.filter(m => !m.includes('http') && !m.includes('//') && !m.includes('{{'));
console.log(localPaths);
