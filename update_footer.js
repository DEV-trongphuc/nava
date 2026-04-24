const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');
html = html.replace(/<a href=\"https:\/\/navastore\.vn\/chinh-sach-bao-hanh\">Chính sách bảo hành<\/a>/g, '<a href=\"#\" id=\"open-warranty-modal-footer\">Chính sách bảo hành</a>');
fs.writeFileSync('index.html', html);

let js = fs.readFileSync('assets/main.js', 'utf8');
js = js.replace(/const openWarrantyBtn = document\.getElementById\('open-warranty-modal'\);/g, "const openWarrantyBtn = document.getElementById('open-warranty-modal');\n    const openWarrantyBtnFooter = document.getElementById('open-warranty-modal-footer');");
js = js.replace(/if \(openWarrantyBtn && warrantyModal && closeWarrantyBtn\) \{/g, "if (warrantyModal && closeWarrantyBtn) {");
js = js.replace(/openWarrantyBtn\.addEventListener\('click', \(e\) => \{\n\s*e\.preventDefault\(\);\n\s*warrantyModal\.classList\.add\('active'\);\n\s*document\.body\.style\.overflow = 'hidden';\n\s*\}\);/g, "const openModal = (e) => {\n            e.preventDefault();\n            warrantyModal.classList.add('active');\n            document.body.style.overflow = 'hidden';\n        };\n        if (openWarrantyBtn) openWarrantyBtn.addEventListener('click', openModal);\n        if (openWarrantyBtnFooter) openWarrantyBtnFooter.addEventListener('click', openModal);");
fs.writeFileSync('assets/main.js', js);
console.log('done footer update');
