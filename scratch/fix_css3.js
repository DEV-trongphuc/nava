const fs = require('fs');
let css = fs.readFileSync('f:/BAO_SAPO/sapo_new/assets/style.css', 'utf8');

// Replace light blue backgrounds
css = css.replace(/background(-color)?:\s*#(f8faff|eef2fb|f0f4ff)(?=\s*[;}!])/gi, 'background$1: var(--bg-gray)');

// Replace border colors
css = css.replace(/border(-[a-z]+)?:\s*([^;]*)#(e2e8f8|e8edf5)(?=\s*[;}!])/gi, 'border$1: $2var(--border-color)');

// Replace gradients that use light blue colors
css = css.replace(/background(-image)?:\s*linear-gradient\([^;]+#(f8faff|eef2fb|f0f4ff)[^;]+\)(?=\s*[;}!])/gi, 'background$1: var(--bg-gray)');

// Replace hardcoded dark text colors
css = css.replace(/color:\s*#1a1f36(?=\s*[;}!])/gi, 'color: var(--text-dark)');
css = css.replace(/color:\s*#5a6480(?=\s*[;}!])/gi, 'color: var(--text-gray)');

fs.writeFileSync('f:/BAO_SAPO/sapo_new/assets/style.css', css);
console.log("Replaced successfully!");
