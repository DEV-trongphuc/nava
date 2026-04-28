const fs = require('fs');

function fixFinal() {
    const filename = 'index.bwt';
    if (!fs.existsSync(filename)) return;
    let content = fs.readFileSync(filename, 'utf8');

    // 1. Fix benefit slider height and width cut-off
    const sliderCssRegex = /\.hero-benefits-slider\s*\{[^}]*\}/;
    // We already have some CSS for hero-benefits-slider injected in previous scripts
    // Let's replace it robustly.
    const newSliderCss = `.hero-benefits-slider {
    position: relative;
    overflow: hidden !important;
    padding: 20px !important;
    margin: -20px !important;
    height: 130px !important; /* 90px card + 40px padding */
    display: flex;
    align-items: center;
}`;
    
    // Replace existing injected slider CSS if present
    content = content.replace(/\.hero-benefits-slider\s*\{\s*position: relative;\s*overflow: hidden;\s*\}/g, newSliderCss);
    // If it wasn't replaced, maybe the previous script didn't inject exactly that. 
    // Let's just append the override to the style block.
    if (!content.includes('height: 130px !important;')) {
        content = content.replace('/* Benefit 3D Hover & Slower Track */', '/* Benefit 3D Hover & Slower Track */\n' + newSliderCss);
    }

    // 2. Fix social wrapper completely overriding style.css
    content = content.replace(
        /\.floating-social-wrapper \{\s*position: fixed !important;\s*bottom: 20px !important;\s*right: 20px !important;/g,
        '.floating-social-wrapper {\n            position: fixed !important;\n            bottom: 20px !important;\n            right: 20px !important;\n            top: auto !important;\n            transform: none !important;\n            flex-direction: column !important;'
    );

    // 3. Make benefit-pair top: 20px; left: 20px to account for the padding
    content = content.replace(
        /\.benefit-pair \{\s*position: absolute;\s*top: 0;\s*left: 0;/g,
        '.benefit-pair {\n    position: absolute;\n    top: 20px;\n    left: 20px;\n    width: calc(100% - 40px); /* subtract padding */'
    );

    fs.writeFileSync(filename, content);
    console.log(filename + ' updated.');
}

fixFinal();
