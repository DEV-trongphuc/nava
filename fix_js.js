const fs = require('fs');
let js = fs.readFileSync('assets/main.js', 'utf8');

const modalJS = `
    // 12. WARRANTY MODAL
    const openWarrantyBtn = document.getElementById('open-warranty-modal');
    const openWarrantyBtnFooter = document.getElementById('open-warranty-modal-footer');
    const warrantyModal = document.getElementById('warranty-modal');
    const closeWarrantyBtn = document.getElementById('close-warranty-modal');

    if (warrantyModal && closeWarrantyBtn) {
        const openModal = (e) => {
            e.preventDefault();
            warrantyModal.classList.add('active');
            document.body.style.overflow = 'hidden';
        };

        if (openWarrantyBtn) openWarrantyBtn.addEventListener('click', openModal);
        if (openWarrantyBtnFooter) openWarrantyBtnFooter.addEventListener('click', openModal);

        closeWarrantyBtn.addEventListener('click', () => {
            warrantyModal.classList.remove('active');
            document.body.style.overflow = '';
        });

        warrantyModal.addEventListener('click', (e) => {
            if (e.target === warrantyModal) {
                warrantyModal.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    }
`;

if (!js.includes('WARRANTY MODAL')) {
    const lastBraceIndex = js.lastIndexOf('});');
    if (lastBraceIndex !== -1) {
        js = js.slice(0, lastBraceIndex) + modalJS + '\n' + js.slice(lastBraceIndex);
        fs.writeFileSync('assets/main.js', js);
        console.log('Appended to main.js');
    } else {
        console.log('Could not find last });');
    }
} else {
    console.log('Already exists');
}
