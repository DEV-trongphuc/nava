const fs = require('fs');

let css = fs.readFileSync('f:/BAO_SAPO/sapo_new/assets/style.css', 'utf8');

// Replace background: white; or background: #fff; with background: var(--bg-white);
css = css.replace(/background(-color)?:\s*(white|#fff|#ffffff)(?=\s*[;}!])/gi, 'background$1: var(--bg-white)');

// Replace text-gray with var
css = css.replace(/color:\s*(#475569|#64748b)(?=\s*[;}!])/gi, 'color: var(--text-gray)');

// Some rgba for header
css = css.replace(/background:\s*rgba\(255,\s*255,\s*255,\s*0\.95\)/gi, 'background: var(--bg-header, rgba(255, 255, 255, 0.95))');

// rgba for float items
css = css.replace(/background:\s*rgba\(255,\s*255,\s*255,\s*0\.9\)/gi, 'background: var(--bg-float, rgba(255, 255, 255, 0.9))');

fs.writeFileSync('f:/BAO_SAPO/sapo_new/assets/style.css', css);

console.log("Replaced successfully!");
