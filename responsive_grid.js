const fs = require('fs');
let css = fs.readFileSync('assets/style.css', 'utf8');

const newCss = `
/* --- CUSTOMER GRID --- */
.customer-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 30px;
}

@media (max-width: 768px) {
    .customer-grid {
        grid-template-columns: 1fr;
        gap: 20px;
    }
}
`;

if (!css.includes('.customer-grid {')) {
    css += newCss;
    fs.writeFileSync('assets/style.css', css);
    console.log('Appended customer-grid css');
} else {
    console.log('customer-grid already exists in css');
}
