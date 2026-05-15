import os
import re

def clean_liquid_tags(text):
    text = re.sub(r'{%\s*comment\s*%}.*?{%\s*endcomment\s*%}', '', text, flags=re.DOTALL)
    
    # Convert asset_url and img_url liquid tags to static URLs
    def replace_asset(match):
        filename = match.group(1)
        full_tag = match.group(0)
        url = f"https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/{filename}"
        if 'stylesheet_tag' in full_tag:
            return f'<link href="{url}" rel="stylesheet" type="text/css" />'
        elif 'script_tag' in full_tag:
            return f'<script src="{url}"></script>'
        else:
            return url
    
    text = re.sub(r"{{\s*'([^']+)'\s*\|\s*(?:bizweb_)?asset_url[^}]*}}", replace_asset, text)
    text = re.sub(r'{{\s*"([^"]+)"\s*\|\s*(?:bizweb_)?asset_url[^}]*}}', replace_asset, text)
    
    # Delete the logged-in link block safely
    text = re.sub(r'<a href="/account" class="action-item">\s*<i class="ph ph-user-check" style="color: var\(--primary\);"></i>\s*<div><small>Xin chào,</small><br><strong>.*?</strong></div>\s*</a>\s*{%\s*else\s*%}', '', text, flags=re.DOTALL)
    
    # Remove remaining loose liquid logic tags explicitly
    text = re.sub(r"{%-?\s*(if|else|elsif|endif|for|endfor|unless|endunless|include|schema|endschema|javascript|endjavascript|stylesheet|endstylesheet|break|continue|case|when|assign|capture|endcapture)[^}]*%}", "", text)
    
    # Strip fallback text from tags if possible, e.g. {{ blog.name | default: 'Tin Tức' }}
    text = re.sub(r"{{[^|}]*\|\s*default:\s*'([^']+)'[^}]*}}", r"\1", text)
    text = re.sub(r'{{[^|}]*\|\s*default:\s*"([^"]+)"[^}]*}}', r"\1", text)
    
    # Remove all remaining {{ ... }} tags
    text = re.sub(r"{{-?\s*[^}]+\s*}}", "", text)

    return text

def get_core_layout(base_dir):
    with open(os.path.join(base_dir, "theme.bwt"), "r", encoding="utf-8") as f:
        theme = f.read()
        
    with open(os.path.join(base_dir, "extracted_footer.html"), "r", encoding="utf-8") as f:
        footer_content = f.read()
        
    with open(os.path.join(base_dir, "extracted_header.html"), "r", encoding="utf-8") as f:
        header_content = f.read()

    parts = theme.split("{{ content_for_layout }}")
    header_part = parts[0]
    footer_part = parts[1] if len(parts) > 1 else "</body></html>"

    # Inject Header
    header_part = header_part.replace("{%- include 'header' -%}", header_content)
    # Inject Footer
    footer_part = footer_part.replace("{%- include 'footer' -%}", footer_content)
    
    return header_part, footer_part

def build_index(base_dir, header_part, footer_part):
    with open(os.path.join(base_dir, "index.bwt"), "r", encoding="utf-8") as f:
        index_content = f.read()
        
    full_index = header_part.replace(open(os.path.join(base_dir, "extracted_header.html"), "r", encoding="utf-8").read(), "") + index_content + footer_part
    full_index = clean_liquid_tags(full_index)
    
    with open(os.path.join(base_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(full_index)

def build_collection(base_dir, header_part, footer_part):
    # Extract sticky stuff from index.bwt
    sticky_stuff = ""
    with open(os.path.join(base_dir, "index.bwt"), "r", encoding="utf-8") as f:
        idx_content = f.read()
        if "<!-- Mobile Sidebar Drawer -->" in idx_content:
            sticky_stuff = idx_content[idx_content.find("<!-- Mobile Sidebar Drawer -->"):]
            if "<!-- /MASTER SAPO ESCAPE WRAPPER -->" in sticky_stuff:
                sticky_stuff = sticky_stuff.split("<!-- /MASTER SAPO ESCAPE WRAPPER -->")[0]
                
    local_footer_part = sticky_stuff + '<script src="https://nava-one.vercel.app/assets/main.js" defer></script>\n' + footer_part

    collection_html = """
        <div class="container" style="max-width: 1600px !important; width: 100% !important; box-sizing: border-box !important; margin: 50px auto 0 !important; padding: 30px 30px 80px;">
            <div class="breadcrumb" style="background: transparent; padding: 0; margin-bottom: 25px; font-size: 0.95rem;">
                <a href="/" style="color: var(--text-gray); text-decoration: none; display: inline-flex; align-items: center; gap: 5px;"><i class="ph ph-house"></i> Trang chủ</a> 
                <span style="margin: 0 10px; color: var(--text-gray);">/</span> 
                <span style="color: var(--primary); font-weight: bold;">ASUS NUC</span>
            </div>

            <!-- Techy Hero Banner -->
            <div class="collection-hero" style="background: linear-gradient(135deg, rgba(14,165,233,0.1) 0%, rgba(15,23,42,0.02) 100%); border-radius: var(--radius-lg); padding: 40px 50px; margin-bottom: 40px; border: 1px solid var(--border-color); position: relative; overflow: hidden; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 10px 30px rgba(0,0,0,0.02);">
                <div class="card-glow" style="position: absolute; width: 500px; height: 500px; background: radial-gradient(circle, var(--primary) 0%, transparent 70%); opacity: 0.08; top: -150px; right: -100px; border-radius: 50%;"></div>
                <div style="position: relative; z-index: 2;">
                    <span style="display: inline-flex; align-items: center; gap: 6px; background: var(--primary); color: white; padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: bold; margin-bottom: 15px; box-shadow: 0 4px 10px rgba(14, 165, 233, 0.3);">
                        🏆 ASUS Gold Partner
                    </span>
                    <h1 style="font-size: 2.5rem; font-weight: 900; margin-bottom: 12px; color: var(--text-color); letter-spacing: -0.5px;">Mini PC ASUS NUC Chính Hãng</h1>
                    <p style="color: var(--text-gray); max-width: 650px; font-size: 1.05rem; margin: 0; line-height: 1.6;">Là đối tác Gold Partner của ASUS, NAVA Store tự hào cung cấp các dòng sản phẩm ASUS NUC với chất lượng dịch vụ bảo hành cao cấp nhất.</p>
                </div>
                <div style="padding-right: 40px; position: relative; z-index: 2; opacity: 0.9;">
                    <img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/asus.png" alt="ASUS" style="max-width: 250px; max-height: 80px; object-fit: contain; filter: drop-shadow(0 10px 20px rgba(14,165,233,0.2));">
                </div>
            </div>

            <style>
                /* Layout */
                .nava-collection-layout { display: flex; flex-direction: column; gap: 40px; }
                .nava-sidebar { width: 100%; }
                .nava-main { width: 100%; min-width: 0; }
                
                .sidebar-block { margin-bottom: 35px; }
                .sidebar-title { font-weight: 800; font-size: 1.1rem; text-transform: uppercase; margin-bottom: 20px; color: var(--text-color); display: flex; align-items: center; gap: 10px; }
                .sidebar-title::before { content: ''; display: block; width: 4px; height: 18px; background: var(--primary); border-radius: 2px; }
                
                .category-list { list-style: none; padding: 0; margin: 0; }
                .category-list li { margin-bottom: 10px; }
                .category-list a { display: flex; align-items: center; gap: 10px; color: var(--text-color); text-decoration: none; font-weight: 600; font-size: 0.95rem; transition: all 0.3s; padding: 8px 12px; border-radius: var(--radius-sm); }
                .category-list a:hover, .category-list a.active { color: var(--primary); background: rgba(14, 165, 233, 0.05); padding-left: 15px; }
                .category-list a img { flex-shrink: 0; }
                .category-list .count { margin-left: auto; background: var(--bg-gray); padding: 2px 8px; border-radius: 10px; font-size: 0.8rem; color: var(--text-gray); display: flex; align-items: center; gap: 4px; }
                
                .price-filter-inputs { display: flex; gap: 10px; margin-bottom: 15px; }
                .price-filter-inputs input { width: 50%; padding: 12px; border-radius: var(--radius-sm); border: 1px solid var(--border-color); background: transparent; color: var(--text-color); font-size: 0.9rem; transition: border-color 0.3s; }
                .price-filter-inputs input:focus { border-color: var(--primary); outline: none; }
                
                .brand-list { display: flex; flex-wrap: wrap; gap: 8px; width: 100%; box-sizing: border-box; }
                .brand-item { width: calc(50% - 4px); display: flex; align-items: center; justify-content: center; padding: 6px; border: 1px solid var(--border-color); border-radius: var(--radius-sm); cursor: pointer; transition: all 0.3s; background: transparent; height: 48px; box-sizing: border-box; }
                .brand-item img { max-height: 20px; max-width: 85%; width: auto; object-fit: contain; filter: grayscale(100%) brightness(1.5); opacity: 0.7; transition: all 0.3s; }
                .brand-item:hover { border-color: var(--primary); background: rgba(14, 165, 233, 0.05); }
                .brand-item:hover img { filter: grayscale(0%) brightness(1); opacity: 1; }
                
                .sort-bar { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; margin-bottom: 30px; background: var(--bg-white); padding: 15px 20px; border-radius: var(--radius-lg); border: 1px solid var(--border-color); box-shadow: var(--shadow-sm); }
                .sort-label { font-weight: 700; margin-right: 10px; color: var(--text-color); }
                .sort-btn { padding: 8px 18px; border-radius: 20px; border: 1px solid transparent; background: var(--bg-gray); color: var(--text-gray); font-size: 0.9rem; font-weight: 600; cursor: pointer; transition: all 0.3s; }
                .sort-btn:hover { background: rgba(14, 165, 233, 0.1); color: var(--primary); }
                .sort-btn.active { background: var(--primary); color: white; box-shadow: 0 4px 10px rgba(14, 165, 233, 0.3); }
                
                .card-specs { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 15px; }
                .spec-pill { background: linear-gradient(135deg, #1e3a8a, #3b82f6); color: white; padding: 4px 8px; border-radius: 6px; font-size: 0.7rem; font-weight: 800; display: inline-block; white-space: nowrap; box-shadow: 0 2px 4px rgba(30, 58, 138, 0.2); }
                .spec-pill.secondary { background: var(--bg-gray); color: var(--text-gray); border: 1px solid var(--border-color); box-shadow: none; font-weight: 600; }
                
                .product-card { transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease; border: 1px solid var(--border-color); border-radius: var(--radius-lg); overflow: hidden; background: var(--bg-white); }
                .product-card:hover { transform: translateY(-5px); box-shadow: 0 20px 40px rgba(0,0,0,0.08); border-color: var(--primary); }
                
                /* Advanced UX/UI Features */
                @keyframes skeleton-loading { 0% { background-position: 100% 50%; } 100% { background-position: 0 50%; } }
                .grid-loading { position: relative; pointer-events: none; }
                .grid-loading::after { content: ''; position: absolute; inset: 0; background: rgba(255,255,255,0.5); z-index: 10; backdrop-filter: blur(1px); }
                .grid-loading .product-card { position: relative; overflow: hidden; border-color: var(--border-color); }
                .grid-loading .product-card::before { content: ''; position: absolute; inset: 0; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.8), transparent); background-size: 200% 100%; animation: skeleton-loading 1.2s infinite; z-index: 11; pointer-events: none; }
                
                #toast-container { position: fixed; top: 20px; right: 20px; z-index: 9999; display: flex; flex-direction: column; gap: 10px; pointer-events: none; }
                .nava-toast { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border: 1px solid var(--border-color); border-left: 4px solid var(--primary); padding: 15px 20px; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); color: var(--text-color); font-weight: 600; font-size: 0.95rem; display: flex; align-items: center; gap: 12px; transform: translateX(120%); opacity: 0; transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55); }
                .nava-toast.show { transform: translateX(0); opacity: 1; }
                
                .quick-view-btn { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -30%); opacity: 0; visibility: hidden; background: rgba(255, 255, 255, 0.4); backdrop-filter: blur(4px); border: 1px solid rgba(255,255,255,0.6); color: var(--text-color); width: 45px; height: 45px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.3s; z-index: 10; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
                .product-card:hover .quick-view-btn { opacity: 1; visibility: visible; transform: translate(-50%, -50%); }
                .quick-view-btn:hover { background: rgba(255, 255, 255, 0.8); }
                
                .product-img { transition: opacity 0.4s; }
                .product-img-hover { position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: contain; opacity: 0; transition: opacity 0.4s; z-index: 1; }
                .product-card:hover .product-img { opacity: 0; }
                .product-card:hover .product-img-hover { opacity: 1; }
                
                .mobile-filter-btn { display: none; position: fixed; bottom: 85px; left: 50%; transform: translateX(-50%); background: var(--primary); color: white; border: none; padding: 12px 24px; border-radius: 30px; font-weight: bold; z-index: 90; box-shadow: 0 5px 20px rgba(14,165,233,0.4); align-items: center; gap: 8px; cursor: pointer; transition: transform 0.2s; }
                .mobile-filter-btn:active { transform: translateX(-50%) scale(0.95); }
                
                @media (min-width: 992px) {
                    .nava-collection-layout { flex-direction: row; align-items: flex-start; }
                    .nava-sidebar { width: 260px; flex-shrink: 0; position: sticky; top: 120px; }
                    .nava-main { flex: 1; min-width: 0; }
                    .product-grid { grid-template-columns: repeat(4, 1fr) !important; gap: 20px !important; }
                }
                @media (max-width: 1199px) and (min-width: 992px) {
                    .product-grid { grid-template-columns: repeat(3, 1fr) !important; }
                }
                @media (max-width: 991px) {
                    .nava-sidebar { position: fixed; top: 0; left: -100%; width: 85%; max-width: 320px; height: 100vh; background: var(--bg-white); z-index: 1000; transition: 0.3s ease; overflow-y: auto; box-shadow: 20px 0 50px rgba(0,0,0,0.1); padding: 20px 0; }
                    .nava-sidebar.active { left: 0; }
                    .sidebar-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 999; display: none; backdrop-filter: blur(3px); }
                    .sidebar-overlay.active { display: block; }
                    .mobile-filter-btn { display: flex; }
                    .brand-list { flex-wrap: nowrap; overflow-x: auto; scroll-snap-type: x mandatory; padding-bottom: 10px; margin: 0 -5px; padding: 0 5px 10px; }
                    .brand-item { scroll-snap-align: start; flex: 0 0 100px; }
                    .brand-list::-webkit-scrollbar { height: 4px; }
                    .brand-list::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
                }
            </style>

            <div class="nava-collection-layout">
                <!-- Sidebar Filter -->
                <div class="nava-sidebar">
                    <div class="filter-sidebar" style="background: var(--bg-white); padding: 25px 20px; border-radius: var(--radius-lg); border: 1px solid var(--border-color); box-shadow: var(--shadow-sm); box-sizing: border-box; width: 100%;">
                        
                        <div class="sidebar-block">
                            <h4 class="sidebar-title">DANH MỤC SẢN PHẨM</h4>
                            <ul class="category-list">
                                <li><a href="#" style="color: var(--primary);"><img src="//bizweb.dktcdn.net/thumb/small/100/543/817/themes/1000289/assets/icon_dmenu_3.png?1775454528082" style="width:22px;height:22px;object-fit:contain;"> Mini PC <span class="count">(145) <i class="ph-bold ph-caret-down"></i></span></a></li>
                                <li><a href="#"><img src="//bizweb.dktcdn.net/thumb/small/100/543/817/themes/1000289/assets/icon_dmenu_4.png?1775454528082" style="width:22px;height:22px;object-fit:contain;"> eGPU <span class="count">(14)</span></a></li>
                                <li><a href="#"><img src="//bizweb.dktcdn.net/thumb/small/100/543/817/themes/1000289/assets/icon_dmenu_6.png?1775454528082" style="width:22px;height:22px;object-fit:contain;"> RAM/SSD <span class="count">(11)</span></a></li>
                                <li><a href="#"><img src="//bizweb.dktcdn.net/thumb/small/100/543/817/themes/1000289/assets/icon_dmenu_6.png?1775454528082" style="width:22px;height:22px;object-fit:contain;"> Màn hình <span class="count">(28)</span></a></li>
                                <li><a href="#"><img src="//bizweb.dktcdn.net/thumb/small/100/543/817/themes/1000289/assets/icon_dmenu_7.png?1775454528082" style="width:22px;height:22px;object-fit:contain;"> Phụ kiện <span class="count">(25)</span></a></li>
                                <li><a href="#"><img src="//bizweb.dktcdn.net/thumb/small/100/543/817/themes/1000289/assets/icon_dmenu_8.png?1775454528082" style="width:22px;height:22px;object-fit:contain;"> Like new <span class="count">(6)</span></a></li>
                            </ul>
                        </div>

                        
                        <!-- Lọc giá -->
                        <div class="sidebar-block">
                            <h4 class="sidebar-title">LỌC GIÁ</h4>
                            <div style="margin-bottom: 20px; padding: 0 5px;">
                                <style>
                                    .range-slider { position: relative; height: 20px; margin-top: 10px; margin-bottom: 15px; }
                                    .range-slider input[type="range"] { position: absolute; width: 100%; height: 4px; background: transparent; -webkit-appearance: none; pointer-events: none; outline: none; margin: 0; top: 8px; z-index: 3; }
                                    .range-slider input[type="range"]::-webkit-slider-thumb { -webkit-appearance: none; pointer-events: auto; width: 16px; height: 16px; background: white; border: 2px solid var(--primary); border-radius: 50%; cursor: pointer; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }
                                    .range-track { position: absolute; width: 100%; height: 4px; background: var(--bg-gray); top: 8px; border-radius: 2px; }
                                    .range-fill { position: absolute; height: 100%; background: var(--primary); top: 0; border-radius: 2px; }
                                </style>
                                <div class="range-slider">
                                    <div class="range-track"><div class="range-fill" id="priceFill" style="left: 10%; right: 25%;"></div></div>
                                    <input type="range" min="0" max="40000000" step="500000" value="4000000" id="priceMin" oninput="updatePriceVisuals()" onchange="if(typeof applyFiltersAndSort === 'function') applyFiltersAndSort()">
                                    <input type="range" min="0" max="40000000" step="500000" value="30000000" id="priceMax" oninput="updatePriceVisuals()" onchange="if(typeof applyFiltersAndSort === 'function') applyFiltersAndSort()">
                                </div>
                                <div style="display: flex; justify-content: space-between; align-items: center; gap: 10px;">
                                    <input type="text" id="priceInputMin" value="4.000.000đ" readonly style="flex: 1; min-width: 0; padding: 8px 4px; border: 1px solid var(--border-color); border-radius: 6px; font-size: 0.85rem; color: var(--text-color); font-weight: 700; text-align: center; outline: none; box-shadow: inset 0 1px 2px rgba(0,0,0,0.02); background: var(--bg-gray);">
                                    <span style="color: var(--text-gray); flex-shrink: 0; font-weight: bold;">-</span>
                                    <input type="text" id="priceInputMax" value="30.000.000đ" readonly style="flex: 1; min-width: 0; padding: 8px 4px; border: 1px solid var(--border-color); border-radius: 6px; font-size: 0.85rem; color: var(--text-color); font-weight: 700; text-align: center; outline: none; box-shadow: inset 0 1px 2px rgba(0,0,0,0.02); background: var(--bg-gray);">
                                </div>
                                <script>
                                    function updatePriceVisuals() {
                                        let minVal = parseInt(document.getElementById('priceMin').value);
                                        let maxVal = parseInt(document.getElementById('priceMax').value);
                                        if(minVal > maxVal) { let tmp = minVal; minVal = maxVal; maxVal = tmp; }
                                        document.getElementById('priceInputMin').value = minVal.toLocaleString('vi-VN') + 'đ';
                                        document.getElementById('priceInputMax').value = maxVal.toLocaleString('vi-VN') + 'đ';
                                        const fill = document.getElementById('priceFill');
                                        fill.style.left = (minVal / 40000000 * 100) + '%';
                                        fill.style.right = (100 - (maxVal / 40000000 * 100)) + '%';
                                    }
                                </script>
                            </div>

                        </div>

                        <!-- Thương hiệu -->
                        <div class="sidebar-block">
                            <h4 class="sidebar-title">THƯƠNG HIỆU</h4>
                            <div class="brand-list">
                                <div class="brand-item" title="ASUS"><img src="assets/asus.png" alt="ASUS" style="max-height: 24px; max-width: 85%; object-fit: contain;"></div>
                                <div class="brand-item" title="BEELINK"><img src="https://bizweb.dktcdn.net/100/543/817/files/beelink.png" alt="BEELINK" style="max-height: 24px; max-width: 85%; object-fit: contain;"></div>
                                <div class="brand-item" title="BEIKONG"><img src="https://bizweb.dktcdn.net/100/543/817/files/beikong.png" alt="BEIKONG" style="max-height: 24px; max-width: 85%; object-fit: contain;"></div>
                                <div class="brand-item" title="BMAX"><img src="https://bizweb.dktcdn.net/100/543/817/files/bmax.png" alt="BMAX" style="max-height: 24px; max-width: 85%; object-fit: contain;"></div>
                                <div class="brand-item" title="AOOSTAR"><img src="assets/aoostar.png" alt="AOOSTAR" style="max-height: 24px; max-width: 85%; object-fit: contain;"></div>
                                <div class="brand-item" title="GMKTEC"><img src="https://bizweb.dktcdn.net/100/543/817/files/gmktec.png" alt="GMKTEC" style="max-height: 24px; max-width: 85%; object-fit: contain;"></div>
                                <div class="brand-item" title="MINISFORUM"><img src="https://bizweb.dktcdn.net/100/543/817/files/minisforum.png" alt="MINISFORUM" style="max-height: 24px; max-width: 85%; object-fit: contain;"></div>
                                <div class="brand-item" title="MSI"><img src="assets/msi.png" alt="MSI" style="max-height: 24px; max-width: 85%; object-fit: contain;"></div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Main Content -->
                <div class="nava-main">
                    <!-- AI Search Bar & Sort (single unified bar) -->
                    <div style="display: flex; align-items: center; margin-bottom: 30px; gap: 16px; flex-wrap: nowrap; overflow: visible;">
                        <!-- AI Search Bar -->
                        <div id="ai-search-widget" style="flex: 1; min-width: 0; position: relative;">
                            <style>
                                .ai-glow-wrap { background: linear-gradient(90deg, #1d4ed8, #3b82f6, #38bdf8, #3b82f6, #1d4ed8); background-size: 300% 100%; animation: glow-anim 5s ease infinite; border-radius: 50px; padding: 2px; box-shadow: 0 6px 20px rgba(59,130,246,0.2); }
                                @keyframes glow-anim { 0%,100% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } }
                                .ai-inner { background: var(--bg-white, #fff); border-radius: 48px; display: flex; align-items: center; padding: 5px 6px 5px 18px; gap: 10px; }
                                .ai-input { flex: 1; border: none; outline: none; background: transparent; font-size: 1rem; color: var(--text-color, #1e293b); font-weight: 500; min-width: 0; }
                                .ai-input::placeholder { color: var(--text-gray, #94a3b8); }
                                .ai-btn { background: linear-gradient(270deg, #1e3a8a, #3b82f6, #38bdf8, #3b82f6, #1e3a8a); background-size: 300% 100%; animation: glow-anim 5s ease infinite; border: none; color: white; padding: 8px 18px; border-radius: 40px; font-weight: 700; font-size: 0.85rem; cursor: pointer; transition: all 0.2s; box-shadow: 0 3px 10px rgba(30,58,138,0.35); white-space: nowrap; flex-shrink: 0; display: flex; align-items: center; gap: 6px; }
                                .ai-btn:hover { transform: translateY(-1px); box-shadow: 0 5px 15px rgba(59,130,246,0.5); }
                                @keyframes pulse-sparkle { 0%,100% { transform: scale(1); } 50% { transform: scale(1.15); } }
                                .ai-results-dropdown { position: absolute; top: calc(100% + 12px); left: 0; right: 0; background: var(--bg-white, #fff); border-radius: 16px; box-shadow: 0 20px 50px rgba(0,0,0,0.12); border: 1px solid var(--border-color, #e2e8f0); z-index: 999; overflow: hidden; opacity: 0; visibility: hidden; transform: translateY(-8px); transition: all 0.25s cubic-bezier(0.4,0,0.2,1); }
                                .ai-results-dropdown.active { opacity: 1; visibility: visible; transform: translateY(0); }
                                .ai-result-header { padding: 14px 20px 10px; font-size: 0.8rem; color: var(--text-gray, #64748b); font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 1px solid var(--border-color, #f1f5f9); }
                                .ai-result-item { display: flex; align-items: center; gap: 14px; padding: 12px 20px; border-bottom: 1px solid var(--border-color, #f8fafc); cursor: pointer; transition: background 0.15s; text-decoration: none; }
                                .ai-result-item:hover { background: var(--bg-gray, #f8fafc); }
                                .ai-result-img { width: 64px; height: 64px; object-fit: contain; border-radius: 10px; background: transparent; padding: 6px; flex-shrink: 0; border: 1px solid var(--border-color, #f1f5f9); }
                                .ai-result-info h5 { margin: 0 0 4px; font-size: 0.9rem; color: var(--text-color, #1e293b); font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 400px; }
                                .ai-result-price { display: inline-block; color: white; background: linear-gradient(135deg,#1e3a8a,#2563eb); font-weight: 700; font-size: 0.82rem; padding: 3px 10px; border-radius: 20px; margin-top: 4px; }
                                .ai-view-more { display: flex; align-items: center; justify-content: center; gap: 8px; padding: 14px; background: linear-gradient(135deg, rgba(37,99,235,0.05), rgba(37,99,235,0.1)); color: #2563eb; font-weight: 700; font-size: 0.92rem; text-decoration: none; transition: background 0.2s; }
                                .ai-view-more:hover { background: linear-gradient(135deg, rgba(37,99,235,0.1), rgba(37,99,235,0.15)); }
                                .ai-loading-row { display: flex; align-items: center; justify-content: center; gap: 10px; padding: 20px; color: var(--text-gray, #64748b); font-size: 0.95rem; }
                                @keyframes ai-spin { 100% { transform: rotate(360deg); } }
                                .ai-spinner { width: 18px; height: 18px; border: 2px solid var(--border-color, #dbeafe); border-top-color: #3b82f6; border-radius: 50%; animation: ai-spin 0.7s linear infinite; }
                                /* Sort */
                                .sort-pill-btn { display: flex; align-items: center; gap: 10px; background: var(--bg-white, #fff); border: 1px solid var(--border-color, #e2e8f0); color: var(--text-color, #334155); padding: 10px 18px; border-radius: 40px; font-weight: 700; font-size: 0.92rem; cursor: pointer; white-space: nowrap; box-shadow: 0 2px 8px rgba(0,0,0,0.05); transition: all 0.2s; flex-shrink: 0; }
                                .sort-pill-btn:hover { border-color: var(--primary); box-shadow: 0 4px 12px rgba(59,130,246,0.15); }
                                .sort-drop-menu { position: absolute; top: calc(100% + 8px); right: 0; background: var(--bg-white, #fff); border: 1px solid var(--border-color, #e2e8f0); border-radius: 12px; padding: 6px 0; min-width: 180px; box-shadow: 0 12px 30px rgba(0,0,0,0.1); display: none; z-index: 999; }
                                .sort-drop-menu.show { display: block; }
                                .sort-drop-menu a { display: block; padding: 10px 18px; color: var(--text-color, #334155); text-decoration: none; font-weight: 600; font-size: 0.9rem; transition: all 0.15s; }
                                .sort-drop-menu a:hover { background: var(--bg-gray, #eff6ff); color: var(--primary); }
                            </style>
                            <div class="ai-glow-wrap">
                                <div class="ai-inner">
                                    <i class="ph-fill ph-sparkle" style="font-size: 1.4rem; color: #3b82f6; flex-shrink: 0; animation: pulse-sparkle 2s infinite;"></i>
                                    <input type="text" class="ai-input" id="aiSearchInput" placeholder="Mô tả AI... (VD: Mini PC chơi game Wukong giá dưới 15 củ)">
                                    <button class="ai-btn" id="aiSearchBtn"><i class="ph-bold ph-magnifying-glass"></i> Tìm kiếm AI</button>
                                </div>
                            </div>
                            <!-- AI Results -->
                            <div class="ai-results-dropdown" id="aiResultsDropdown">
                                <div class="ai-result-header" id="aiResultHeader">🤖 AI đang phân tích...</div>
                                <div id="aiLoading"><div class="ai-loading-row"><div class="ai-spinner"></div> Đang tìm sản phẩm phù hợp...</div></div>
                                <div id="aiResultsList" style="display:none;">
                                    <!-- AI Analysis Summary -->
                                    <div style="padding: 15px 20px; border-bottom: 1px solid #f1f5f9; background: #f8fafc;">
                                        <div style="display: flex; gap: 10px; align-items: flex-start;">
                                            <div style="width: 28px; height: 28px; border-radius: 50%; background: linear-gradient(135deg, #1e3a8a, #3b82f6); color: white; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-top: 2px; box-shadow: 0 4px 10px rgba(37,99,235,0.2);"><i class="ph-bold ph-robot"></i></div>
                                            <div>
                                                <div style="font-size: 0.9rem; color: #334155; line-height: 1.5;" id="aiSummaryText">
                                                    <strong>Phân tích:</strong> Đang xử lý yêu cầu...
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <!-- Top Recommendation -->
                                    <div style="padding: 15px 20px 5px; font-size: 0.8rem; color: #d97706; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; display: flex; align-items: center; gap: 6px;">
                                        <i class="ph-fill ph-check-circle" style="font-size: 1.1rem;"></i> ĐỀ XUẤT PHÙ HỢP NHẤT
                                    </div>
                                    <a href="#" class="ai-result-item" style="background: rgba(217, 119, 6, 0.06); border-left: 3px solid #d97706; margin: 0 10px 10px; border-radius: 8px;">
                                        <img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_1.png" class="ai-result-img" alt="GMKTEC">
                                        <div class="ai-result-info" style="white-space: normal;">
                                            <h5 style="white-space: nowrap;">GMKTEC NucBox K6 (Ryzen 7 7840HS / 32GB)</h5>
                                            <div style="font-size: 0.8rem; color: #475569; margin: 4px 0 6px; line-height: 1.4;">Tích hợp Radeon 780M cực mạnh, RAM 32GB lớn, đáp ứng hoàn hảo nhu cầu chiến mượt các tựa game AAA.</div>
                                            <div class="ai-result-price" style="background: linear-gradient(135deg, #b45309, #d97706); box-shadow: 0 2px 6px rgba(217,119,6,0.2);">14.200.000₫</div>
                                        </div>
                                    </a>
                                    
                                    <!-- Other Options -->
                                    <div style="padding: 10px 20px 5px; font-size: 0.75rem; color: #94a3b8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; border-top: 1px solid #f1f5f9;">
                                        Các lựa chọn thay thế khác
                                    </div>
                                    <a href="#" class="ai-result-item">
                                        <img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" class="ai-result-img" alt="ASUS NUC">
                                        <div class="ai-result-info"><h5>ASUS NUC 14 Pro Core Ultra 5 (16GB/512GB)</h5><div class="ai-result-price">12.500.000₫</div></div>
                                    </a>
                                    <a href="#" class="ai-view-more">Xem thêm tất cả 8 kết quả &nbsp;<i class="ph-bold ph-arrow-right"></i></a>
                                </div>
                            </div>
                            <script>
                                (function() {
                                    var input = document.getElementById('aiSearchInput');
                                    var btn = document.getElementById('aiSearchBtn');
                                    var drop = document.getElementById('aiResultsDropdown');
                                    var loading = document.getElementById('aiLoading');
                                    var list = document.getElementById('aiResultsList');
                                    var header = document.getElementById('aiResultHeader');
                                    var summary = document.getElementById('aiSummaryText');
                                    var timer = null;
                                    function doSearch() {
                                        var q = input.value.trim();
                                        if (!q) { drop.classList.remove('active'); return; }
                                        drop.classList.add('active');
                                        loading.style.display = 'block';
                                        list.style.display = 'none';
                                        header.textContent = '\uD83E\uDD16 AI đang phân tích: "' + q + '"...';
                                        
                                        // Cập nhật text mockup
                                        summary.innerHTML = '<strong>Phân tích nhu cầu:</strong> Bạn đang tìm kiếm <em>"' + q + '"</em>. Dựa trên dữ liệu, AI ưu tiên đề xuất máy có GPU tích hợp mạnh, RAM tối thiểu 16GB và tản nhiệt tốt trong phân khúc.';
                                        
                                        setTimeout(function() {
                                            loading.style.display = 'none';
                                            list.style.display = 'block';
                                            header.textContent = '\u2728 HOÀN TẤT PHÂN TÍCH & TÌM KIẾM';
                                        }, 1200);
                                    }
                                    input.addEventListener('input', function() { clearTimeout(timer); timer = setTimeout(doSearch, 700); });
                                    input.addEventListener('keypress', function(e) { if (e.key==='Enter') { clearTimeout(timer); doSearch(); } });
                                    btn.addEventListener('click', function() { clearTimeout(timer); doSearch(); });
                                    document.addEventListener('click', function(e) { if (!document.getElementById('ai-search-widget').contains(e.target)) drop.classList.remove('active'); });
                                })();
                            </script>
                        </div>

                        <!-- Sort Dropdown -->
                        <div style="position: relative; flex-shrink: 0;">
                            <button class="sort-pill-btn" id="sortToggleBtn" onclick="document.getElementById('sortDropMenu').classList.toggle('show')">
                                <i class="ph ph-sort-ascending" style="color: var(--primary);"></i>
                                <span id="sortLabel">Mặc định</span>
                                <i class="ph ph-caret-down" style="color:#94a3b8; font-size:0.85rem;"></i>
                            </button>
                            <div class="sort-drop-menu" id="sortDropMenu">
                                <a href="#" onclick="document.getElementById('sortLabel').textContent='Mặc định'; document.getElementById('sortDropMenu').classList.remove('show'); return false;"><i class="ph ph-list-dashes" style="margin-right:8px; font-size: 1.1em; vertical-align: middle;"></i> Mặc định</a>
                                <a href="#" onclick="document.getElementById('sortLabel').textContent='Giá tăng dần'; document.getElementById('sortDropMenu').classList.remove('show'); return false;"><i class="ph ph-sort-ascending" style="margin-right:8px; font-size: 1.1em; vertical-align: middle;"></i> Giá tăng dần</a>
                                <a href="#" onclick="document.getElementById('sortLabel').textContent='Giá giảm dần'; document.getElementById('sortDropMenu').classList.remove('show'); return false;"><i class="ph ph-sort-descending" style="margin-right:8px; font-size: 1.1em; vertical-align: middle;"></i> Giá giảm dần</a>
                                <a href="#" onclick="document.getElementById('sortLabel').textContent='Mới nhất'; document.getElementById('sortDropMenu').classList.remove('show'); return false;"><i class="ph ph-sparkle" style="margin-right:8px; font-size: 1.1em; vertical-align: middle;"></i> Mới nhất</a>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Featured Products -->
                    <div class="featured-section" style="display: none; margin-bottom: 40px;">
                        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px;">
                            <h3 style="margin: 0; font-size: 1.25rem; font-weight: 800; color: var(--text-color); display: flex; align-items: center; gap: 8px;">
                                <i class="ph-fill ph-star" style="color: var(--primary); font-size: 1.4rem;"></i> Nổi bật nhất
                            </h3>
                        </div>
                        <div class="featured-grid" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;">
                            
                            <div class="product-card" style="margin:0; display: flex; align-items: center; padding: 15px; gap: 15px;" onclick="window.location.href='demo_product.html'">
                                <div style="width: 90px; height: 90px; flex-shrink: 0; position: relative;">
                                    <button class="compare-btn" data-name="ASUS NUC 14 Essential" title="Thêm vào so sánh" style="position: absolute; top: -5px; right: -5px; width: 28px; height: 28px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-color); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'ASUS NUC 14 Essential', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png', '4.490.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right" style="font-size: 0.8rem;"></i></button>
                                
                                    <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" alt="Featured" style="width: 100%; height: 100%; object-fit: contain;">
                                </div>
                                <div style="flex: 1; min-width: 0;">
                                    <span class="spec-pill" style="margin-bottom: 8px;">HOT SALE</span>
                                    <h4 style="margin: 0 0 6px 0; font-size: 0.95rem; font-weight: 700; color: var(--text-color); display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; line-height: 1.4;">ASUS NUC 14 Essential</h4>
                                    <span style="color: var(--text-color); font-weight: 800; font-size: 1.1rem;">4.490.000₫</span>
                                </div>
                            </div>
                            
                            <div class="product-card" style="margin:0; display: flex; align-items: center; padding: 15px; gap: 15px;" onclick="window.location.href='demo_product.html'">
                                <div style="width: 90px; height: 90px; flex-shrink: 0; position: relative;">
                                    <button class="compare-btn" data-name="AtomMan G7 PT Mini PC" title="Thêm vào so sánh" style="position: absolute; top: -5px; right: -5px; width: 28px; height: 28px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-color); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'AtomMan G7 PT Mini PC', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png', '34.490.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right" style="font-size: 0.8rem;"></i></button>
                                
                                    <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" alt="Featured" style="width: 100%; height: 100%; object-fit: contain;">
                                </div>
                                <div style="flex: 1; min-width: 0;">
                                    <span class="spec-pill" style="margin-bottom: 8px;">BÁN CHẠY</span>
                                    <h4 style="margin: 0 0 6px 0; font-size: 0.95rem; font-weight: 700; color: var(--text-color); display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; line-height: 1.4;">AtomMan G7 PT Mini PC</h4>
                                    <span style="color: var(--text-color); font-weight: 800; font-size: 1.1rem;">34.490.000₫</span>
                                </div>
                            </div>
                            
                            <div class="product-card" style="margin:0; display: flex; align-items: center; padding: 15px; gap: 15px;" onclick="window.location.href='demo_product.html'">
                                <div style="width: 90px; height: 90px; flex-shrink: 0; position: relative;">
                                    <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_1.png" alt="Featured" style="width: 100%; height: 100%; object-fit: contain;">
                                </div>
                                <div style="flex: 1; min-width: 0;">
                                    <span class="spec-pill" style="margin-bottom: 8px;">MỚI RA MẮT</span>
                                    <h4 style="margin: 0 0 6px 0; font-size: 0.95rem; font-weight: 700; color: var(--text-color); display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; line-height: 1.4;">GMK EVO X1 32G</h4>
                                    <span style="color: var(--text-color); font-weight: 800; font-size: 1.1rem;">31.190.000₫</span>
                                </div>
                            </div>
                            
                        </div>
                        <style>
                            @media (max-width: 1399px) { .featured-grid { grid-template-columns: repeat(2, 1fr) !important; } }
                            @media (max-width: 768px) { .featured-grid { grid-template-columns: 1fr !important; } }
                        </style>
                    </div>
                    
                    <!-- Product Grid (4 columns) -->
                    <div class="product-grid" style="grid-template-columns: repeat(2, 1fr); gap: 20px;">
                        
                        <!-- Product 1 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="ASUS NUC 14 Essential Int" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-color); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'ASUS NUC 14 Essential Int', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png', '4.490.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
                                <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" alt="ASUS NUC 14" class="product-img" style="object-fit: contain; width: 100%; height: 100%; transition: transform 0.4s ease;">
                            </div>
                            <div class="card-content" style="padding: 15px 0 0 0; flex: 1; display: flex; flex-direction: column;">
                                <!-- Specs Badges -->
                                <div class="card-specs">
                                    <span class="spec-pill">CPU 6.000</span>
                                    <span class="spec-pill secondary">MARK</span>
                                    <span class="spec-pill secondary">GPU 1.200</span>
                                    <span class="spec-pill">WIFI 6E</span>
                                    <span class="spec-pill secondary">4 USB 3.2</span>
                                    <span class="spec-pill secondary">2 TYPE C</span>
                                </div>
                                
                                <h2 class="card-title" style="font-size: 1rem; line-height: 1.4; margin-bottom: 10px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; height: 40px; font-weight: 700;">ASUS NUC 14 Essential Int...</h2>
                                
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: auto;">
                                    <span style="color: var(--text-color); font-weight: 800; font-size: 1.15rem;">4.490.000₫</span>
                                    <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                                </div>
                            </div>
                        </div>

                        <!-- Product 2 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="AtomMan G7 PT Mini PC" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-color); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'AtomMan G7 PT Mini PC', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png', '34.490.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
                                <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" alt="AtomMan G7 PT" class="product-img" style="object-fit: contain; width: 100%; height: 100%; transition: transform 0.4s ease;">
                            </div>
                            <div class="card-content" style="padding: 15px 0 0 0; flex: 1; display: flex; flex-direction: column;">
                                <div class="card-specs">
                                    <span class="spec-pill">CPU 40.000</span>
                                    <span class="spec-pill secondary">MARK</span>
                                    <span class="spec-pill secondary">GPU 17...</span>
                                    <span class="spec-pill">4 FAN S...</span>
                                    <span class="spec-pill secondary">WIFI 7</span>
                                </div>
                                
                                <h2 class="card-title" style="font-size: 1rem; line-height: 1.4; margin-bottom: 10px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; height: 40px; font-weight: 700;">AtomMan G7 PT Mini PC...</h2>
                                
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: auto;">
                                    <span style="color: var(--text-color); font-weight: 800; font-size: 1.15rem;">34.490.000₫</span>
                                    <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                                </div>
                            </div>
                        </div>

                        <!-- Product 3 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="Mini PC GMK EVO X1 32G" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-color); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'Mini PC GMK EVO X1 32G', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_1.png', '31.190.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
                                <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_1.png" alt="GMK EVO X1" class="product-img" style="object-fit: contain; width: 100%; height: 100%; transition: transform 0.4s ease;">
                            </div>
                            <div class="card-content" style="padding: 15px 0 0 0; flex: 1; display: flex; flex-direction: column;">
                                <div class="card-specs">
                                    <span class="spec-pill">CPU 38.500</span>
                                    <span class="spec-pill secondary">MARK</span>
                                    <span class="spec-pill secondary">GPU ...</span>
                                    <span class="spec-pill">2 NVME</span>
                                    <span class="spec-pill secondary">USB4</span>
                                </div>
                                
                                <h2 class="card-title" style="font-size: 1rem; line-height: 1.4; margin-bottom: 10px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; height: 40px; font-weight: 700;">Mini PC GMK EVO X1 32G...</h2>
                                
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: auto;">
                                    <span style="color: var(--text-color); font-weight: 800; font-size: 1.15rem;">31.190.000₫</span>
                                    <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                                </div>
                            </div>
                        </div>

                        <!-- Product 4 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="Tablet Minisforum V3 SE" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-color); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'Tablet Minisforum V3 SE', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_2.png', '23.090.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
                                <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_2.png" alt="Tablet Minisforum" class="product-img" style="object-fit: contain; width: 100%; height: 100%; transition: transform 0.4s ease;">
                            </div>
                            <div class="card-content" style="padding: 15px 0 0 0; flex: 1; display: flex; flex-direction: column;">
                                <div class="card-specs">
                                    <span class="spec-pill">CPU 22.000</span>
                                    <span class="spec-pill secondary">MARK</span>
                                    <span class="spec-pill secondary">CPU ...</span>
                                    <span class="spec-pill">WIFI 6</span>
                                    <span class="spec-pill secondary">2 USB4</span>
                                </div>
                                
                                <h2 class="card-title" style="font-size: 1rem; line-height: 1.4; margin-bottom: 10px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; height: 40px; font-weight: 700;">Tablet Minisforum V3 SE...</h2>
                                
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: auto;">
                                    <span style="color: var(--text-color); font-weight: 800; font-size: 1.15rem;">23.090.000₫</span>
                                    <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Product 5 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="Beelink SER8 AMD 884" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-color); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'Beelink SER8 AMD 884', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_2.png', '11.990.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
                                <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_2.png" alt="Beelink SER8" class="product-img" style="object-fit: contain; width: 100%; height: 100%; transition: transform 0.4s ease;">
                            </div>
                            <div class="card-content" style="padding: 15px 0 0 0; flex: 1; display: flex; flex-direction: column;">
                                <div class="card-specs">
                                    <span class="spec-pill">CPU 26.000</span>
                                    <span class="spec-pill secondary">MARK</span>
                                    <span class="spec-pill secondary">GPU 16...</span>
                                    <span class="spec-pill">WIFI 6</span>
                                </div>
                                
                                <h2 class="card-title" style="font-size: 1rem; line-height: 1.4; margin-bottom: 10px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; height: 40px; font-weight: 700;">Beelink SER8 AMD 884...</h2>
                                
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: auto;">
                                    <span style="color: var(--text-color); font-weight: 800; font-size: 1.15rem;">11.990.000₫</span>
                                    <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                                </div>
                            </div>
                        </div>
                        
<!-- Product 6 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="ASUS NUC 14 Essential Int" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-color); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'ASUS NUC 14 Essential Int', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png', '4.490.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
                                <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" alt="ASUS NUC 14" class="product-img" style="object-fit: contain; width: 100%; height: 100%; transition: transform 0.4s ease;">
                            </div>
                            <div class="card-content" style="padding: 15px 0 0 0; flex: 1; display: flex; flex-direction: column;">
                                <!-- Specs Badges -->
                                <div class="card-specs">
                                    <span class="spec-pill">CPU 6.000</span>
                                    <span class="spec-pill secondary">MARK</span>
                                    <span class="spec-pill secondary">GPU 1.200</span>
                                    <span class="spec-pill">WIFI 6E</span>
                                    <span class="spec-pill secondary">4 USB 3.2</span>
                                    <span class="spec-pill secondary">2 TYPE C</span>
                                </div>
                                
                                <h2 class="card-title" style="font-size: 1rem; line-height: 1.4; margin-bottom: 10px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; height: 40px; font-weight: 700;">ASUS NUC 14 Essential Int...</h2>
                                
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: auto;">
                                    <span style="color: var(--text-color); font-weight: 800; font-size: 1.15rem;">4.490.000₫</span>
                                    <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                                </div>
                            </div>
                        </div>

                        <!-- Product 7 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="AtomMan G7 PT Mini PC" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-color); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'AtomMan G7 PT Mini PC', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png', '34.490.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
                                <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" alt="AtomMan G7 PT" class="product-img" style="object-fit: contain; width: 100%; height: 100%; transition: transform 0.4s ease;">
                            </div>
                            <div class="card-content" style="padding: 15px 0 0 0; flex: 1; display: flex; flex-direction: column;">
                                <div class="card-specs">
                                    <span class="spec-pill">CPU 40.000</span>
                                    <span class="spec-pill secondary">MARK</span>
                                    <span class="spec-pill secondary">GPU 17...</span>
                                    <span class="spec-pill">4 FAN S...</span>
                                    <span class="spec-pill secondary">WIFI 7</span>
                                </div>
                                
                                <h2 class="card-title" style="font-size: 1rem; line-height: 1.4; margin-bottom: 10px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; height: 40px; font-weight: 700;">AtomMan G7 PT Mini PC...</h2>
                                
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: auto;">
                                    <span style="color: var(--text-color); font-weight: 800; font-size: 1.15rem;">34.490.000₫</span>
                                    <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                                </div>
                            </div>
                        </div>

                        <!-- Product 8 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="Mini PC GMK EVO X1 32G" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-color); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'Mini PC GMK EVO X1 32G', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_1.png', '31.190.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
                                <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_1.png" alt="GMK EVO X1" class="product-img" style="object-fit: contain; width: 100%; height: 100%; transition: transform 0.4s ease;">
                            </div>
                            <div class="card-content" style="padding: 15px 0 0 0; flex: 1; display: flex; flex-direction: column;">
                                <div class="card-specs">
                                    <span class="spec-pill">CPU 38.500</span>
                                    <span class="spec-pill secondary">MARK</span>
                                    <span class="spec-pill secondary">GPU ...</span>
                                    <span class="spec-pill">2 NVME</span>
                                    <span class="spec-pill secondary">USB4</span>
                                </div>
                                
                                <h2 class="card-title" style="font-size: 1rem; line-height: 1.4; margin-bottom: 10px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; height: 40px; font-weight: 700;">Mini PC GMK EVO X1 32G...</h2>
                                
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: auto;">
                                    <span style="color: var(--text-color); font-weight: 800; font-size: 1.15rem;">31.190.000₫</span>
                                    <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                                </div>
                            </div>
                        </div>

                        <!-- Product 9 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="Tablet Minisforum V3 SE" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-color); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'Tablet Minisforum V3 SE', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_2.png', '23.090.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
                                <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_2.png" alt="Tablet Minisforum" class="product-img" style="object-fit: contain; width: 100%; height: 100%; transition: transform 0.4s ease;">
                            </div>
                            <div class="card-content" style="padding: 15px 0 0 0; flex: 1; display: flex; flex-direction: column;">
                                <div class="card-specs">
                                    <span class="spec-pill">CPU 22.000</span>
                                    <span class="spec-pill secondary">MARK</span>
                                    <span class="spec-pill secondary">CPU ...</span>
                                    <span class="spec-pill">WIFI 6</span>
                                    <span class="spec-pill secondary">2 USB4</span>
                                </div>
                                
                                <h2 class="card-title" style="font-size: 1rem; line-height: 1.4; margin-bottom: 10px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; height: 40px; font-weight: 700;">Tablet Minisforum V3 SE...</h2>
                                
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: auto;">
                                    <span style="color: var(--text-color); font-weight: 800; font-size: 1.15rem;">23.090.000₫</span>
                                    <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Product 10 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="Beelink SER8 AMD 884" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-color); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'Beelink SER8 AMD 884', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_2.png', '11.990.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
                                <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_2.png" alt="Beelink SER8" class="product-img" style="object-fit: contain; width: 100%; height: 100%; transition: transform 0.4s ease;">
                            </div>
                            <div class="card-content" style="padding: 15px 0 0 0; flex: 1; display: flex; flex-direction: column;">
                                <div class="card-specs">
                                    <span class="spec-pill">CPU 26.000</span>
                                    <span class="spec-pill secondary">MARK</span>
                                    <span class="spec-pill secondary">GPU 16...</span>
                                    <span class="spec-pill">WIFI 6</span>
                                </div>
                                
                                <h2 class="card-title" style="font-size: 1rem; line-height: 1.4; margin-bottom: 10px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; height: 40px; font-weight: 700;">Beelink SER8 AMD 884...</h2>
                                
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: auto;">
                                    <span style="color: var(--text-color); font-weight: 800; font-size: 1.15rem;">11.990.000₫</span>
                                    <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                                </div>
                            </div>
                        </div>
                        
<!-- Product 11 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="ASUS NUC 14 Essential Int" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-color); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'ASUS NUC 14 Essential Int', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png', '4.490.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
                                <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" alt="ASUS NUC 14" class="product-img" style="object-fit: contain; width: 100%; height: 100%; transition: transform 0.4s ease;">
                            </div>
                            <div class="card-content" style="padding: 15px 0 0 0; flex: 1; display: flex; flex-direction: column;">
                                <!-- Specs Badges -->
                                <div class="card-specs">
                                    <span class="spec-pill">CPU 6.000</span>
                                    <span class="spec-pill secondary">MARK</span>
                                    <span class="spec-pill secondary">GPU 1.200</span>
                                    <span class="spec-pill">WIFI 6E</span>
                                    <span class="spec-pill secondary">4 USB 3.2</span>
                                    <span class="spec-pill secondary">2 TYPE C</span>
                                </div>
                                
                                <h2 class="card-title" style="font-size: 1rem; line-height: 1.4; margin-bottom: 10px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; height: 40px; font-weight: 700;">ASUS NUC 14 Essential Int...</h2>
                                
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: auto;">
                                    <span style="color: var(--text-color); font-weight: 800; font-size: 1.15rem;">4.490.000₫</span>
                                    <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                                </div>
                            </div>
                        </div>

                        <!-- Product 12 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="AtomMan G7 PT Mini PC" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-color); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'AtomMan G7 PT Mini PC', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png', '34.490.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
                                <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" alt="AtomMan G7 PT" class="product-img" style="object-fit: contain; width: 100%; height: 100%; transition: transform 0.4s ease;">
                            </div>
                            <div class="card-content" style="padding: 15px 0 0 0; flex: 1; display: flex; flex-direction: column;">
                                <div class="card-specs">
                                    <span class="spec-pill">CPU 40.000</span>
                                    <span class="spec-pill secondary">MARK</span>
                                    <span class="spec-pill secondary">GPU 17...</span>
                                    <span class="spec-pill">4 FAN S...</span>
                                    <span class="spec-pill secondary">WIFI 7</span>
                                </div>
                                
                                <h2 class="card-title" style="font-size: 1rem; line-height: 1.4; margin-bottom: 10px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; height: 40px; font-weight: 700;">AtomMan G7 PT Mini PC...</h2>
                                
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: auto;">
                                    <span style="color: var(--text-color); font-weight: 800; font-size: 1.15rem;">34.490.000₫</span>
                                    <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                                </div>
                            </div>
                        </div>

                        <!-- Product 13 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="Mini PC GMK EVO X1 32G" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-color); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'Mini PC GMK EVO X1 32G', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_1.png', '31.190.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
                                <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_1.png" alt="GMK EVO X1" class="product-img" style="object-fit: contain; width: 100%; height: 100%; transition: transform 0.4s ease;">
                            </div>
                            <div class="card-content" style="padding: 15px 0 0 0; flex: 1; display: flex; flex-direction: column;">
                                <div class="card-specs">
                                    <span class="spec-pill">CPU 38.500</span>
                                    <span class="spec-pill secondary">MARK</span>
                                    <span class="spec-pill secondary">GPU ...</span>
                                    <span class="spec-pill">2 NVME</span>
                                    <span class="spec-pill secondary">USB4</span>
                                </div>
                                
                                <h2 class="card-title" style="font-size: 1rem; line-height: 1.4; margin-bottom: 10px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; height: 40px; font-weight: 700;">Mini PC GMK EVO X1 32G...</h2>
                                
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: auto;">
                                    <span style="color: var(--text-color); font-weight: 800; font-size: 1.15rem;">31.190.000₫</span>
                                    <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                                </div>
                            </div>
                        </div>

                        <!-- Product 14 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="Tablet Minisforum V3 SE" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-color); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'Tablet Minisforum V3 SE', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_2.png', '23.090.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
                                <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_2.png" alt="Tablet Minisforum" class="product-img" style="object-fit: contain; width: 100%; height: 100%; transition: transform 0.4s ease;">
                            </div>
                            <div class="card-content" style="padding: 15px 0 0 0; flex: 1; display: flex; flex-direction: column;">
                                <div class="card-specs">
                                    <span class="spec-pill">CPU 22.000</span>
                                    <span class="spec-pill secondary">MARK</span>
                                    <span class="spec-pill secondary">CPU ...</span>
                                    <span class="spec-pill">WIFI 6</span>
                                    <span class="spec-pill secondary">2 USB4</span>
                                </div>
                                
                                <h2 class="card-title" style="font-size: 1rem; line-height: 1.4; margin-bottom: 10px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; height: 40px; font-weight: 700;">Tablet Minisforum V3 SE...</h2>
                                
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: auto;">
                                    <span style="color: var(--text-color); font-weight: 800; font-size: 1.15rem;">23.090.000₫</span>
                                    <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Product 15 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="Beelink SER8 AMD 884" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-color); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'Beelink SER8 AMD 884', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_2.png', '11.990.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
                                <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_2.png" alt="Beelink SER8" class="product-img" style="object-fit: contain; width: 100%; height: 100%; transition: transform 0.4s ease;">
                            </div>
                            <div class="card-content" style="padding: 15px 0 0 0; flex: 1; display: flex; flex-direction: column;">
                                <div class="card-specs">
                                    <span class="spec-pill">CPU 26.000</span>
                                    <span class="spec-pill secondary">MARK</span>
                                    <span class="spec-pill secondary">GPU 16...</span>
                                    <span class="spec-pill">WIFI 6</span>
                                </div>
                                
                                <h2 class="card-title" style="font-size: 1rem; line-height: 1.4; margin-bottom: 10px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; height: 40px; font-weight: 700;">Beelink SER8 AMD 884...</h2>
                                
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: auto;">
                                    <span style="color: var(--text-color); font-weight: 800; font-size: 1.15rem;">11.990.000₫</span>
                                    <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                                </div>
                            </div>
                        </div>
                        
<!-- Product 16 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="ASUS NUC 14 Essential Int" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-color); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'ASUS NUC 14 Essential Int', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png', '4.490.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
                                <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" alt="ASUS NUC 14" class="product-img" style="object-fit: contain; width: 100%; height: 100%; transition: transform 0.4s ease;">
                            </div>
                            <div class="card-content" style="padding: 15px 0 0 0; flex: 1; display: flex; flex-direction: column;">
                                <!-- Specs Badges -->
                                <div class="card-specs">
                                    <span class="spec-pill">CPU 6.000</span>
                                    <span class="spec-pill secondary">MARK</span>
                                    <span class="spec-pill secondary">GPU 1.200</span>
                                    <span class="spec-pill">WIFI 6E</span>
                                    <span class="spec-pill secondary">4 USB 3.2</span>
                                    <span class="spec-pill secondary">2 TYPE C</span>
                                </div>
                                
                                <h2 class="card-title" style="font-size: 1rem; line-height: 1.4; margin-bottom: 10px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; height: 40px; font-weight: 700;">ASUS NUC 14 Essential Int...</h2>
                                
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: auto;">
                                    <span style="color: var(--text-color); font-weight: 800; font-size: 1.15rem;">4.490.000₫</span>
                                    <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                                </div>
                            </div>
                        </div>

                                            </div>
                    
                    <div class="pagination" style="display: flex; justify-content: center; gap: 12px; margin-top: 50px; margin-bottom: 20px;">
                        <button style="width: 44px; height: 44px; border-radius: 50%; border: 1px solid var(--border-color); background: var(--bg-white); color: var(--text-color); font-weight: bold; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.3s;" onmouseover="this.style.background='var(--bg-gray)'" onmouseout="this.style.background='var(--bg-white)'"><i class="ph ph-caret-left"></i></button>
                        <button style="width: 44px; height: 44px; border-radius: 50%; border: none; background: var(--primary); color: white; font-weight: bold; cursor: pointer; box-shadow: 0 4px 10px rgba(14, 165, 233, 0.3);">1</button>
                        <button style="width: 44px; height: 44px; border-radius: 50%; border: 1px solid var(--border-color); background: var(--bg-white); color: var(--text-color); font-weight: bold; cursor: pointer; transition: all 0.3s;" onmouseover="this.style.background='var(--bg-gray)'" onmouseout="this.style.background='var(--bg-white)'">2</button>
                        <button style="width: 44px; height: 44px; border-radius: 50%; border: 1px solid var(--border-color); background: var(--bg-white); color: var(--text-color); font-weight: bold; cursor: pointer; transition: all 0.3s;" onmouseover="this.style.background='var(--bg-gray)'" onmouseout="this.style.background='var(--bg-white)'">3</button>
                        <button style="width: 44px; height: 44px; border-radius: 50%; border: 1px solid var(--border-color); background: var(--bg-white); color: var(--text-color); font-weight: bold; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.3s;" onmouseover="this.style.background='var(--bg-gray)'" onmouseout="this.style.background='var(--bg-white)'"><i class="ph ph-caret-right"></i></button>
                    </div>
                </div>
            </div>
            
            <button class="mobile-filter-btn" onclick="toggleMobileSidebar()"><i class="ph-bold ph-faders"></i> Lọc sản phẩm</button>
            <div class="sidebar-overlay" onclick="toggleMobileSidebar()"></div>
            
            <div id="quick-view-modal" style="position: fixed; inset: 0; background: rgba(0,0,0,0.6); backdrop-filter: blur(5px); z-index: 10000; display: none; align-items: center; justify-content: center; opacity: 0; transition: opacity 0.3s;">
                <div style="background: var(--bg-white); width: 90%; max-width: 900px; height: 80vh; max-height: 600px; border-radius: var(--radius-lg); position: relative; display: flex; overflow: hidden; transform: scale(0.95); transition: transform 0.3s;">
                    <button onclick="closeQuickView()" style="position: absolute; top: 15px; right: 15px; background: var(--bg-gray); border: none; width: 40px; height: 40px; border-radius: 50%; font-size: 1.2rem; display: flex; align-items: center; justify-content: center; cursor: pointer; z-index: 10;" onmouseover="this.style.color='#ef4444'" onmouseout="this.style.color='var(--text-color)'"><i class="ph-bold ph-x"></i></button>
                    <div style="flex: 1; display: flex; align-items: center; justify-content: center; background: #f8fafc; padding: 20px;">
                        <img id="qv-img" src="" style="max-width: 100%; max-height: 100%; object-fit: contain;">
                    </div>
                    <div style="flex: 1; padding: 40px 30px; display: flex; flex-direction: column;">
                        <h2 id="qv-title" style="font-size: 1.5rem; font-weight: 800; margin-bottom: 10px; color: var(--text-color);"></h2>
                        <div id="qv-price" style="font-size: 1.8rem; font-weight: 900; color: var(--primary); margin-bottom: 20px;"></div>
                        <div style="flex: 1; border-top: 1px solid var(--border-color); padding-top: 20px;">
                            <p style="color: var(--text-gray); line-height: 1.6;">Sản phẩm Mini PC chính hãng, thiết kế nhỏ gọn, hiệu năng vượt trội. Hỗ trợ giao hàng hỏa tốc trong 2h tại nội thành.</p>
                            <div class="card-specs" style="margin-top: 20px;">
                                <span class="spec-pill">WIFI 6</span>
                                <span class="spec-pill secondary">BT 5.2</span>
                                <span class="spec-pill secondary">Type-C</span>
                            </div>
                        </div>
                        <div style="display: flex; gap: 15px; margin-top: 20px;">
                            <a href="demo_product.html" style="flex: 1; padding: 12px; background: var(--bg-gray); color: var(--text-color); border: 1px solid var(--border-color); border-radius: 8px; font-weight: bold; font-size: 1.1rem; text-align: center; text-decoration: none; transition: 0.2s;" onmouseover="this.style.background='var(--border-color)'" onmouseout="this.style.background='var(--bg-gray)'">Xem chi tiết</a>
                            <button onclick="showToast('Đã thêm vào giỏ hàng thành công!'); closeQuickView();" style="flex: 1; padding: 12px; background: var(--primary); color: white; border: none; border-radius: 8px; font-weight: bold; font-size: 1.1rem; cursor: pointer; transition: 0.2s; box-shadow: 0 4px 15px rgba(14,165,233,0.3);" onmouseover="this.style.opacity='0.9'" onmouseout="this.style.opacity='1'">Thêm vào giỏ</button>
                        </div>
                    </div>
                </div>
            </div>

            <script>
                // 1. Toast Notification System
                function showToast(message) {
                    let container = document.getElementById('toast-container');
                    if(!container) {
                        container = document.createElement('div');
                        container.id = 'toast-container';
                        document.body.appendChild(container);
                    }
                    const toast = document.createElement('div');
                    toast.className = 'nava-toast';
                    toast.innerHTML = '<i class="ph-fill ph-check-circle" style="color: var(--primary); font-size: 1.3rem;"></i> ' + message;
                    container.appendChild(toast);
                    
                    // trigger reflow
                    void toast.offsetWidth;
                    toast.classList.add('show');
                    
                    setTimeout(() => {
                        toast.classList.remove('show');
                        setTimeout(() => toast.remove(), 400);
                    }, 3000);
                }

                // 2. Interactive UX: Skeleton Loading & Filtering
                function simulateLoading() {
                    const grid = document.querySelector('.product-grid');
                    if(!grid) return;
                    grid.classList.add('grid-loading');
                    setTimeout(() => {
                        grid.classList.remove('grid-loading');
                    }, 800);
                }
                
                let originalCards = [];
                function applyFiltersAndSort() {
                    const grid = document.querySelector('.product-grid');
                    if(!grid) return;
                    
                    if(originalCards.length === 0) {
                        originalCards = Array.from(grid.querySelectorAll('.product-card'));
                    }
                    
                    grid.classList.add('grid-loading');
                    
                    setTimeout(() => {
                        const minInput = document.getElementById('priceMin');
                        const maxInput = document.getElementById('priceMax');
                        const minVal = minInput ? parseInt(minInput.value) : 0;
                        const maxVal = maxInput ? parseInt(maxInput.value) : 40000000;
                        
                        const sortLabelEl = document.getElementById('sortLabel');
                        const sortMethod = sortLabelEl ? sortLabelEl.textContent.trim() : 'Mặc định';
                        
                        let visibleCards = [];
                        
                        // Filtering
                        originalCards.forEach(card => {
                            const priceEl = card.querySelector('.card-content > div:last-child > span');
                            let price = 0;
                            if(priceEl) {
                                price = parseInt(priceEl.textContent.replace(/[^0-9]/g, '')) || 0;
                            }
                            
                            if(price >= minVal && price <= maxVal) {
                                card.style.display = 'flex';
                                visibleCards.push(card);
                            } else {
                                card.style.display = 'none';
                            }
                        });
                        
                        // Sorting
                        if(sortMethod === 'Giá tăng dần') {
                            visibleCards.sort((a, b) => {
                                const pa = parseInt(a.querySelector('.card-content > div:last-child > span').textContent.replace(/[^0-9]/g, '')) || 0;
                                const pb = parseInt(b.querySelector('.card-content > div:last-child > span').textContent.replace(/[^0-9]/g, '')) || 0;
                                return pa - pb;
                            });
                        } else if(sortMethod === 'Giá giảm dần') {
                            visibleCards.sort((a, b) => {
                                const pa = parseInt(a.querySelector('.card-content > div:last-child > span').textContent.replace(/[^0-9]/g, '')) || 0;
                                const pb = parseInt(b.querySelector('.card-content > div:last-child > span').textContent.replace(/[^0-9]/g, '')) || 0;
                                return pb - pa;
                            });
                        } else if(sortMethod === 'Mới nhất') {
                            visibleCards.reverse(); // simple mock
                        }
                        
                        // Re-append
                        grid.innerHTML = '';
                        visibleCards.forEach(card => grid.appendChild(card));
                        
                        if(visibleCards.length === 0) {
                            grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 50px; color: var(--text-gray); font-size: 1.1rem; border: 1px dashed var(--border-color); border-radius: var(--radius-lg);">Không tìm thấy sản phẩm nào trong tầm giá này.</div>';
                        }
                        
                        grid.classList.remove('grid-loading');
                    }, 400);
                }
                
                // Bind loading to sort options and brand items
                setTimeout(() => {
                    document.querySelectorAll('.sort-drop-menu a').forEach(a => {
                        const originalClick = a.onclick;
                        a.onclick = function(e) {
                            const res = originalClick ? originalClick.call(this, e) : true;
                            applyFiltersAndSort();
                            return res;
                        }
                    });
                    
                    document.querySelectorAll('.brand-item').forEach(b => {
                        b.onclick = function() { applyFiltersAndSort(); showToast('Đã lọc theo thương hiệu'); }
                    });
                }, 500);

                // 3. Quick View Modal
                function openQuickView(name, price, img) {
                    const modal = document.getElementById('quick-view-modal');
                    document.getElementById('qv-title').textContent = name;
                    document.getElementById('qv-price').textContent = price;
                    document.getElementById('qv-img').src = img;
                    
                    modal.style.display = 'flex';
                    void modal.offsetWidth;
                    modal.style.opacity = '1';
                    modal.children[0].style.transform = 'scale(1)';
                }
                function closeQuickView() {
                    const modal = document.getElementById('quick-view-modal');
                    modal.style.opacity = '0';
                    modal.children[0].style.transform = 'scale(0.95)';
                    setTimeout(() => { modal.style.display = 'none'; }, 300);
                }
                
                // Inject Quick View buttons into all product cards
                document.addEventListener('DOMContentLoaded', () => {
                    document.querySelectorAll('.product-card').forEach(card => {
                        const imgWrap = card.querySelector('.card-image-wrap');
                        const titleEl = card.querySelector('.card-title');
                        const priceEl = card.querySelector('.card-content > div:last-child > span');
                        const imgEl = card.querySelector('.product-img');
                        
                        if(imgWrap && titleEl && priceEl && imgEl) {
                            const name = titleEl.textContent.trim().replace('...', '');
                            const price = priceEl.textContent.trim();
                            const imgUrl = imgEl.src;
                            
                            // Add Quick View Button
                            const btn = document.createElement('button');
                            btn.className = 'quick-view-btn';
                            btn.title = 'Xem nhanh';
                            btn.innerHTML = '<i class="ph-bold ph-eye" style="font-size: 1.2rem;"></i>';
                            btn.onclick = function(e) {
                                e.stopPropagation();
                                e.preventDefault();
                                openQuickView(name, price, imgUrl);
                            };
                            imgWrap.appendChild(btn);
                            
                            // Add hover image (fake 2nd angle by inverting or just a slightly different mock)
                            const hoverImg = document.createElement('img');
                            hoverImg.src = imgUrl; 
                            hoverImg.className = 'product-img-hover';
                            hoverImg.style.filter = 'brightness(0.9) contrast(1.1)'; // visual distinction for demo
                            imgWrap.appendChild(hoverImg);
                            
                            // Add tooltips to spec pills
                            card.querySelectorAll('.spec-pill').forEach(pill => {
                                pill.title = 'Thông số phần cứng: ' + pill.textContent.trim();
                            });
                            
                            // Update card onclick to open Quick View
                            card.onclick = function(e) {
                                e.preventDefault();
                                openQuickView(name, price, imgUrl);
                            };
                        }
                    });
                });
                
                // 4. Mobile Off-canvas Sidebar
                function toggleMobileSidebar() {
                    document.querySelector('.nava-sidebar').classList.toggle('active');
                    document.querySelector('.sidebar-overlay').classList.toggle('active');
                }
            </script>
        </div>
    """
    full_html = clean_liquid_tags(header_part + collection_html + local_footer_part)
    
    # Inject sticky compare bar directly into the HTML
    try:
        with open(os.path.join(base_dir, "post_build.py"), "r", encoding="utf-8") as pb_file:
            pb_content = pb_file.read()
            start_idx = pb_content.find('sticky_html = """') + len('sticky_html = """')
            end_idx = pb_content.find('"""\n\nfile_path')
            if start_idx != -1 and end_idx != -1:
                sticky_html = pb_content[start_idx:end_idx]
                if "<!-- Sticky Compare Bar -->" not in full_html:
                    if "</body>" in full_html:
                        full_html = full_html.replace("</body>", sticky_html + "\n</body>")
                    else:
                        full_html += sticky_html
    except Exception as e:
        print("Failed to inject sticky compare bar:", e)
        
    # Remove any surrogate characters that may come from theme files
    full_html = full_html.encode('utf-8', errors='replace').decode('utf-8', errors='replace')
    with open(os.path.join(base_dir, "demo_collection.html"), "w", encoding="utf-8") as f:
        f.write(full_html)


def build_product(base_dir, header_part, footer_part):
    # Extract sticky stuff from index.bwt
    sticky_stuff = ""
    with open(os.path.join(base_dir, "index.bwt"), "r", encoding="utf-8") as f:
        idx_content = f.read()
        if "<!-- Mobile Sidebar Drawer -->" in idx_content:
            sticky_stuff = idx_content[idx_content.find("<!-- Mobile Sidebar Drawer -->"):]
            if "<!-- /MASTER SAPO ESCAPE WRAPPER -->" in sticky_stuff:
                sticky_stuff = sticky_stuff.split("<!-- /MASTER SAPO ESCAPE WRAPPER -->")[0]
                
    local_footer_part = sticky_stuff + '<script src="https://nava-one.vercel.app/assets/main.js" defer></script>\n' + footer_part

    product_html = """
        <div class="container" style="max-width: 1600px !important; margin: 0 auto !important; padding: 40px 15px; margin-top: 100px;">
            <div class="breadcrumb" style="background: transparent; padding: 0; margin-bottom: 25px;">
                <a href="/" style="color: var(--text-gray); text-decoration: none;"><i class="ph ph-house"></i> Trang chủ</a> 
                <span style="margin: 0 10px; color: var(--text-gray);">/</span> 
                <a href="demo_collection.html" style="color: var(--text-gray); text-decoration: none;">DOCK eGPU</a>
                <span style="margin: 0 10px; color: var(--text-gray);">/</span> 
                <span style="color: var(--primary); font-weight: bold;">EGPU MINISFORUM DEG1 Oculink</span>
            </div>
            
            <style>
                .nava-product-layout { display: flex; flex-direction: column; gap: 40px; }
                .nava-prod-gallery { width: 100%; }
                .nava-prod-info { width: 100%; }
                @media (min-width: 992px) {
                    .nava-product-layout { flex-direction: row; align-items: flex-start; }
                    .nava-prod-gallery { width: 45%; flex-shrink: 0; position: sticky; top: 100px; }
                    .nava-prod-info { width: 55%; flex-shrink: 0; padding-left: 20px; }
                }
            </style>
            <div class="nava-product-layout" style="background: var(--bg-white); border-radius: var(--radius-lg); border: 1px solid var(--border-color); padding: 35px; margin-bottom: 40px; box-shadow: var(--shadow-sm);">
                <!-- Product Gallery -->
                <div class="nava-prod-gallery">
                    <div class="main-image" style="border: 1px solid var(--border-color); border-radius: var(--radius-lg); padding: 50px; text-align: center; margin-bottom: 20px; background: var(--bg-gray); position: relative; overflow: hidden; cursor: zoom-in;">
                        <span class="badge" style="position: absolute; top: 20px; left: 20px; background: #ef4444; color: white; padding: 6px 12px; border-radius: 8px; font-size: 0.85rem; font-weight: 800; z-index: 2; box-shadow: 0 4px 10px rgba(239, 68, 68, 0.3);">MỚI NHẤT</span>
                        <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" alt="MINISFORUM DEG1" style="max-width: 85%; height: auto; transition: transform 0.4s ease;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                    </div>
                    <div class="thumbnail-list" style="display: flex; gap: 15px; overflow-x: auto; padding-bottom: 10px; scrollbar-width: none;">
                        <div style="width: 85px; height: 85px; border: 2px solid var(--primary); border-radius: var(--radius-md); padding: 10px; background: var(--bg-gray); cursor: pointer; flex-shrink: 0;">
                            <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" style="width: 100%; height: 100%; object-fit: contain;">
                        </div>
                        <div style="width: 85px; height: 85px; border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 10px; background: var(--bg-gray); cursor: pointer; flex-shrink: 0; opacity: 0.7; transition: all 0.3s;" onmouseover="this.style.opacity='1'">
                            <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" style="width: 100%; height: 100%; object-fit: contain;">
                        </div>
                        <div style="width: 85px; height: 85px; border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 10px; background: var(--bg-gray); cursor: pointer; flex-shrink: 0; opacity: 0.7; transition: all 0.3s;" onmouseover="this.style.opacity='1'">
                            <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" style="width: 100%; height: 100%; object-fit: contain;">
                        </div>
                    </div>
                </div>
                
                <!-- Product Info -->
                <div class="nava-prod-info">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                        <span style="font-size: 0.85rem; font-weight: 700; color: var(--text-gray); text-transform: uppercase; letter-spacing: 1px;">Minisforum</span>
                        <span style="width: 4px; height: 4px; background: var(--text-gray); border-radius: 50%;"></span>
                        <span style="font-size: 0.85rem; font-weight: 600; color: #10b981; display: flex; align-items: center; gap: 4px;"><i class="ph-fill ph-check-circle"></i> Tình trạng: Còn hàng</span>
                    </div>
                    
                    <h1 style="font-size: 2.2rem; font-weight: 800; margin-bottom: 15px; line-height: 1.3; color: var(--text-color);">EGPU MINISFORUM DEG1 Oculink - Hàng chính hãng MinisForum</h1>
                    
                    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 25px; color: var(--text-gray); font-size: 0.95rem;">
                        <span style="display: flex; align-items: center; gap: 5px;"><i class="ph-fill ph-star" style="color: #f59e0b; font-size: 1.1rem;"></i> <strong style="color: var(--text-color);">4.9</strong> (152 Đánh giá)</span>
                        <span style="width: 1px; height: 15px; background: var(--border-color);"></span>
                        <span>Đã bán: <strong style="color: var(--text-color);">340+</strong></span>
                        <span style="width: 1px; height: 15px; background: var(--border-color);"></span>
                        <span style="cursor: pointer; color: var(--primary); font-weight: 600;"><i class="ph ph-share-network"></i> Chia sẻ</span>
                    </div>
                    
                    <div class="price-box" style="background: linear-gradient(90deg, rgba(14,165,233,0.05) 0%, transparent 100%); border-left: 4px solid var(--primary); padding: 20px 25px; border-radius: 0 var(--radius-md) var(--radius-md) 0; margin-bottom: 30px;">
                        <div style="color: var(--primary); font-weight: 900; font-size: 2.5rem; line-height: 1; margin-bottom: 5px;">2.490.000₫</div>
                        <div style="color: var(--text-gray); font-size: 1rem;">Cam kết chính hãng 100%. Đã bao gồm VAT.</div>
                    </div>
                    
                    <div style="margin-bottom: 30px; font-size: 0.95rem; line-height: 1.6; color: var(--text-color);">
                        <ul style="padding-left: 20px; margin: 0; color: var(--text-color);">
                            <li style="margin-bottom: 8px;"><strong>Kết Nối OCuLink Hiệu Suất Cao:</strong> PCIe 4.0 x4, băng thông 64 GB/s.</li>
                            <li style="margin-bottom: 8px;"><strong>Thiết Kế Mở Linh Hoạt:</strong> Hỗ trợ các card đồ họa lớn như RTX 4090 / RX 7900 XTX.</li>
                            <li style="margin-bottom: 8px;"><strong>Tương Thích Nguồn ATX/SFX:</strong> Đảm bảo điện năng cho VGA cao cấp.</li>
                        </ul>
                    </div>
                    
                    <hr style="border: 0; border-top: 1px solid var(--border-color); margin: 30px 0;">
                    
                    <div class="quantity-add" style="display: flex; gap: 15px; margin-bottom: 25px;">
                        <div style="display: flex; border: 1px solid var(--border-color); border-radius: var(--radius-md); overflow: hidden; background: var(--bg-gray);">
                            <button style="width: 45px; height: 50px; background: transparent; border: none; cursor: pointer; font-size: 1.2rem; transition: background 0.2s;" onmouseover="this.style.background='rgba(0,0,0,0.05)'" onmouseout="this.style.background='transparent'">-</button>
                            <input type="text" value="1" style="width: 60px; height: 50px; border: none; text-align: center; font-weight: bold; background: var(--bg-white); color: var(--text-color); font-size: 1.1rem; border-left: 1px solid var(--border-color); border-right: 1px solid var(--border-color);">
                            <button style="width: 45px; height: 50px; background: transparent; border: none; cursor: pointer; font-size: 1.2rem; transition: background 0.2s;" onmouseover="this.style.background='rgba(0,0,0,0.05)'" onmouseout="this.style.background='transparent'">+</button>
                        </div>
                        <button class="btn-pill" style="flex: 1; border-radius: var(--radius-md); font-size: 1.1rem; display: flex; justify-content: center; align-items: center; gap: 10px; background: rgba(14, 165, 233, 0.1); color: var(--primary); border: 2px solid var(--primary); font-weight: bold; cursor: pointer; transition: all 0.3s;" onmouseover="this.style.background='var(--primary)'; this.style.color='white';" onmouseout="this.style.background='rgba(14, 165, 233, 0.1)'; this.style.color='var(--primary)';">
                            <i class="ph ph-shopping-cart-simple" style="font-size: 1.3rem;"></i> THÊM VÀO GIỎ
                        </button>
                    </div>
                    
                    <button class="btn-pill btn-blue" style="width: 100%; border-radius: var(--radius-md); padding: 16px; font-weight: bold; font-size: 1.2rem; margin-bottom: 30px; cursor: pointer; box-shadow: 0 8px 20px rgba(14, 165, 233, 0.3);">
                        MUA NGAY <br> <span style="font-size: 0.9rem; font-weight: normal; opacity: 0.9;">Giao hàng tận nơi hoặc nhận tại cửa hàng</span>
                    </button>
                    
                    <!-- Policy Grid -->
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; padding: 20px; border-radius: var(--radius-lg); border: 1px dashed var(--border-color); background: var(--bg-gray);">
                        <div style="display: flex; align-items: flex-start; gap: 12px;">
                            <i class="ph-fill ph-shield-check" style="font-size: 28px; color: var(--primary);"></i>
                            <div>
                                <div style="font-weight: 700; font-size: 0.95rem; margin-bottom: 4px; color: var(--text-color);">Bảo hành chính hãng</div>
                                <div style="font-size: 0.85rem; color: var(--text-gray);">12 tháng tại các trung tâm</div>
                            </div>
                        </div>
                        <div style="display: flex; align-items: flex-start; gap: 12px;">
                            <i class="ph-fill ph-rocket" style="font-size: 28px; color: var(--primary);"></i>
                            <div>
                                <div style="font-weight: 700; font-size: 0.95rem; margin-bottom: 4px; color: var(--text-color);">Giao hàng hỏa tốc</div>
                                <div style="font-size: 0.85rem; color: var(--text-gray);">Trong vòng 2h tại TP.HCM & HN</div>
                            </div>
                        </div>
                        <div style="display: flex; align-items: flex-start; gap: 12px;">
                            <i class="ph-fill ph-arrows-left-right" style="font-size: 28px; color: var(--primary);"></i>
                            <div>
                                <div style="font-weight: 700; font-size: 0.95rem; margin-bottom: 4px; color: var(--text-color);">1 đổi 1 miễn phí</div>
                                <div style="font-size: 0.85rem; color: var(--text-gray);">Trong 30 ngày nếu lỗi NSX</div>
                            </div>
                        </div>
                        <div style="display: flex; align-items: flex-start; gap: 12px;">
                            <i class="ph-fill ph-headset" style="font-size: 28px; color: var(--primary);"></i>
                            <div>
                                <div style="font-weight: 700; font-size: 0.95rem; margin-bottom: 4px; color: var(--text-color);">Hỗ trợ kỹ thuật</div>
                                <div style="font-size: 0.85rem; color: var(--text-gray);">Giải đáp nhanh chóng trọn đời</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Product Tabs -->
            <div style="margin-bottom: 60px; width: 100%;">
                <div>
                    <div style="background: var(--bg-white); border-radius: var(--radius-lg); border: 1px solid var(--border-color); overflow: hidden; box-shadow: var(--shadow-sm);">
                        <div style="display: flex; border-bottom: 1px solid var(--border-color); background: var(--bg-gray); overflow-x: auto; scrollbar-width: none;">
                            <button style="padding: 20px 30px; background: var(--bg-white); border: none; border-bottom: 3px solid var(--primary); color: var(--primary); font-weight: 800; font-size: 1.1rem; cursor: pointer; white-space: nowrap;">Mô Tả Sản Phẩm</button>
                            <button style="padding: 20px 30px; background: transparent; border: none; border-bottom: 3px solid transparent; color: var(--text-gray); font-weight: 600; font-size: 1.1rem; cursor: pointer; white-space: nowrap; transition: color 0.3s;" onmouseover="this.style.color='var(--text-color)'" onmouseout="this.style.color='var(--text-gray)'">Thông Số Kỹ Thuật</button>
                            <button style="padding: 20px 30px; background: transparent; border: none; border-bottom: 3px solid transparent; color: var(--text-gray); font-weight: 600; font-size: 1.1rem; cursor: pointer; white-space: nowrap; transition: color 0.3s;" onmouseover="this.style.color='var(--text-color)'" onmouseout="this.style.color='var(--text-gray)'">Video Đánh Giá</button>
                            <button style="padding: 20px 30px; background: transparent; border: none; border-bottom: 3px solid transparent; color: var(--text-gray); font-weight: 600; font-size: 1.1rem; cursor: pointer; white-space: nowrap; transition: color 0.3s;" onmouseover="this.style.color='var(--text-color)'" onmouseout="this.style.color='var(--text-gray)'">Bình Luận (152)</button>
                        </div>
                        <div style="padding: 40px; font-size: 1.05rem; line-height: 1.8; color: var(--text-color);">
                            <h3 style="font-weight: 800; margin-bottom: 20px; font-size: 1.5rem;">Thông tin chi tiết</h3>
                            <p style="margin-bottom: 20px;">MINISFORUM DEG1 Oculink eGPU Dock là giải pháp mở rộng đồ họa hiệu suất cao, giúp nâng cấp khả năng xử lý đồ họa cho các thiết bị như laptop siêu mỏng và mini PC. Với thiết kế mở và giao diện OCuLink, sản phẩm này mang lại băng thông truyền tải cao, đáp ứng nhu cầu chơi game và xử lý đồ họa chuyên nghiệp.</p>
                            
                            <h3 style="font-weight: 800; margin-top: 40px; margin-bottom: 20px; font-size: 1.5rem;">Đặc Điểm Nổi Bật</h3>
                            <ul style="padding-left: 20px;">
                                <li style="margin-bottom: 15px;"><strong>Kết Nối OCuLink Hiệu Suất Cao:</strong> Sử dụng giao diện OCuLink (PCIe 4.0 x4), DEG1 cung cấp băng thông truyền tải dữ liệu lên đến 64 GB/s, vượt trội so với các dock eGPU sử dụng Thunderbolt 3.</li>
                                <li style="margin-bottom: 15px;"><strong>Thiết Kế Mở Linh Hoạt:</strong> Với thiết kế mở, DEG1 hỗ trợ các card đồ họa có kích thước khác nhau, bao gồm cả NVIDIA GeForce RTX 4090 và AMD Radeon RX 7900 XTX, giúp người dùng dễ dàng nâng cấp theo nhu cầu.</li>
                                <li style="margin-bottom: 15px;"><strong>Tương Thích Nguồn ATX/SFX:</strong> Hỗ trợ cả nguồn ATX và SFX, người dùng có thể lựa chọn nguồn phù hợp với hệ thống của mình, đảm bảo cung cấp đủ điện năng cho các card đồ họa cao cấp.</li>
                                <li style="margin-bottom: 15px;"><strong>Kết Nối Đa Dạng:</strong> Trang bị cổng PCIe x16 (PCIe 4.0 x4) cho phép kết nối linh hoạt với nhiều loại card đồ họa, mở rộng khả năng xử lý đồ họa cho hệ thống.</li>
                            </ul>
                            
                            <h3 style="font-weight: 800; margin-top: 40px; margin-bottom: 20px; font-size: 1.5rem;">Lưu Ý Khi Sử Dụng</h3>
                            <ul style="padding-left: 20px;">
                                <li style="margin-bottom: 15px;"><strong>Không Hỗ Trợ Hot-Plugging:</strong> Giao diện OCuLink không hỗ trợ cắm nóng; cần tắt cả dock và máy tính trước khi kết nối hoặc ngắt kết nối để tránh hư hỏng.</li>
                                <li style="margin-bottom: 15px;"><strong>Khóa Cố Định Cổng Kết Nối:</strong> Cổng OCuLink có cơ chế khóa; cần nhấn nút mở khóa trước khi rút cáp để tránh gây hỏng cổng kết nối.</li>
                                <li style="margin-bottom: 15px;"><strong>Tính Năng Khởi Động Đồng Thời:</strong> Chức năng khởi động đồng thời chỉ tương thích với các mini PC của MINISFORUM và yêu cầu sử dụng dây cáp chính hãng.</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Sticky Add to Cart (Hidden by default, shown on scroll in JS) -->
            <div id="sticky-cart-bar" style="position: fixed; bottom: 0; left: 0; width: 100%; background: var(--bg-white); box-shadow: 0 -10px 30px rgba(0,0,0,0.1); padding: 15px 0; z-index: 1000; transform: translateY(100%); transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); border-top: 1px solid var(--border-color);">
                <div class="container" style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 20px;">
                        <div style="width: 60px; height: 60px; background: var(--bg-gray); border-radius: var(--radius-sm); border: 1px solid var(--border-color); padding: 5px;">
                            <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" style="width: 100%; height: 100%; object-fit: contain;">
                        </div>
                        <div style="display: none; @media (min-width: 768px) { display: block; }">
                            <div style="font-weight: 700; font-size: 1.1rem; color: var(--text-color); margin-bottom: 4px;">EGPU MINISFORUM DEG1 Oculink</div>
                            <div style="color: var(--primary); font-weight: 900; font-size: 1.2rem;">2.490.000₫</div>
                        </div>
                    </div>
                    <div style="display: flex; gap: 15px; align-items: center;">
                        <div class="d-none d-md-flex" style="align-items: center; gap: 10px; margin-right: 15px;">
                            <span style="font-weight: 600; color: var(--text-gray); font-size: 0.9rem;">Số lượng:</span>
                            <div style="display: flex; border: 1px solid var(--border-color); border-radius: var(--radius-sm); overflow: hidden; height: 40px;">
                                <button style="width: 30px; background: var(--bg-gray); border: none; cursor: pointer; font-weight: bold;">-</button>
                                <input type="text" value="1" style="width: 40px; border: none; text-align: center; font-weight: bold; background: var(--bg-white); color: var(--text-color);">
                                <button style="width: 30px; background: var(--bg-gray); border: none; cursor: pointer; font-weight: bold;">+</button>
                            </div>
                        </div>
                        <button class="btn-pill" style="padding: 12px 24px; border-radius: var(--radius-sm); border: 2px solid var(--primary); color: var(--primary); background: transparent; font-weight: bold; cursor: pointer; transition: all 0.3s;" onmouseover="this.style.background='var(--primary)'; this.style.color='white';" onmouseout="this.style.background='transparent'; this.style.color='var(--primary)';">Thêm vào giỏ</button>
                        <button class="btn-pill btn-blue" style="padding: 12px 30px; border-radius: var(--radius-sm); font-weight: bold; font-size: 1.05rem; box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3);">Mua ngay</button>
                    </div>
                </div>
            </div>
            
            <script>
                // Show sticky bar on scroll
                window.addEventListener('scroll', function() {
                    const stickyBar = document.getElementById('sticky-cart-bar');
                    if (window.scrollY > 500) {
                        stickyBar.style.transform = 'translateY(0)';
                    } else {
                        stickyBar.style.transform = 'translateY(100%)';
                    }
                });
            </script>
        </div>
    """
    full_html = clean_liquid_tags(header_part + product_html + footer_part)
    with open(os.path.join(base_dir, "demo_product.html"), "w", encoding="utf-8") as f:
        f.write(full_html)

def build_all():
    base_dir = r"F:\BAO_SAPO\sapo_new"
    header_part, footer_part = get_core_layout(base_dir)
    
    build_index(base_dir, header_part, footer_part)
    print("Generated index.html successfully!")
    
    build_collection(base_dir, header_part, footer_part)
    print("Generated demo_collection.html successfully!")
    
    build_product(base_dir, header_part, footer_part)
    print("Generated demo_product.html successfully!")

if __name__ == "__main__":
    build_all()
