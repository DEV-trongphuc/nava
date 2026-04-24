const fs = require('fs');

// --- 1. Modify index.html ---
let html = fs.readFileSync('index.html', 'utf8');

// Replace the flipbook button
html = html.replace(
    /<a href="https:\/\/navastore\.vn\/chinh-sach-bao-hanh" target="_blank" class="btn-pill btn-blue btn-large"([^>]*)>([\s\S]*?)<i class="ph ph-book-open"><\/i> Xem chi tiết dạng Flipbook\s*<\/a>/g,
    '<button id="open-warranty-modal" class="btn-pill btn-blue btn-large"$1>$2<i class="ph ph-article"></i> Xem chi tiết chính sách</button>'
);

// Check if modal already exists
if (!html.includes('id="warranty-modal"')) {
    const modalHTML = `
    <!-- Warranty Modal -->
    <div id="warranty-modal" class="modal-overlay">
        <div class="modal-content warranty-modal-content">
            <button class="modal-close" id="close-warranty-modal"><i class="ph ph-x"></i></button>
            <div class="modal-header">
                <h2>Chính sách bảo hành tại Nava Store</h2>
                <p class="modal-subtitle">Lưu ý: Shop không bảo hành dữ liệu cho khách hàng.</p>
            </div>
            <div class="modal-body-scroll">
                <div class="warranty-block">
                    <h3><i class="ph-fill ph-check-circle" style="color: #10b981;"></i> Áp Dụng Cho Các Sản Phẩm:</h3>
                    <ul>
                        <li><strong>Đối với MiniPC:</strong>
                            <ul>
                                <li>Minis Forum: Bảo hành 2 năm từ nhà sản xuất, miễn phí gửi bảo hành 1 năm đầu.</li>
                                <li>Bee Link, Aoostar, GMKtec, Morefine, FEVM: Bảo hành 12 tháng, miễn phí gửi bảo hành 6 tháng đầu.</li>
                                <li>Firebat, Trycoo,... : Bảo hành 6 tháng từ nhà sản xuất.</li>
                            </ul>
                        </li>
                        <li><strong>Đối với RAM Samsung/Hynix:</strong> Bảo hành 3 năm từ nhà sản xuất.</li>
                        <li><strong>Đối với SSD:</strong>
                            <ul>
                                <li>Samsung/Lexar/Predator: Bảo hành 3 năm từ nhà sản xuất.</li>
                                <li>Hynix: Bảo hành 1 năm từ nhà sản xuất.</li>
                            </ul>
                        </li>
                    </ul>
                </div>

                <div class="warranty-block">
                    <h3><i class="ph-fill ph-shield-check" style="color: var(--primary);"></i> Điều Kiện Bảo Hành:</h3>
                    <ul>
                        <li>Sản phẩm được bán ra bởi Nava Store và có tem bảo hành của Nava Store hoặc tem bảo hành từ nhà cung cấp/sản xuất (còn nguyên vẹn).</li>
                        <li>Sản phẩm trong thời hạn bảo hành hợp lệ, đầy đủ phụ kiện và bao bì theo yêu cầu.</li>
                        <li>Sản phẩm lỗi do kỹ thuật hoặc từ nhà sản xuất, được xác định bởi Nava Store hoặc nhà phân phối.</li>
                    </ul>
                </div>

                <div class="warranty-block">
                    <h3><i class="ph-fill ph-warning-circle" style="color: #ef4444;"></i> Không Đủ Điều Kiện Bảo Hành:</h3>
                    <ul>
                        <li>Sản phẩm hết hạn hoặc không đáp ứng điều kiện bảo hành.</li>
                        <li>Sản phẩm mất tem, mờ tem, cạo sửa, chắp vá.</li>
                        <li>Hư hại do va đập, cấn móp, cháy nổ, dính chất lỏng, hoặc lỗi do người dùng.</li>
                        <li>Sản phẩm có dấu hiệu tự ý tháo mở, sửa chữa.</li>
                    </ul>
                </div>

                <div class="warranty-block note-block">
                    <h3><i class="ph-fill ph-info" style="color: #3b82f6;"></i> Lưu ý thêm:</h3>
                    <p>- Nếu sản phẩm chỉ còn tem của nhà sản xuất, quý khách vui lòng đến TTBH chính hãng để được hỗ trợ.</p>
                    <p>- <strong>Nava Store không bảo hành dữ liệu</strong> và không chịu trách nhiệm cho dữ liệu trên sản phẩm.</p>
                    <p>- Tra cứu bảo hành các hãng (ASUS, MSI, ASROCK, ZOTAC...) vui lòng liên hệ TTBH chính hãng tương ứng.</p>
                </div>

                <div class="warranty-contact">
                    <h3>Liên hệ bảo hành:</h3>
                    <div class="contact-grid">
                        <a href="https://facebook.com/navastore" target="_blank" class="contact-item fb"><i class="ph-fill ph-facebook-logo"></i> Fanpage Nava Store</a>
                        <a href="https://zalo.me/0972178527" target="_blank" class="contact-item zalo"><i class="ph-fill ph-chat-circle-dots"></i> Zalo OA: Nava Store</a>
                        <div class="contact-item phone"><i class="ph-fill ph-phone"></i> Hotline: 0972178527</div>
                        <div class="contact-item address" style="grid-column: 1 / -1;"><i class="ph-fill ph-map-pin"></i> 160/15 Linh Trung, TP. Thủ Đức, TP. Hồ Chí Minh.</div>
                        <div class="contact-item time" style="grid-column: 1 / -1;"><i class="ph-fill ph-clock"></i> Tiếp nhận: Thứ 2 – Thứ 7 (9:00 AM – 5:00 PM).</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Floating Contact Buttons -->`;
    html = html.replace('<!-- Floating Contact Buttons -->', modalHTML);
}
fs.writeFileSync('index.html', html);

// --- 2. Modify style.css ---
let css = fs.readFileSync('assets/style.css', 'utf8');
if (!css.includes('.warranty-modal-content')) {
    const modalCSS = `
/* --- WARRANTY MODAL --- */
.modal-overlay {
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(5px);
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
}

.modal-overlay.active {
    opacity: 1;
    visibility: visible;
}

.warranty-modal-content {
    background: var(--bg-white);
    width: 90%;
    max-width: 800px;
    max-height: 90vh;
    border-radius: var(--radius-lg);
    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    display: flex;
    flex-direction: column;
    position: relative;
    transform: translateY(20px);
    transition: all 0.3s ease;
    border: 1px solid var(--border-color);
}

.modal-overlay.active .warranty-modal-content {
    transform: translateY(0);
}

.modal-close {
    position: absolute;
    top: 20px;
    right: 20px;
    background: var(--bg-gray);
    border: 1px solid var(--border-color);
    width: 40px; height: 40px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem;
    color: var(--text-dark);
    cursor: pointer;
    z-index: 10;
    transition: 0.3s;
}

.modal-close:hover {
    background: #ef4444;
    color: white;
    border-color: #ef4444;
}

.modal-header {
    padding: 30px;
    border-bottom: 1px solid var(--border-color);
    text-align: center;
}

.modal-header h2 {
    font-size: 1.8rem;
    font-weight: 800;
    color: var(--text-dark);
    margin-bottom: 10px;
}

.modal-subtitle {
    color: #ef4444;
    font-weight: 600;
    font-size: 0.95rem;
}

.modal-body-scroll {
    padding: 30px;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: var(--border-color) transparent;
}

.modal-body-scroll::-webkit-scrollbar {
    width: 6px;
}
.modal-body-scroll::-webkit-scrollbar-thumb {
    background-color: var(--border-color);
    border-radius: 10px;
}

.warranty-block {
    margin-bottom: 30px;
}

.warranty-block h3 {
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--text-dark);
    margin-bottom: 15px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.warranty-block ul {
    list-style: none;
    padding-left: 20px;
}

.warranty-block ul li {
    position: relative;
    color: var(--text-gray);
    margin-bottom: 10px;
    line-height: 1.6;
}

.warranty-block ul > li::before {
    content: "•";
    position: absolute;
    left: -15px;
    color: var(--primary);
    font-weight: bold;
}

.warranty-block ul ul {
    margin-top: 10px;
    margin-bottom: 10px;
    padding-left: 15px;
}

.warranty-block ul ul li::before {
    content: "-";
    color: var(--text-gray);
}

.note-block {
    background: rgba(59, 130, 246, 0.05);
    border: 1px dashed rgba(59, 130, 246, 0.3);
    padding: 20px;
    border-radius: var(--radius-md);
}

.note-block p {
    color: var(--text-gray);
    margin-bottom: 8px;
    line-height: 1.5;
    font-size: 0.95rem;
}
.note-block p:last-child { margin-bottom: 0; }

.warranty-contact h3 {
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--text-dark);
    margin-bottom: 15px;
}

.contact-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
}

.contact-item {
    display: flex; align-items: center; gap: 10px;
    padding: 12px 15px;
    background: var(--bg-gray);
    border-radius: var(--radius-sm);
    border: 1px solid var(--border-color);
    color: var(--text-dark);
    font-weight: 600;
    font-size: 0.9rem;
    text-decoration: none;
    transition: 0.3s;
}

.contact-item.fb { color: #1877f2; }
.contact-item.zalo { color: #0068ff; }
.contact-item.phone { color: #10b981; }

.contact-item[href]:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-sm);
    border-color: currentColor;
}

@media (max-width: 768px) {
    .modal-header h2 { font-size: 1.5rem; }
    .contact-grid { grid-template-columns: 1fr; }
    .modal-body-scroll { padding: 20px; }
    .modal-header { padding: 20px; }
}
`;
    css += '\n' + modalCSS;
    fs.writeFileSync('assets/style.css', css);
}

// --- 3. Modify main.js ---
let js = fs.readFileSync('assets/main.js', 'utf8');
if (!js.includes('warranty-modal')) {
    const modalJS = `
    // 12. WARRANTY MODAL
    const openWarrantyBtn = document.getElementById('open-warranty-modal');
    const warrantyModal = document.getElementById('warranty-modal');
    const closeWarrantyBtn = document.getElementById('close-warranty-modal');

    if (openWarrantyBtn && warrantyModal && closeWarrantyBtn) {
        openWarrantyBtn.addEventListener('click', (e) => {
            e.preventDefault();
            warrantyModal.classList.add('active');
            document.body.style.overflow = 'hidden';
        });

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
    // Append to DOMContentLoaded
    js = js.replace(/}\); \/\/ End of DOMContentLoaded/g, modalJS + '\n}); // End of DOMContentLoaded');
    fs.writeFileSync('assets/main.js', js);
}

console.log('done updating modal');
