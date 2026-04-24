const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

// 1. Remove from header
html = html.replace(
    /<div class="modal-header">\s*<h2>Chính sách bảo hành tại Nava Store<\/h2>\s*<p class="modal-subtitle">Lưu ý: Shop không bảo hành dữ liệu cho khách hàng\.<\/p>\s*<\/div>/g,
    '<div class="modal-header">\n                <h2>Chính sách bảo hành tại Nava Store</h2>\n            </div>'
);

// 2. Add to the bottom of the note-block
const oldNoteBlock = `<div class="warranty-block note-block">
                    <h3><i class="ph-fill ph-info" style="color: #3b82f6;"></i> Lưu ý thêm:</h3>
                    <p>- Nếu sản phẩm chỉ còn tem của nhà sản xuất, quý khách vui lòng đến TTBH chính hãng để được hỗ trợ.</p>
                    <p>- <strong>Nava Store không bảo hành dữ liệu</strong> và không chịu trách nhiệm cho dữ liệu trên sản phẩm.</p>
                    <p>- Tra cứu bảo hành các hãng (ASUS, MSI, ASROCK, ZOTAC...) vui lòng liên hệ TTBH chính hãng tương ứng.</p>
                </div>`;

const newNoteBlock = `<div class="warranty-block note-block">
                    <h3><i class="ph-fill ph-info" style="color: #3b82f6;"></i> Lưu ý thêm:</h3>
                    <p>- Nếu sản phẩm chỉ còn tem của nhà sản xuất, quý khách vui lòng đến TTBH chính hãng để được hỗ trợ.</p>
                    <p>- Tra cứu bảo hành các hãng (ASUS, MSI, ASROCK, ZOTAC...) vui lòng liên hệ TTBH chính hãng tương ứng.</p>
                    <p class="modal-subtitle" style="margin-top: 15px; text-align: left; font-size: 1rem;"><i class="ph-fill ph-warning-circle"></i> Lưu ý: Shop không bảo hành dữ liệu cho khách hàng.</p>
                </div>`;

html = html.replace(oldNoteBlock, newNoteBlock);

fs.writeFileSync('index.html', html);
console.log('done moving text');
