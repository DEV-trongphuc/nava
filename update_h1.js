const fs = require('fs');
let script = fs.readFileSync('update_index_bwt.js', 'utf8');

// Inject visually hidden H1 right inside the master wrapper
script = script.replace(
    '<!-- PRELOADER -->',
    `<!-- SEO H1 -->
        <h1 style="position:absolute; width:1px; height:1px; padding:0; margin:-1px; overflow:hidden; clip:rect(0,0,0,0); border:0;">NAVA STORE - Chuyên Mini PC, eGPU, Linh kiện máy tính & Đồ họa AI</h1>
        <!-- PRELOADER -->`
);

fs.writeFileSync('update_index_bwt.js', script);
console.log('Updated update_index_bwt.js with SEO H1');
