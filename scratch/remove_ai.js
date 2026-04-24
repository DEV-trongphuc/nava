const fs = require('fs');

// 1. Remove from HTML
const htmlPath = 'f:/BAO_SAPO/sapo_new/index.html';
let html = fs.readFileSync(htmlPath, 'utf8');

const htmlStart = '    <!-- ===== AI CORE SECTION ===== -->';
const htmlEnd = '    </section>\n';
let startIndex = html.indexOf(htmlStart);
if (startIndex !== -1) {
    let endIndex = html.indexOf(htmlEnd, startIndex);
    if (endIndex !== -1) {
        html = html.substring(0, startIndex) + html.substring(endIndex + htmlEnd.length);
        fs.writeFileSync(htmlPath, html);
        console.log('Removed from HTML');
    }
}

// 2. Remove from CSS
const cssPath = 'f:/BAO_SAPO/sapo_new/assets/style.css';
let css = fs.readFileSync(cssPath, 'utf8');

const cssStart = '/* ============================================\n   AI CORE SECTION\n   ============================================ */';
let cssStartIndex = css.indexOf(cssStart);
if (cssStartIndex !== -1) {
    css = css.substring(0, cssStartIndex).trimEnd();
    fs.writeFileSync(cssPath, css);
    console.log('Removed from CSS');
}

// 3. Remove from JS
const jsPath = 'f:/BAO_SAPO/sapo_new/assets/main.js';
let js = fs.readFileSync(jsPath, 'utf8');

const jsStart = '    // ============================================\n    // 13. AI CORE ORB INTERACTION\n    // ============================================';
let jsStartIndex = js.indexOf(jsStart);
if (jsStartIndex !== -1) {
    let jsEndIndex = js.indexOf('});', jsStartIndex);
    if (jsEndIndex !== -1) {
        // Keep the closing brace for DOMContentLoaded
        js = js.substring(0, jsStartIndex).trimEnd() + '\n\n});\n';
        fs.writeFileSync(jsPath, js);
        console.log('Removed from JS');
    }
}
