const fs = require('fs');

const cssAppends = `
/* ============================================
   PERFORMANCE OPTIMIZATION
   ============================================ */
.footer,
.blog-section,
.video-section,
.brand-slider {
    content-visibility: auto;
    contain-intrinsic-size: auto 800px;
}
`;

fs.appendFileSync('f:/BAO_SAPO/sapo_new/assets/style.css', '\n' + cssAppends);
console.log('Appended CSS performance rules');
