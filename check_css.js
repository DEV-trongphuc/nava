const fs = require('fs');
const content = fs.readFileSync('live_home.html', 'utf8');
const lines = content.split('\n');
lines.forEach((l, i) => {
    if (l.includes('rel="stylesheet"') || l.includes("rel='stylesheet'")) {
        console.log(`Line ${i}: ${l.trim()}`);
    }
});
