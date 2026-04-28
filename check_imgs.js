const fs = require('fs');
const content = fs.readFileSync('index.html', 'utf8');
const matches = content.match(/src="[^"]+"/g);
if(matches) console.log(matches.slice(0, 30));
