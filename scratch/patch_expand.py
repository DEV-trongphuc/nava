import re

def patch_expand():
    file_path = 'f:/BAO_SAPO/sapo_new/build_demos.py'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace the opening wrapper tag
    content = content.replace(
        '                    <div class="desc-column">\n                        <h2 style="font-size: 1.4rem; font-weight: 700; margin-bottom: 24px; color: #0f172a;">Đặc điểm nổi bật</h2>\n                        <div>',
        '                    <div class="desc-column">\n                        <h2 style="font-size: 1.4rem; font-weight: 700; margin-bottom: 24px; color: #0f172a;">Đặc điểm nổi bật</h2>\n                        <div class="desc-content-wrapper" id="desc-wrapper">'
    )

    # 2. Replace the closing wrapper tag with the overlay and show more button
    # The target closing block is:
    # </div>\n\n                        </div>\n                    </div>\n                    \n                    <!-- Right: Technical Specs -->
    # We should look at lines 2052-2057:
    # 2052: </div>
    # 2053: 
    # 2054:                         </div>
    # 2055:                     </div>
    # 2056:                     
    # 2057:                     <!-- Right: Technical Specs -->
    
    target_close = '</div>\n\n                        </div>\n                    </div>\n                    \n                    <!-- Right: Technical Specs -->'
    replacement_close = '</div>\n                            <div class="desc-overlay"></div>\n                        </div>\n                        <div style="text-align: center; margin-top: 20px;">\n                            <button class="btn-show-more" onclick="toggleDescription()" id="btn-show-desc">Xem thêm <i class="ph-bold ph-caret-down"></i></button>\n                        </div>\n                    </div>\n                    \n                    <!-- Right: Technical Specs -->'
    
    if target_close in content:
        content = content.replace(target_close, replacement_close)
        print("Replaced closing div with show more button.")
    else:
        # Try a regex approach
        content, count = re.subn(
            r'</div>\s*</div>\s*</div>\s*(?=\s*<!-- Right: Technical Specs -->)',
            '</div>\n                            <div class="desc-overlay"></div>\n                        </div>\n                        <div style="text-align: center; margin-top: 20px;">\n                            <button class="btn-show-more" onclick="toggleDescription()" id="btn-show-desc">Xem thêm <i class="ph-bold ph-caret-down"></i></button>\n                        </div>\n                    </div>',
            content,
            flags=re.DOTALL
        )
        print(f"Replaced closing div using regex (count: {count}).")

    # 3. Add toggleDescription function in script
    content = content.replace(
        '            <script>\n                // Image Gallery Logic',
        '            <script>\n                function toggleDescription() {\n                    const wrapper = document.getElementById(\'desc-wrapper\');\n                    const btn = document.getElementById(\'btn-show-desc\');\n                    if (wrapper.classList.contains(\'expanded\')) {\n                        wrapper.classList.remove(\'expanded\');\n                        btn.innerHTML = \'Xem thêm <i class=\"ph-bold ph-caret-down\"></i>\';\n                        wrapper.scrollIntoView({ behavior: \'smooth\' });\n                    } else {\n                        wrapper.classList.add(\'expanded\');\n                        btn.innerHTML = \'Thu gọn <i class=\"ph-bold ph-caret-up\"></i>\';\n                    }\n                }\n                // Image Gallery Logic'
    )
    print("Added toggleDescription JavaScript.")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    patch_expand()
