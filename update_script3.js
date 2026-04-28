const fs = require('fs');
let script = fs.readFileSync('update_index_bwt.js', 'utf8');
const sliderInject = `
// Inject Shopee Mobile Slider CSS
bodyContent = bodyContent.replace(
    /<!-- Shopee Reviews Section -->/i,
    \`<!-- Shopee Reviews Mobile Slider CSS -->
<style>
@media (max-width: 768px) {
    .shopee-comments-list {
        flex-direction: row;
        overflow-x: auto;
        scroll-snap-type: x mandatory;
        padding-bottom: 20px;
        gap: 15px;
        scrollbar-width: none;
    }
    .shopee-comments-list::-webkit-scrollbar {
        display: none;
    }
    .shopee-comment-item {
        flex: 0 0 85%;
        scroll-snap-align: center;
        border-bottom: none;
        border: 1px solid var(--border-color, #e2e8f0);
        border-radius: 12px;
        padding: 20px;
        background: var(--bg-card, #ffffff);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
}
</style>
<!-- Shopee Reviews Section -->\`
);

`;
script = script.replace('fs.writeFileSync', sliderInject + 'fs.writeFileSync');
fs.writeFileSync('update_index_bwt.js', script);
console.log('Updated update_index_bwt.js');
