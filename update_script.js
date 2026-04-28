const fs = require('fs');
let content = fs.readFileSync('update_index_bwt.js', 'utf8');

const repl = `
// Inject Liquid for Cart Badge
bodyContent = bodyContent.replace(
    /<span class="cart-count-badge" id="cart-count-badge" style="display: none;">0<\\/span>/g,
    '<span class="cart-count-badge" id="cart-count-badge" {% if cart.item_count > 0 %}style="display: flex;"{% else %}style="display: none;"{% endif %}>{{ cart.item_count }}</span>'
);

`;

content = content.replace('fs.writeFileSync', repl + 'fs.writeFileSync');
fs.writeFileSync('update_index_bwt.js', content, 'utf8');
console.log('Updated update_index_bwt.js');
