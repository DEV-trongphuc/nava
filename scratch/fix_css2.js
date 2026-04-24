const fs = require('fs');
let css = fs.readFileSync('f:/BAO_SAPO/sapo_new/assets/style.css', 'utf8');

// Replace background: #f8fafc;
css = css.replace(/background(-color)?:\s*#f8fafc(?=\s*[;}!])/gi, 'background$1: var(--bg-gray)');

// Replace text dark
css = css.replace(/color:\s*#0f172a(?=\s*[;}!])/gi, 'color: var(--text-dark)');

fs.writeFileSync('f:/BAO_SAPO/sapo_new/assets/style.css', css);
console.log("Replaced extra colors successfully!");
