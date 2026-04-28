const fs = require('fs');

const additionalCSS = `
/* Shopee Desktop Grid */
@media (min-width: 769px) {
    .shopee-comments-list {
        display: grid !important;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
    }
    .shopee-comment-item {
        border-bottom: none !important;
        border: 1px solid var(--border-color, #e2e8f0);
        border-radius: 12px;
        padding: 20px;
        background: var(--bg-card, #ffffff);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        height: 100%;
    }
}

/* Policy 3D Hover & Slower Track */
.policy-card {
    transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease !important;
    transform-style: preserve-3d;
    perspective: 1000px;
}
.policy-card:hover {
    transform: translateY(-8px) rotateX(4deg) rotateY(-4deg) scale(1.03) !important;
    box-shadow: -5px 15px 30px rgba(0, 51, 102, 0.15) !important;
    z-index: 10;
}
.policy-track {
    animation-duration: 45s !important;
    will-change: transform;
}
`;

function fixHtml(filename) {
    let content = fs.readFileSync(filename, 'utf8');
    if (!content.includes('Shopee Desktop Grid')) {
        content = content.replace('</style>\n<!-- Shopee Reviews Mobile Slider CSS -->', additionalCSS + '</style>\n<!-- Shopee Reviews Mobile Slider CSS -->');
        content = content.replace('</style>\r\n<!-- Shopee Reviews Mobile Slider CSS -->', additionalCSS + '</style>\r\n<!-- Shopee Reviews Mobile Slider CSS -->');
        fs.writeFileSync(filename, content);
        console.log(filename + ' updated.');
    }
}

function fixJs() {
    let content = fs.readFileSync('update_index_bwt.js', 'utf8');
    if (!content.includes('Shopee Desktop Grid')) {
        content = content.replace(/<\/style>\\n<!-- Shopee Reviews Mobile Slider CSS -->/, additionalCSS.replace(/\n/g, '\\n') + '</style>\\n<!-- Shopee Reviews Mobile Slider CSS -->');
        fs.writeFileSync('update_index_bwt.js', content);
        console.log('update_index_bwt.js updated.');
    }
}

fixHtml('index.html');
fixJs();
