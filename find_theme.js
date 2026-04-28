const fs = require('fs');
let content = fs.readFileSync('theme.bwt', 'utf8');
const matches = content.match(/src="([^"]+)"/g) || [];
const localPaths = matches.filter(m => !m.includes('http') && !m.includes('//') && !m.includes('{{'));
console.log(localPaths);
