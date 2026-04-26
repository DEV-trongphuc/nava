const fs = require('fs');

const indexFile = 'f:/BAO_SAPO/sapo_new/index.html';
let html = fs.readFileSync(indexFile, 'utf8');

// There are 4 closing divs:
// </div> <!-- closes hero-benefits-slider -->
// </div> <!-- closes hero-foot -->
// </div> <!-- closes hero-3d-container -->
// </div> <!-- EXTRA DIV! -->
// We want to replace the last one.
const badPattern = /<\/div>\s*<\/div>\s*<\/div>\s*<\/div>\s*<!-- Scroll Indicator -->/;
html = html.replace(badPattern, `</div>
            </div>
            </div>
        
        <!-- Scroll Indicator -->`);

fs.writeFileSync(indexFile, html);
console.log('Removed extra div');
