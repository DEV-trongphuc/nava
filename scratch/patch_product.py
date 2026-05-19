import re

def patch_product():
    file_path = 'f:/BAO_SAPO/sapo_new/build_demos.py'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    with open('f:/BAO_SAPO/sapo_new/scratch/product_desc.html', 'r', encoding='utf-8') as f:
        desc_html = f.read()

    # We will find:
    #                     <!-- Left: Description -->
    #                     <div class="desc-column">
    #                         ...
    #                     </div>
    #
    # And replace the inner content of <div class="desc-column"> with the desc_html.
    # To do this safely, we can target the exact lines:
    
    target_desc = r'''                    <!-- Left: Description -->
                    <div class="desc-column">
                        <h2 style="font-size: 1.4rem; font-weight: 700; margin-bottom: 24px; color: #0f172a;">Đặc điểm nổi bật</h2>
                        
                        <h3 style="font-weight: 700; margin-bottom: 12px; font-size: 1.1rem; color: #0f172a;">Đỉnh Cao Hiệu Suất Trong Thiết Kế Nhỏ Gọn</h3>
                        <p style="margin-bottom: 24px; color: #475569; line-height: 1.7; font-size: 0.95rem;">ASUS NUC AI 350 (PN54) là mẫu Mini PC tiên phong được trang bị bộ vi xử lý AMD Ryzen™ AI 300 Series, mang đến hiệu suất vượt trội và khả năng xử lý trí tuệ nhân tạo (AI) tiên tiến. Với thiết kế siêu nhỏ gọn, độ bền đạt chuẩn quân đội MIL-STD-810H, và tích hợp công nghệ Copilot+ PC.</p>
                        
                        <img src="//bizweb.dktcdn.net/thumb/large/100/543/817/products/mini-pc-asus-nuc-ai-350-pn54-ryzen-ai-7-350-gaming.jpg?v=1763971973973" style="width: 100%; border-radius: 12px; margin-bottom: 24px; border: 1px solid #e2e8f0;" alt="ASUS NUC">
                        
                        <h3 style="font-weight: 700; margin-bottom: 12px; font-size: 1.1rem; color: #0f172a;">Hiệu Suất Vượt Trội Với AMD Ryzen™ AI 300</h3>
                        <p style="margin-bottom: 16px; color: #475569; line-height: 1.7; font-size: 0.95rem;">Trang bị bộ vi xử lý tối đa 12 lõi siêu nhanh và kiến trúc tiên tiến:</p>
                        <ul style="padding-left: 20px; color: #475569; line-height: 1.7; font-size: 0.95rem;">
                            <li style="margin-bottom: 8px;"><strong style="color: #0f172a;">Đồ họa mạnh mẽ:</strong> AMD Radeon™ 890M dựa trên kiến trúc RDNA™ 3.5.</li>
                            <li style="margin-bottom: 8px;"><strong style="color: #0f172a;">Băng thông AI tối đa:</strong> Kiến trúc XDNA 2 cung cấp NPU lên đến 50 TOPS.</li>
                            <li style="margin-bottom: 8px;"><strong style="color: #0f172a;">Chuẩn bị cho tương lai:</strong> Đáp ứng yêu cầu khắt khe của Copilot+ PC.</li>
                        </ul>
                    </div>'''
    
    replacement_desc = f'''                    <!-- Left: Description -->
                    <div class="desc-column">
                        <h2 style="font-size: 1.4rem; font-weight: 700; margin-bottom: 24px; color: #0f172a;">Đặc điểm nổi bật</h2>
                        <div>
                            {desc_html}
                        </div>
                    </div>'''

    if target_desc in content:
        content = content.replace(target_desc, replacement_desc)
        print("Replaced description mockup.")
    else:
        # Fallback regex if spacing is slightly different
        content, count = re.subn(
            r'<!-- Left: Description -->\s*<div class="desc-column">.*?</div>\s*(?=\s*<!-- Right: Technical Specs -->)',
            replacement_desc.replace('\\', '\\\\'),
            content,
            flags=re.DOTALL
        )
        print(f"Replaced description mockup using regex (count: {count}).")

    # Now remove the Datasheet button inside specs-column
    target_btn = r'''                        <button class="action-btn" style="width: 100%; margin-top: 30px; border: 1px solid #cbd5e1; background: #fff; color: var(--primary); font-weight: 700; height: 48px; border-radius: 12px; display: flex; justify-content: center; align-items: center; gap: 8px; cursor: pointer; transition: all 0.2s;" onmouseover="this.style.borderColor='var(--primary)'; this.style.boxShadow='0 4px 10px rgba(14,165,233,0.1)';" onmouseout="this.style.borderColor='#cbd5e1'; this.style.boxShadow='none';">
                            <i class="ph-bold ph-download-simple"></i> Tải Datasheet (PDF)
                        </button>'''

    if target_btn in content:
        content = content.replace(target_btn, '')
        print("Removed datasheet button.")
    else:
        content, count = re.subn(
            r'<button class="action-btn"[^>]*?>\s*<i class="ph-bold ph-download-simple"></i> Tải Datasheet \(PDF\)\s*</button>',
            '',
            content,
            flags=re.DOTALL
        )
        print(f"Removed datasheet button using regex (count: {count}).")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    patch_product()
