const fs = require('fs');
let script = fs.readFileSync('update_index_bwt.js', 'utf8');

// The Shopee Reviews Mobile Slider CSS is already there. Let's find it and inject our Cart Mobile CSS inside the same @media block or next to it.
script = script.replace(
    '<!-- Shopee Reviews Mobile Slider CSS -->',
    `<!-- Mobile CSS Fixes (Cart + Shopee) -->
<style>
@media (max-width: 768px) {
    /* Fix hidden cart icon on mobile */
    .top-actions .cart-btn .cart-icon-wrapper {
        display: block !important;
    }
    .top-actions .cart-btn {
        font-size: 0 !important; /* Hide 'Giỏ hàng' text */
        padding: 6px 10px;
    }
    .top-actions .cart-btn i {
        font-size: 1.6rem !important;
    }
    .cart-count-badge {
        font-size: 10px !important;
    }
}
</style>
<!-- Shopee Reviews Mobile Slider CSS -->`
);

fs.writeFileSync('update_index_bwt.js', script);
console.log('Updated update_index_bwt.js with Mobile Cart CSS fix');
