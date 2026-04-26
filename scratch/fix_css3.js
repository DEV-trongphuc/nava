const fs = require('fs');

const styleFile = 'f:/BAO_SAPO/sapo_new/assets/style.css';
let css = fs.readFileSync(styleFile, 'utf8');

// 1. Center the FAB vertically
css = css.replace(/bottom: 110px;/, 'top: 50%;\n    transform: translateY(-50%);');

// 2. Round the cycle images
css = css.replace(/object-fit: contain;(\s*opacity: 0;)/, 'object-fit: cover;\n    border-radius: 50%;$1');

// 3. Widen the benefit cards container to align with text
css = css.replace(/max-width: 550px;\s*\/\*\s*Rộng bằng chữ SỨC MẠNH ĐIỆN TOÁN\s*\*\//, 'max-width: 615px; /* Rộng bằng chữ SỨC MẠNH ĐIỆN TOÁN */');

fs.writeFileSync(styleFile, css);
console.log('Fixed styles');
