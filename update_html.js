const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

// 1. Logo
html = html.replace('https://s120-ava-talk.zadn.vn/3/5/0/c/2/120/81f9e13ab9e5380232f102e36863b648.jpg', 'https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/logo.png?1775454528082');

// 2. Reduce 'overreact' words
html = html.replace(/Xử lý đỉnh cao/g, 'Xử lý mượt mà');
html = html.replace(/đồ họa đỉnh cao/g, 'đồ họa chuyên nghiệp');
html = html.replace(/Những công nghệ tối tân nhất/gi, 'Những công nghệ hiện đại');
html = html.replace(/sự ổn định cao nhất/gi, 'sự ổn định đáng tin cậy');
html = html.replace(/cực tốc độ/g, 'nhanh chóng');

// 3. Add 'Nhóm khách hàng' section before Product Grid
const customerSection = `
    <!-- Target Customer Groups Section -->
    <section class="target-customers-section" style="padding: 60px 0; background: var(--bg-gray);">
        <div class="container">
            <div class="section-header text-center mb-5" style="margin-bottom: 40px; text-align: center;">
                <h2 class="section-title">NHU CẦU CỦA BẠN LÀ GÌ?</h2>
                <p class="bento-subtitle" style="color: var(--text-gray);">Các giải pháp chuyên biệt từ NAVA STORE đáp ứng hoàn hảo hai nhóm nhu cầu lớn nhất</p>
            </div>
            <div class="customer-grid" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 30px;">
                <!-- Setup Văn Phòng -->
                <div class="customer-card reveal" style="background: var(--bg-white); border-radius: var(--radius-lg); padding: 40px; box-shadow: var(--shadow-md); border: 1px solid var(--border-color); text-align: center; transition: 0.3s; position: relative; overflow: hidden;">
                    <div class="card-glow" style="position: absolute; width: 200px; height: 200px; background: radial-gradient(circle, var(--primary) 0%, transparent 70%); opacity: 0.05; top: -50px; right: -50px; border-radius: 50%;"></div>
                    <div style="font-size: 3rem; color: var(--primary); margin-bottom: 20px;"><i class="ph-fill ph-monitor"></i></div>
                    <h3 style="font-size: 1.5rem; font-weight: 800; margin-bottom: 15px;">Set-up Văn Phòng Tối Giản</h3>
                    <p style="color: var(--text-gray); line-height: 1.6; margin-bottom: 20px;">Giải phóng không gian làm việc với Mini PC siêu nhỏ gọn nhưng đáp ứng tốt công việc. Tiết kiệm diện tích, giảm tiếng ồn và tạo cảm hứng làm việc mỗi ngày.</p>
                    <a href="https://navastore.vn/minipc" class="btn-pill btn-outline" style="display: inline-flex; border: 2px solid var(--primary); padding: 10px 24px; border-radius: 9999px; font-weight: 600; color: var(--primary); text-decoration: none; transition: 0.3s;">Xem giải pháp Văn phòng <i class="ph ph-arrow-right" style="margin-left: 8px;"></i></a>
                </div>

                <!-- Chạy Local AI -->
                <div class="customer-card reveal delay-1" style="background: var(--bg-white); border-radius: var(--radius-lg); padding: 40px; box-shadow: var(--shadow-md); border: 1px solid var(--border-color); text-align: center; transition: 0.3s; position: relative; overflow: hidden;">
                    <div class="card-glow" style="position: absolute; width: 200px; height: 200px; background: radial-gradient(circle, var(--primary) 0%, transparent 70%); opacity: 0.05; top: -50px; left: -50px; border-radius: 50%;"></div>
                    <div style="font-size: 3rem; color: var(--primary); margin-bottom: 20px;"><i class="ph-fill ph-cpu"></i></div>
                    <h3 style="font-size: 1.5rem; font-weight: 800; margin-bottom: 15px;">Chạy Local AI & Đồ Họa</h3>
                    <p style="color: var(--text-gray); line-height: 1.6; margin-bottom: 20px;">Sức mạnh từ NPU và eGPU hỗ trợ bạn huấn luyện mô hình ngôn ngữ lớn (LLM), render 3D, và xử lý dữ liệu ngay tại nhà hiệu quả.</p>
                    <a href="https://navastore.vn/egpu" class="btn-pill btn-blue" style="display: inline-flex; background: var(--primary); color: white; padding: 10px 24px; border-radius: 9999px; font-weight: 600; text-decoration: none; transition: 0.3s;">Xem giải pháp AI <i class="ph ph-arrow-right" style="margin-left: 8px;"></i></a>
                </div>
            </div>
        </div>
    </section>

    <!-- Product Grid Section (Siêu Phẩm Công Nghệ) -->`;

html = html.replace('<!-- Product Grid Section (Siêu Phẩm Công Nghệ) -->', customerSection);

// 4. Add Warranty Flipbook Section before Performance Benchmark
const warrantySection = `
    <!-- Warranty Flipbook Section -->
    <section class="warranty-section" style="padding: 60px 0; background: var(--bg-white);">
        <div class="container">
            <div class="warranty-card reveal" style="background: linear-gradient(135deg, var(--bg-gray) 0%, var(--bg-white) 100%); border-radius: var(--radius-lg); border: 1px solid var(--border-color); padding: 50px; box-shadow: var(--shadow-md); display: flex; align-items: center; justify-content: space-between; gap: 40px; flex-wrap: wrap;">
                <div class="warranty-content" style="flex: 1; min-width: 300px;">
                    <div style="display: inline-flex; align-items: center; gap: 8px; padding: 6px 12px; background: rgba(0, 51, 102, 0.1); color: var(--primary); border-radius: 9999px; font-weight: 600; font-size: 0.85rem; margin-bottom: 20px;">
                        <i class="ph-fill ph-shield-check"></i> Cam Kết Chất Lượng
                    </div>
                    <h2 class="section-title" style="margin-bottom: 20px; font-size: 2rem;">Chính Sách Bảo Hành & Hậu Mãi</h2>
                    <p style="color: var(--text-gray); font-size: 1.1rem; line-height: 1.6; margin-bottom: 30px;">An tâm sử dụng với chính sách bảo hành minh bạch và rõ ràng từ NAVA STORE. Trải nghiệm đọc chính sách dạng Flipbook trực quan và dễ hiểu.</p>
                    <a href="https://navastore.vn/chinh-sach-bao-hanh" target="_blank" class="btn-pill btn-blue btn-large" style="display: inline-flex; align-items: center; gap: 10px; background: var(--primary); color: white; padding: 14px 28px; border-radius: 9999px; font-weight: 600; font-size: 1.05rem; transition: 0.3s; box-shadow: var(--shadow-md);">
                        <i class="ph ph-book-open"></i> Xem chi tiết dạng Flipbook
                    </a>
                </div>
                <div class="warranty-image" style="flex: 1; min-width: 300px; text-align: center; position: relative;">
                    <div style="position: absolute; width: 100%; height: 100%; background: radial-gradient(circle, var(--primary) 0%, transparent 60%); opacity: 0.05; top: 0; left: 0;"></div>
                    <i class="ph-fill ph-shield-star" style="font-size: 10rem; color: var(--primary); filter: drop-shadow(0 10px 20px rgba(0, 51, 102, 0.2));"></i>
                </div>
            </div>
        </div>
    </section>

    <!-- ===== PERFORMANCE BENCHMARK SECTION ===== -->`;

html = html.replace('<!-- ===== PERFORMANCE BENCHMARK SECTION ===== -->', warrantySection);

fs.writeFileSync('index.html', html);
console.log('done updating index.html');
