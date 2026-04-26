const fs = require('fs');

const indexFile = 'f:/BAO_SAPO/sapo_new/index.html';
let html = fs.readFileSync(indexFile, 'utf8');

// Extract scroll indicator
const scrollRegex = /\s*<!-- Scroll Indicator -->[\s\S]*?<div class="hero-scroll-indicator">[\s\S]*?<\/div>\s*<\/div>/;
const scrollMatch = html.match(scrollRegex);
if (scrollMatch) {
    html = html.replace(scrollMatch[0], '');
    
    // Insert before </section>
    html = html.replace('</section>', `
        <!-- Scroll Indicator -->
        <div class="hero-scroll-indicator">
            <span>Khám phá</span>
            <div class="mouse-icon">
                <div class="wheel"></div>
            </div>
        </div>
    </section>`);
}

fs.writeFileSync(indexFile, html);
console.log('Moved scroll indicator out of transformed parent');
