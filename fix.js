const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

// Replace ANY remaining Zalo avatars
html = html.replace(/https:\/\/s120-ava-talk\.zadn\.vn\/3\/5\/0\/c\/2\/120\/81f9e13ab9e5380232f102e36863b648\.jpg/g, 'assets/logo.png');

// Fix 'cực tốc độ'
html = html.replace(/Hiệu suất vượt trội, thiết kế nhôm nguyên khối mang đến trải nghiệm cực tốc\s+độ\./g, 'Hiệu suất mạnh mẽ, thiết kế nhôm nguyên khối mang đến trải nghiệm làm việc mượt mà.');

// Set default theme to light (remove prefers-color-scheme)
html = html.replace(/if \(savedTheme === 'dark' \|\| \(!savedTheme && window\.matchMedia\('\(prefers-color-scheme: dark\)'\)\.matches\)\) \{/g, "if (savedTheme === 'dark') {");

fs.writeFileSync('index.html', html);
console.log('done fixing');
