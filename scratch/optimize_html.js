const fs = require('fs');

const path = 'f:/BAO_SAPO/sapo_new/index.html';
let html = fs.readFileSync(path, 'utf8');

// 1. Phosphor icon script
html = html.replace('<script src="https://unpkg.com/@phosphor-icons/web"></script>', '<script src="https://unpkg.com/@phosphor-icons/web" defer></script>');

// 2. Head injection (fonts, preloads)
const preloads = `    <!-- Preload Critical Assets -->
    <link rel="preload" href="assets/style.css?v=20260423i" as="style">
    <link rel="preload" href="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png?1775454528082" as="image">
    <!-- Google Fonts Optimized -->
    <link href="https://fonts.googleapis.com/css2?family=Fira+Mono:wght@400;500&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
`;
// find where to inject, right before the custom css link
html = html.replace('    <!-- Custom CSS -->', preloads + '    <!-- Custom CSS -->');

// 3. Cache busting
html = html.replace('assets/style.css?v=20260423h', 'assets/style.css?v=20260423i');

// 4. Lazy load all images except hero and logo
html = html.replace(/<img\s([^>]+)>/gi, (match, p1) => {
    // Check if it's already lazy loaded
    if (p1.includes('loading="lazy"')) return match;
    
    // Check if it's hero or logo
    if (p1.includes('class="floating-pc"') || p1.includes('class="logo-img"')) {
        // Just add decoding async to hero images for performance
        if (!p1.includes('decoding=')) {
            return `<img ${p1} decoding="async">`;
        }
        return match;
    }
    
    // Add lazy load
    return `<img ${p1} loading="lazy" decoding="async">`;
});

fs.writeFileSync(path, html);
console.log('Performance optimization applied to HTML.');
