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
    
    # Intercept Auth Links for Demo Environment
    demo_auth_interceptor = """
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Hijack login and register links to point to local demo HTMLs
            const authLinks = document.querySelectorAll('a[href^="/account/login"], a[href^="/account/register"]');
            authLinks.forEach(link => {
                link.addEventListener('click', function(e) {
                    e.preventDefault();
                    if (this.getAttribute('href').includes('login')) {
                        window.location.href = 'demo_login.html';
                    } else if (this.getAttribute('href').includes('register')) {
                        window.location.href = 'demo_register.html';
                    }
                });
            });
        });
    </script>
    """
    footer_part += demo_auth_interceptor
    
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
                
    local_footer_part = sticky_stuff + '<script src="assets/main.js" defer></script>\n' + footer_part

    collection_html = """
        <div class="container" id="nava-col-container" style="max-width: 1600px !important; width: 100% !important; box-sizing: border-box !important; margin: 0 auto !important; padding: 30px 30px 80px;">
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
                    <h1 style="font-size: 2.5rem; font-weight: 900; margin-bottom: 12px; color: var(--text-dark); letter-spacing: -0.5px;">Mini PC ASUS NUC Chính Hãng</h1>
                    <p style="color: var(--text-gray); max-width: 650px; font-size: 1.05rem; margin: 0; line-height: 1.6;">Là đối tác Gold Partner của ASUS, NAVA Store tự hào cung cấp các dòng sản phẩm ASUS NUC với chất lượng dịch vụ bảo hành cao cấp nhất.</p>
                </div>
                <div style="position: relative; z-index: 2; opacity: 0.9;" class="hero-image-wrap">
                    <img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/asus.png" alt="ASUS" style="max-width: 250px; max-height: 80px; object-fit: contain; filter: drop-shadow(0 10px 20px rgba(14,165,233,0.2));">
                </div>
            </div>

            <style>
                /* Layout */
                .nava-collection-layout { display: flex; flex-direction: column; gap: 40px; }
                .nava-sidebar { width: 100%; }
                .nava-main { width: 100%; min-width: 0; }
                
                .sidebar-block { margin-bottom: 35px; }
                .sidebar-title { font-weight: 800; font-size: 1.1rem; text-transform: uppercase; margin-bottom: 20px; color: var(--text-dark); display: flex; align-items: center; gap: 10px; }
                .sidebar-title::before { content: ''; display: block; width: 4px; height: 18px; background: var(--primary); border-radius: 2px; }
                
                .category-list { list-style: none; padding: 0; margin: 0; }
                .category-list li { margin-bottom: 10px; }
                .category-list a { display: flex; align-items: center; gap: 10px; color: var(--text-dark); text-decoration: none; font-weight: 600; font-size: 0.95rem; transition: all 0.3s; padding: 8px 12px; border-radius: var(--radius-sm); }
                .category-list a:hover, .category-list a.active { color: var(--primary); background: rgba(14, 165, 233, 0.05); padding-left: 15px; }
                .category-list a img { flex-shrink: 0; }
                .category-list .count { margin-left: auto; background: var(--bg-gray); padding: 2px 8px; border-radius: 10px; font-size: 0.8rem; color: var(--text-gray); display: flex; align-items: center; gap: 4px; }
                
                .price-filter-inputs { display: flex; gap: 10px; margin-bottom: 15px; }
                .price-filter-inputs input { width: 50%; padding: 12px; border-radius: var(--radius-sm); border: 1px solid var(--border-color); background: transparent; color: var(--text-dark); font-size: 0.9rem; transition: border-color 0.3s; }
                .price-filter-inputs input:focus { border-color: var(--primary); outline: none; }
                
                .brand-list { display: flex; flex-wrap: wrap; gap: 8px; width: 100%; box-sizing: border-box; }
                .brand-item { width: calc(50% - 4px); display: flex; align-items: center; justify-content: center; padding: 6px; border: 1px solid var(--border-color); border-radius: var(--radius-sm); cursor: pointer; transition: all 0.3s; background: transparent; height: 48px; box-sizing: border-box; }
                .brand-item img { max-height: 20px; max-width: 85%; width: auto; object-fit: contain; filter: grayscale(100%) brightness(1.5); opacity: 0.7; transition: all 0.3s; }
                .brand-item:hover { border-color: var(--primary); background: rgba(14, 165, 233, 0.05); }
                .brand-item:hover img { filter: grayscale(0%) brightness(1); opacity: 1; }
                
                .sort-bar { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; margin-bottom: 30px; background: var(--bg-white); padding: 15px 20px; border-radius: var(--radius-lg); border: 1px solid var(--border-color); box-shadow: var(--shadow-sm); }
                .sort-label { font-weight: 700; margin-right: 10px; color: var(--text-dark); }
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
                .nava-toast { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border: 1px solid var(--border-color); border-left: 4px solid var(--primary); padding: 15px 20px; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); color: var(--text-dark); font-weight: 600; font-size: 0.95rem; display: flex; align-items: center; gap: 12px; transform: translateX(120%); opacity: 0; transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55); }
                .nava-toast.show { transform: translateX(0); opacity: 1; }
                
                .quick-view-btn { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -30%); opacity: 0; visibility: hidden; background: rgba(255, 255, 255, 0.4); backdrop-filter: blur(4px); border: 1px solid rgba(255,255,255,0.6); color: var(--text-dark); width: 45px; height: 45px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.3s; z-index: 10; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
                .product-card:hover .quick-view-btn { opacity: 1; visibility: visible; transform: translate(-50%, -50%); }
                .quick-view-btn:hover { background: rgba(255, 255, 255, 0.8); }
                
                .product-img { transition: opacity 0.4s; }
                .product-img-hover { position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: contain; opacity: 0; transition: opacity 0.4s; z-index: 1; }
                .product-card:hover .product-img { opacity: 0; }
                .product-card:hover .product-img-hover { opacity: 1; }
                
                .mobile-filter-btn { display: none; position: fixed; bottom: 85px; right: 20px; background: var(--primary); color: white; border: none; width: 50px; height: 50px; border-radius: 50%; z-index: 90; box-shadow: 0 5px 20px rgba(14,165,233,0.4); justify-content: center; align-items: center; cursor: pointer; transition: transform 0.2s; }
                .mobile-filter-btn:active { transform: scale(0.95); }
                
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
                    #nava-col-container { margin-top: 0 !important; padding-top: 25px !important; }
                    .hero-image-wrap { display: none; }
                    .collection-hero { flex-direction: column !important; align-items: flex-start !important; padding: 25px 20px !important; text-align: left; }
                    .collection-hero h1 { font-size: 1.8rem !important; }
                    .collection-hero p { font-size: 0.95rem !important; }
                    
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
                
                @media (max-width: 575px) {
                    #nava-col-container { padding: 10px 10px 80px !important; margin-top: 0 !important; }
                    .product-grid { display: grid !important; grid-template-columns: repeat(2, minmax(0, 1fr)) !important; gap: 8px !important; }
                    /* Filter icon only */
                    #sortLabel, #sortToggleBtn .ph-caret-down { display: none !important; }
                    #sortToggleBtn { width: 44px; height: 44px; padding: 0 !important; display: flex; justify-content: center; align-items: center; border-radius: 12px; }
                    #sortToggleBtn > i:first-child { font-size: 1.4rem !important; margin: 0 !important; }
                    .ai-btn { padding: 8px 12px !important; }
                    .product-card { padding: 10px !important; min-width: 0; }
                    .card-title { font-size: 0.85rem !important; height: auto !important; max-height: 36px !important; margin-bottom: 6px !important; }
                    .card-specs { gap: 4px !important; margin-bottom: 8px !important; }
                    .spec-pill { padding: 2px 4px !important; font-size: 0.6rem !important; }
                    /* Force the price row to wrap properly on very small screens */
                    .product-card > .card-content > div:last-child { flex-direction: column !important; align-items: flex-start !important; gap: 6px !important; }
                    .product-card > .card-content > div:last-child span { font-size: 0.95rem !important; }
                    .product-card > .card-content > div:last-child a { padding: 6px 10px !important; font-size: 0.75rem !important; width: 100%; box-sizing: border-box; justify-content: center; }
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
                                    <input type="text" id="priceInputMin" value="4.000.000đ" readonly style="flex: 1; min-width: 0; padding: 8px 4px; border: 1px solid var(--border-color); border-radius: 6px; font-size: 0.85rem; color: var(--text-dark); font-weight: 700; text-align: center; outline: none; box-shadow: inset 0 1px 2px rgba(0,0,0,0.02); background: var(--bg-gray);">
                                    <span style="color: var(--text-gray); flex-shrink: 0; font-weight: bold;">-</span>
                                    <input type="text" id="priceInputMax" value="30.000.000đ" readonly style="flex: 1; min-width: 0; padding: 8px 4px; border: 1px solid var(--border-color); border-radius: 6px; font-size: 0.85rem; color: var(--text-dark); font-weight: 700; text-align: center; outline: none; box-shadow: inset 0 1px 2px rgba(0,0,0,0.02); background: var(--bg-gray);">
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
                            <button class="sort-pill-btn" id="sortToggleBtn" onclick="document.getElementById('sortDropMenu').classList.toggle('show')" style="display: flex; align-items: center;">
                                <i class="ph ph-faders" style="color: var(--primary); margin-right: 6px;"></i>
                                <span id="sortLabel">Mặc định</span>
                                <i class="ph ph-caret-down" style="color:#94a3b8; font-size:0.85rem; margin-left: 6px;"></i>
                            </button>
                            <div class="sort-drop-menu" id="sortDropMenu">
                                <a href="#" onclick="document.getElementById('sortLabel').textContent='Mặc định'; document.getElementById('sortDropMenu').classList.remove('show'); return false;"><i class="ph ph-list-dashes" style="margin-right:8px; font-size: 1.1em; vertical-align: middle;"></i> Mặc định</a>
                                <a href="#" onclick="document.getElementById('sortLabel').textContent='Giá tăng dần'; document.getElementById('sortDropMenu').classList.remove('show'); return false;"><i class="ph ph-sort-ascending" style="margin-right:8px; font-size: 1.1em; vertical-align: middle;"></i> Giá tăng dần</a>
                                <a href="#" onclick="document.getElementById('sortLabel').textContent='Giá giảm dần'; document.getElementById('sortDropMenu').classList.remove('show'); return false;"><i class="ph ph-sort-descending" style="margin-right:8px; font-size: 1.1em; vertical-align: middle;"></i> Giá giảm dần</a>
                                <a href="#" onclick="document.getElementById('sortLabel').textContent='Mới nhất'; document.getElementById('sortDropMenu').classList.remove('show'); return false;"><i class="ph ph-sparkle" style="margin-right:8px; font-size: 1.1em; vertical-align: middle;"></i> Mới nhất</a>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Quick Filter Pills -->
                    <div class="quick-filters" style="display: flex; gap: 8px; overflow-x: auto; padding-bottom: 8px; scrollbar-width: none; margin-bottom: 25px; -webkit-overflow-scrolling: touch;">
                        <style>.quick-filters::-webkit-scrollbar { display: none; }</style>
                        <button style="white-space: nowrap; padding: 6px 14px; border-radius: 20px; border: 1px solid var(--primary); background: var(--primary); color: white; font-weight: 600; font-size: 0.85rem; cursor: pointer;">Tất cả</button>
                        <button style="white-space: nowrap; padding: 6px 14px; border-radius: 20px; border: 1px solid var(--border-color); background: var(--bg-white); color: var(--text-dark); font-weight: 600; font-size: 0.85rem; cursor: pointer; transition: 0.2s;" onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border-color)'">Dưới 10 triệu</button>
                        <button style="white-space: nowrap; padding: 6px 14px; border-radius: 20px; border: 1px solid var(--border-color); background: var(--bg-white); color: var(--text-dark); font-weight: 600; font-size: 0.85rem; cursor: pointer; transition: 0.2s;" onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border-color)'">Core Ultra 9</button>
                        <button style="white-space: nowrap; padding: 6px 14px; border-radius: 20px; border: 1px solid var(--border-color); background: var(--bg-white); color: var(--text-dark); font-weight: 600; font-size: 0.85rem; cursor: pointer; transition: 0.2s;" onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border-color)'">Ryzen AI 9</button>
                        <button style="white-space: nowrap; padding: 6px 14px; border-radius: 20px; border: 1px solid var(--border-color); background: var(--bg-white); color: var(--text-dark); font-weight: 600; font-size: 0.85rem; cursor: pointer; transition: 0.2s;" onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border-color)'">RAM 32GB</button>
                        <button style="white-space: nowrap; padding: 6px 14px; border-radius: 20px; border: 1px solid var(--border-color); background: var(--bg-white); color: var(--text-dark); font-weight: 600; font-size: 0.85rem; cursor: pointer; transition: 0.2s;" onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border-color)'">Máy bộ eGPU</button>
                    </div>
                    
                    <!-- Featured Products -->
                    <div class="featured-section" style="display: none; margin-bottom: 40px;">
                        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px;">
                            <h3 style="margin: 0; font-size: 1.25rem; font-weight: 800; color: var(--text-dark); display: flex; align-items: center; gap: 8px;">
                                <i class="ph-fill ph-star" style="color: var(--primary); font-size: 1.4rem;"></i> Nổi bật nhất
                            </h3>
                        </div>
                        <div class="featured-grid" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;">
                            
                            <div class="product-card" style="margin:0; display: flex; align-items: center; padding: 15px; gap: 15px;" onclick="window.location.href='demo_product.html'">
                                <div style="width: 90px; height: 90px; flex-shrink: 0; position: relative;">
                                    <button class="compare-btn" data-name="ASUS NUC 14 Essential" title="Thêm vào so sánh" style="position: absolute; top: -5px; right: -5px; width: 28px; height: 28px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'ASUS NUC 14 Essential', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png', '4.490.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right" style="font-size: 0.8rem;"></i></button>
                                
                                    <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" alt="Featured" style="width: 100%; height: 100%; object-fit: contain;">
                                </div>
                                <div style="flex: 1; min-width: 0;">
                                    <span class="spec-pill" style="margin-bottom: 8px;">HOT SALE</span>
                                    <h4 style="margin: 0 0 6px 0; font-size: 0.95rem; font-weight: 700; color: var(--text-dark); display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; line-height: 1.4;">ASUS NUC 14 Essential</h4>
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.1rem;">4.490.000₫</span>
                                </div>
                            </div>
                            
                            <div class="product-card" style="margin:0; display: flex; align-items: center; padding: 15px; gap: 15px;" onclick="window.location.href='demo_product.html'">
                                <div style="width: 90px; height: 90px; flex-shrink: 0; position: relative;">
                                    <button class="compare-btn" data-name="AtomMan G7 PT Mini PC" title="Thêm vào so sánh" style="position: absolute; top: -5px; right: -5px; width: 28px; height: 28px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'AtomMan G7 PT Mini PC', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png', '34.490.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right" style="font-size: 0.8rem;"></i></button>
                                
                                    <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" alt="Featured" style="width: 100%; height: 100%; object-fit: contain;">
                                </div>
                                <div style="flex: 1; min-width: 0;">
                                    <span class="spec-pill" style="margin-bottom: 8px;">BÁN CHẠY</span>
                                    <h4 style="margin: 0 0 6px 0; font-size: 0.95rem; font-weight: 700; color: var(--text-dark); display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; line-height: 1.4;">AtomMan G7 PT Mini PC</h4>
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.1rem;">34.490.000₫</span>
                                </div>
                            </div>
                            
                            <div class="product-card" style="margin:0; display: flex; align-items: center; padding: 15px; gap: 15px;" onclick="window.location.href='demo_product.html'">
                                <div style="width: 90px; height: 90px; flex-shrink: 0; position: relative;">
                                    <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_1.png" alt="Featured" style="width: 100%; height: 100%; object-fit: contain;">
                                </div>
                                <div style="flex: 1; min-width: 0;">
                                    <span class="spec-pill" style="margin-bottom: 8px;">MỚI RA MẮT</span>
                                    <h4 style="margin: 0 0 6px 0; font-size: 0.95rem; font-weight: 700; color: var(--text-dark); display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; line-height: 1.4;">GMK EVO X1 32G</h4>
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.1rem;">31.190.000₫</span>
                                </div>
                            </div>
                            
                        </div>
                        <style>
                            @media (max-width: 1399px) { .featured-grid { grid-template-columns: repeat(2, 1fr) !important; } }
                            @media (max-width: 768px) { .featured-grid { grid-template-columns: 1fr !important; } }
                        </style>
                    </div>
                    
                    <!-- Product Grid (4 columns) -->
                    <div class="product-grid" style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; width: 100%; box-sizing: border-box;">
                        
                        <!-- Product 1 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="ASUS NUC 14 Essential Int" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'ASUS NUC 14 Essential Int', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png', '4.490.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
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
                                
                                <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">4.490.000₫</span>
                                    <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                                </div>
                            </div>
                        </div>

                        <!-- Product 2 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="AtomMan G7 PT Mini PC" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'AtomMan G7 PT Mini PC', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png', '34.490.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
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
                                
                                <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">34.490.000₫</span>
                                    <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                                </div>
                            </div>
                        </div>

                        <!-- Product 3 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="Mini PC GMK EVO X1 32G" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'Mini PC GMK EVO X1 32G', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_1.png', '31.190.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
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
                                
                                <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">31.190.000₫</span>
                                    <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                                </div>
                            </div>
                        </div>

                        <!-- Product 4 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="Tablet Minisforum V3 SE" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'Tablet Minisforum V3 SE', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_2.png', '23.090.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
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
                                
                                <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">23.090.000₫</span>
                                    <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Product 5 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="Beelink SER8 AMD 884" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'Beelink SER8 AMD 884', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_2.png', '11.990.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
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
                                
                                <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">11.990.000₫</span>
                                    <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                                </div>
                            </div>
                        </div>
                        
<!-- Product 6 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="ASUS NUC 14 Essential Int" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'ASUS NUC 14 Essential Int', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png', '4.490.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
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
                                
                                <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">4.490.000₫</span>
                                    <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                                </div>
                            </div>
                        </div>

                        <!-- Product 7 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="AtomMan G7 PT Mini PC" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'AtomMan G7 PT Mini PC', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png', '34.490.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
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
                                
                                <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">34.490.000₫</span>
                                    <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                                </div>
                            </div>
                        </div>

                        <!-- Product 8 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="Mini PC GMK EVO X1 32G" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'Mini PC GMK EVO X1 32G', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_1.png', '31.190.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
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
                                
                                <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">31.190.000₫</span>
                                    <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                                </div>
                            </div>
                        </div>

                        <!-- Product 9 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="Tablet Minisforum V3 SE" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'Tablet Minisforum V3 SE', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_2.png', '23.090.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
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
                                
                                <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">23.090.000₫</span>
                                    <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Product 10 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="Beelink SER8 AMD 884" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'Beelink SER8 AMD 884', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_2.png', '11.990.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
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
                                
                                <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">11.990.000₫</span>
                                    <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                                </div>
                            </div>
                        </div>
                        
<!-- Product 11 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="ASUS NUC 14 Essential Int" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'ASUS NUC 14 Essential Int', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png', '4.490.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
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
                                
                                <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">4.490.000₫</span>
                                    <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                                </div>
                            </div>
                        </div>

                        <!-- Product 12 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="AtomMan G7 PT Mini PC" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'AtomMan G7 PT Mini PC', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png', '34.490.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
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
                                
                                <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">34.490.000₫</span>
                                    <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                                </div>
                            </div>
                        </div>

                        <!-- Product 13 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="Mini PC GMK EVO X1 32G" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'Mini PC GMK EVO X1 32G', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_1.png', '31.190.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
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
                                
                                <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">31.190.000₫</span>
                                    <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                                </div>
                            </div>
                        </div>

                        <!-- Product 14 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="Tablet Minisforum V3 SE" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'Tablet Minisforum V3 SE', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_2.png', '23.090.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
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
                                
                                <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">23.090.000₫</span>
                                    <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Product 15 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="Beelink SER8 AMD 884" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'Beelink SER8 AMD 884', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_2.png', '11.990.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
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
                                
                                <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">11.990.000₫</span>
                                    <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                                </div>
                            </div>
                        </div>
                        
<!-- Product 16 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="ASUS NUC 14 Essential Int" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'ASUS NUC 14 Essential Int', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png', '4.490.000₫')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
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
                                
                                <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">4.490.000₫</span>
                                    <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                                </div>
                            </div>
                        </div>

                                            </div>
                    
                    <div class="pagination" style="display: flex; justify-content: center; gap: 12px; margin-top: 50px; margin-bottom: 20px;">
                        <button style="width: 44px; height: 44px; border-radius: 50%; border: 1px solid var(--border-color); background: var(--bg-white); color: var(--text-dark); font-weight: bold; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.3s;" onmouseover="this.style.background='var(--bg-gray)'" onmouseout="this.style.background='var(--bg-white)'"><i class="ph ph-caret-left"></i></button>
                        <button style="width: 44px; height: 44px; border-radius: 50%; border: none; background: var(--primary); color: white; font-weight: bold; cursor: pointer; box-shadow: 0 4px 10px rgba(14, 165, 233, 0.3);">1</button>
                        <button style="width: 44px; height: 44px; border-radius: 50%; border: 1px solid var(--border-color); background: var(--bg-white); color: var(--text-dark); font-weight: bold; cursor: pointer; transition: all 0.3s;" onmouseover="this.style.background='var(--bg-gray)'" onmouseout="this.style.background='var(--bg-white)'">2</button>
                        <button style="width: 44px; height: 44px; border-radius: 50%; border: 1px solid var(--border-color); background: var(--bg-white); color: var(--text-dark); font-weight: bold; cursor: pointer; transition: all 0.3s;" onmouseover="this.style.background='var(--bg-gray)'" onmouseout="this.style.background='var(--bg-white)'">3</button>
                        <button style="width: 44px; height: 44px; border-radius: 50%; border: 1px solid var(--border-color); background: var(--bg-white); color: var(--text-dark); font-weight: bold; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.3s;" onmouseover="this.style.background='var(--bg-gray)'" onmouseout="this.style.background='var(--bg-white)'"><i class="ph ph-caret-right"></i></button>
                    </div>
                </div>
            </div>
            
            <button class="mobile-filter-btn" onclick="toggleMobileSidebar()"><i class="ph-bold ph-faders" style="font-size: 1.4rem;"></i></button>
            <div class="sidebar-overlay" onclick="toggleMobileSidebar()"></div>
            
            <div id="quick-view-modal" style="position: fixed; inset: 0; background: rgba(0,0,0,0.6); backdrop-filter: blur(5px); z-index: 10000; display: none; align-items: center; justify-content: center; opacity: 0; transition: opacity 0.3s;">
                <div style="background: var(--bg-white); width: 90%; max-width: 900px; height: 80vh; max-height: 600px; border-radius: var(--radius-lg); position: relative; display: flex; overflow: hidden; transform: scale(0.95); transition: transform 0.3s;">
                    <button onclick="closeQuickView()" style="position: absolute; top: 15px; right: 15px; background: var(--bg-gray); border: none; width: 40px; height: 40px; border-radius: 50%; font-size: 1.2rem; display: flex; align-items: center; justify-content: center; cursor: pointer; z-index: 10;" onmouseover="this.style.color='#ef4444'" onmouseout="this.style.color='var(--text-dark)'"><i class="ph-bold ph-x"></i></button>
                    <div style="flex: 1; display: flex; align-items: center; justify-content: center; background: #f8fafc; padding: 20px;">
                        <img id="qv-img" src="" style="max-width: 100%; max-height: 100%; object-fit: contain;">
                    </div>
                    <div style="flex: 1; padding: 40px 30px; display: flex; flex-direction: column;">
                        <h2 id="qv-title" style="font-size: 1.5rem; font-weight: 800; margin-bottom: 10px; color: var(--text-dark);"></h2>
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
                            <a href="demo_product.html" style="flex: 1; padding: 12px; background: var(--bg-gray); color: var(--text-dark); border: 1px solid var(--border-color); border-radius: 8px; font-weight: bold; font-size: 1.1rem; text-align: center; text-decoration: none; transition: 0.2s;" onmouseover="this.style.background='var(--border-color)'" onmouseout="this.style.background='var(--bg-gray)'">Xem chi tiết</a>
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
                
    local_footer_part = sticky_stuff + '<script src="assets/main.js" defer></script>\n' + footer_part

    product_html = """
        <style>
            html, body { max-width: 100vw; overflow-x: hidden; }
            .nava-breadcrumb, .thumbnail-list { overscroll-behavior-x: contain; box-sizing: border-box; }
        </style>
        <div class="container" style="max-width: 1400px !important; width: 100% !important; box-sizing: border-box !important; margin: 30px auto 0 !important; padding: 0 16px !important;">
            <style>.nava-breadcrumb::-webkit-scrollbar { display: none; }</style>
            <div class="nava-breadcrumb" style="background: transparent; padding: 0; margin-bottom: 24px; font-size: 0.9rem; display: flex; align-items: center; gap: 8px; z-index: 10; position: relative; flex-wrap: nowrap; overflow-x: auto; white-space: nowrap; scrollbar-width: none; -webkit-overflow-scrolling: touch;">
                <a href="/" style="color: #1e3a8a; text-decoration: none; font-weight: 500; flex-shrink: 0;">Trang chủ</a>
                <span style="color: #64748b; font-weight: 500; flex-shrink: 0;">/</span>
                <a href="#" style="color: #1e3a8a; text-decoration: none; font-weight: 500; flex-shrink: 0;">Mini PC</a>
                <span style="color: #64748b; font-weight: 500; flex-shrink: 0;">/</span>
                <a href="#" style="color: #1e3a8a; text-decoration: none; font-weight: 500; flex-shrink: 0;">Mini PC Asus</a>
                <span style="color: #64748b; font-weight: 500; flex-shrink: 0;">/</span>
                <span style="color: #64748b; font-weight: 500; flex-shrink: 0;">ASUS NUC AI 350</span>
            </div>
            
            <style>
                /* Base Reset for Product Page */
                .nava-product-layout { display: flex; flex-direction: column; gap: 40px; margin-top: 20px; width: 100%; box-sizing: border-box; }
                .nava-prod-gallery { width: 100%; box-sizing: border-box; }
                .nava-prod-info { width: 100%; display: flex; flex-direction: column; box-sizing: border-box; }
                @media (min-width: 992px) {
                    .nava-product-layout { flex-direction: row; align-items: flex-start; gap: 60px; }
                    .nava-prod-gallery { width: 55%; position: sticky; top: 130px; }
                    .nava-prod-info { width: 45%; }
                }
                
                /* Clean Gallery */
                .main-image-container { 
                    background: #f8fafc; 
                    border-radius: 16px; 
                    padding: 24px; 
                    text-align: center; 
                    margin-bottom: 16px; 
                    display: flex; 
                    align-items: center; 
                    justify-content: center; 
                    position: relative;
                    aspect-ratio: 4/3;
                }
                .main-image-container img { max-width: 90%; max-height: 90%; object-fit: contain; }
                .gallery-nav-btn {
                    position: absolute; top: 50%; transform: translateY(-50%);
                    width: 40px; height: 40px; background: rgba(255,255,255,0.8); backdrop-filter: blur(4px);
                    border-radius: 50%; display: flex; align-items: center; justify-content: center;
                    cursor: pointer; border: 1px solid #e2e8f0; color: #475569; transition: 0.2s; z-index: 5;
                }
                .gallery-nav-btn:hover { background: #fff; color: var(--primary); box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
                .gallery-nav-prev { left: 16px; }
                .gallery-nav-next { right: 16px; }
                .gallery-dots { display: flex; justify-content: center; gap: 8px; margin-bottom: 16px; }
                .gallery-dot { width: 8px; height: 8px; border-radius: 50%; background: #cbd5e1; cursor: pointer; transition: 0.3s; }
                .gallery-dot.active { background: var(--primary); width: 24px; border-radius: 4px; }
                .gallery-thumb { 
                    width: 72px; height: 72px; border-radius: 12px; background: #f8fafc; padding: 8px; 
                    cursor: pointer; border: 2px solid transparent; transition: 0.2s; flex-shrink: 0;
                }
                .gallery-thumb:hover { border-color: #cbd5e1; }
                .gallery-thumb.active { border-color: var(--primary); }
                
                /* Minimal Typography */
                .prod-brand { margin-bottom: 12px; }
                .prod-brand img { height: 24px; object-fit: contain; }
                .prod-title { font-size: 1.8rem; font-weight: 700; color: #0f172a; line-height: 1.3; margin-bottom: 16px; }
                .prod-price-wrap { display: flex; align-items: baseline; gap: 12px; margin-bottom: 30px; padding-bottom: 24px; border-bottom: 1px solid #e2e8f0; }
                .prod-price { font-size: 2.2rem; font-weight: 700; color: var(--primary); }
                .prod-vat { font-size: 0.85rem; color: #64748b; }
                
                /* Flat Variants completely redesigned */
                .variant-group { margin-bottom: 24px; }
                .variant-label { font-weight: 600; font-size: 0.9rem; color: #1e293b; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;}
                .variant-options { display: flex; flex-wrap: wrap; gap: 8px; }
                .variant-card {
                    border: 1px solid #cbd5e1; border-radius: 8px; padding: 8px 12px;
                    cursor: pointer; background: #fff; transition: 0.2s;
                    display: flex; align-items: baseline; gap: 6px;
                }
                .variant-card:hover { border-color: #94a3b8; }
                .variant-card.active { border-color: var(--primary); background: #f0f9ff; box-shadow: 0 0 0 1px var(--primary); }
                .variant-card-title { font-size: 0.85rem; font-weight: 700; color: #0f172a; }
                .variant-card.active .variant-card-title { color: var(--primary); }
                .variant-card-price { font-size: 0.75rem; color: #64748b; font-weight: 500; }
                
                /* Action Buttons */
                .action-row { display: flex; gap: 12px; margin-bottom: 12px; margin-top: 10px; }
                .qty-input-group { 
                    display: flex; align-items: center; border: 1px solid #cbd5e1; border-radius: 8px; height: 50px; width: 110px; flex-shrink: 0;
                }
                .qty-btn { width: 36px; height: 100%; background: transparent; border: none; font-size: 1.2rem; cursor: pointer; color: #475569; }
                .qty-input { width: 38px; text-align: center; border: none; background: transparent; font-weight: 600; font-size: 1rem; color: #0f172a; }
                
                .btn-add-cart { 
                    flex: 1; height: 50px; background: #f8fafc; color: var(--primary); border: 1px solid #e2e8f0; border-radius: 8px; font-weight: 700; font-size: 0.95rem; cursor: pointer; transition: 0.2s;
                }
                .btn-add-cart:hover { background: #e2e8f0; }
                
                .btn-buy-now { 
                    width: 100%; height: 56px; background: var(--primary); color: #fff; border: none; border-radius: 8px; font-weight: 700; font-size: 1.1rem; cursor: pointer; transition: 0.2s; margin-bottom: 24px;
                }
                .btn-buy-now:hover { opacity: 0.9; box-shadow: 0 4px 12px rgba(14,165,233,0.3); }
                
                /* Dark Mode Overrides for Product Page */
                [data-theme="dark"] body { background-color: var(--bg-white) !important; color: var(--text-dark) !important; }
                [data-theme="dark"] .main-image-container { background: #fff !important; border-color: var(--border-color); padding: 20px; border-radius: 16px; box-shadow: inset 0 0 0 1px #e2e8f0; }
                [data-theme="dark"] .main-image-container img { mix-blend-mode: normal !important; }
                [data-theme="dark"] .gallery-nav-btn { background: rgba(30,41,59,0.8); border-color: var(--border-color); color: var(--text-dark); }
                [data-theme="dark"] .gallery-nav-btn:hover { background: var(--primary); color: white; }
                [data-theme="dark"] .gallery-dot { background: var(--border-color); }
                [data-theme="dark"] .gallery-thumb { background: #fff !important; border-color: var(--border-color); padding: 4px; box-shadow: inset 0 0 0 1px #e2e8f0; }
                [data-theme="dark"] .gallery-thumb.active { box-shadow: 0 0 0 2px var(--primary); }
                [data-theme="dark"] .prod-brand img { filter: brightness(0) invert(1) !important; opacity: 0.9; }
                [data-theme="dark"] .prod-title { color: var(--text-dark); }
                [data-theme="dark"] .prod-price-wrap { border-bottom-color: var(--border-color); }
                [data-theme="dark"] .prod-vat { color: var(--text-gray); }
                [data-theme="dark"] .variant-label { color: var(--text-dark); }
                [data-theme="dark"] .variant-card { background: var(--bg-gray); border-color: var(--border-color); }
                [data-theme="dark"] .variant-card:hover { border-color: var(--text-gray); }
                [data-theme="dark"] .variant-card.active { background: rgba(51, 133, 255, 0.1); border-color: var(--primary); }
                [data-theme="dark"] .variant-card-title { color: var(--text-dark) !important; }
                [data-theme="dark"] .variant-card.active .variant-card-title { color: var(--primary) !important; }
                [data-theme="dark"] .variant-card-price { color: var(--text-gray); }
                [data-theme="dark"] .qty-input-group { border-color: var(--border-color) !important; background: transparent !important; }
                [data-theme="dark"] .qty-btn { color: var(--text-dark); }
                [data-theme="dark"] .qty-input { color: var(--text-dark); }
                [data-theme="dark"] .btn-add-cart { background: rgba(51, 133, 255, 0.15); border-color: rgba(51, 133, 255, 0.3); color: #66a3ff; }
                [data-theme="dark"] .btn-add-cart:hover { background: rgba(51, 133, 255, 0.25); }
                [data-theme="dark"] .btn-buy-now { background: var(--primary); color: #fff; }
                [data-theme="dark"] .policy-box { border-color: var(--border-color) !important; background: var(--bg-gray) !important; }
                [data-theme="dark"] .policy-box h3 { color: var(--text-dark) !important; }
                [data-theme="dark"] .policy-box .policy-item { color: var(--text-dark) !important; }
                [data-theme="dark"] .mobile-actions-col button:nth-child(2) { background: var(--bg-gray) !important; }
                [data-theme="dark"] #sticky-cart-bar { background: rgba(15,23,42,0.95) !important; border-top-color: var(--border-color) !important; }
                [data-theme="dark"] .sticky-cart-left .img-wrap { background: #fff !important; border-color: var(--border-color) !important; }
                [data-theme="dark"] .sticky-title { color: var(--text-dark) !important; }
                [data-theme="dark"] .nava-breadcrumb span { color: var(--text-gray) !important; }
                [data-theme="dark"] .nava-breadcrumb a { color: var(--text-dark) !important; }
                [data-theme="dark"] .nava-breadcrumb a:hover { color: var(--primary) !important; }
                
                [data-theme="dark"] .desc-column { background: var(--bg-white); border-color: var(--border-color); }
                [data-theme="dark"] .desc-column h2, [data-theme="dark"] .desc-column h3 { color: var(--text-dark) !important; }
                [data-theme="dark"] .desc-column p, [data-theme="dark"] .desc-column ul, [data-theme="dark"] .desc-column li { color: var(--text-gray) !important; }
                [data-theme="dark"] .desc-column strong { color: var(--text-dark) !important; }
                
                [data-theme="dark"] .specs-column { background: var(--bg-gray); border-color: var(--border-color); }
                [data-theme="dark"] .specs-column h2 { color: var(--text-dark) !important; }
                [data-theme="dark"] .nava-spec-row { border-color: var(--border-color); }
                [data-theme="dark"] .nava-spec-label { color: var(--text-gray) !important; }
                [data-theme="dark"] .nava-spec-value { color: var(--text-dark) !important; }
                [data-theme="dark"] .specs-column .action-btn { background: var(--bg-white) !important; border-color: var(--border-color) !important; color: var(--primary) !important; }
                [data-theme="dark"] .specs-column .action-btn:hover { background: var(--bg-gray) !important; }
                
                [data-theme="dark"] .product-card { background: var(--bg-white); border-color: var(--border-color); }
                [data-theme="dark"] .product-card h2.card-title { color: var(--text-dark) !important; }
                [data-theme="dark"] .product-card:hover h2.card-title { color: var(--primary) !important; }
                [data-theme="dark"] .product-card .compare-btn { background: var(--bg-gray) !important; color: var(--text-gray) !important; border-color: var(--border-color) !important; }
                [data-theme="dark"] .product-card .compare-btn:hover { color: var(--primary) !important; border-color: var(--primary) !important; }
                [data-theme="dark"] .product-card span[style*="color: var(--text-dark)"] { color: var(--text-dark) !important; }
                [data-theme="dark"] .sp-item { background: var(--bg-gray) !important; border-color: var(--border-color) !important; color: var(--text-dark) !important; }
                [data-theme="dark"] .sp-item i { background: var(--bg-white) !important; box-shadow: none; }
                [data-theme="dark"] h2 { color: var(--text-dark) !important; }
                [data-theme="dark"] .badge { background: var(--primary) !important; color: white !important; }
                
                /* Simple Policy */
                .simple-policies { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; padding-top: 24px; border-top: 1px dashed #cbd5e1; }
                .sp-item { display: flex; align-items: center; gap: 10px; font-size: 0.85rem; color: #334155; font-weight: 600; background: #f8fafc; padding: 12px; border-radius: 8px; border: 1px solid #e2e8f0; }
                .sp-item i { font-size: 1.2rem; color: var(--primary); background: #fff; padding: 6px; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
                
                @media (max-width: 768px) {
                    .prod-title { font-size: 1.4rem; margin-bottom: 12px; }
                    .prod-price { font-size: 1.8rem; }
                    .prod-price-wrap { margin-bottom: 20px; padding-bottom: 16px; flex-direction: column; gap: 4px; border-bottom: none; }
                    
                    /* Fix product details grid padding */
                    .desc-column { padding: 16px !important; }
                    .specs-column { padding: 16px !important; }
                    
                    /* Fix variants layout */
                    .variant-options { display: grid !important; grid-template-columns: 1fr 1fr; gap: 10px; }
                    .variant-card { flex-direction: column; align-items: flex-start; gap: 4px; padding: 10px; width: 100%; box-sizing: border-box; }
                    .variant-card-title { font-size: 0.85rem; }
                    .variant-card-price { font-size: 0.75rem; }
                    
                    /* Fix actions layout */
                    .nava-product-layout { gap: 24px; margin-bottom: 30px !important; }
                    .action-row { margin-bottom: 16px; }
                    .btn-buy-now-subtext { display: none !important; }
                    .mobile-actions-col button { padding: 8px 4px !important; }
                    .mobile-actions-col button span { font-size: 0.75rem !important; }
                    
                    /* Fix policies box */
                    .policy-mobile-box { display: flex !important; flex-direction: column !important; gap: 12px !important; }
                    
                    /* Fix gallery thumbnails cutoff on mobile */
                    .thumbnail-list { justify-content: flex-start !important; padding-left: 8px !important; padding-right: 8px !important; }
                }
                
                /* Magnifier */
                .main-image-container { position: relative; overflow: hidden; cursor: zoom-in; }
                #main-product-img { width: 100%; height: 100%; object-fit: contain; }
            </style>
            
            <div class="nava-product-layout" style="margin-bottom: 60px;">
                <!-- Gallery -->
                <div class="nava-prod-gallery">
                    <div class="main-image-container" id="main-image-container" onclick="openLightbox()">
                        <span class="badge" style="position: absolute; top: 16px; left: 16px; background: var(--primary); color: white; padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; z-index: 2;">MỚI NHẤT</span>
                        
                        <button style="position: absolute; top: 16px; right: 16px; background: rgba(255,255,255,0.8); border: 1px solid var(--border-color); width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; color: var(--text-dark); z-index: 5; backdrop-filter: blur(4px); transition: all 0.2s; box-shadow: 0 2px 8px rgba(0,0,0,0.05);" onmouseover="this.style.background='var(--primary)'; this.style.color='white'; this.style.borderColor='var(--primary)';" onmouseout="this.style.background='rgba(255,255,255,0.8)'; this.style.color='var(--text-dark)'; this.style.borderColor='var(--border-color)';"><i class="ph-bold ph-arrows-out"></i></button>
                        
                        <div class="gallery-nav-btn gallery-nav-prev" onclick="event.stopPropagation(); navigateGallery(-1)"><i class="ph-bold ph-caret-left"></i></div>
                        <img id="main-product-img" src="//bizweb.dktcdn.net/thumb/large/100/543/817/products/mini-pc-asus-nuc-ai-350-pn54-ryzen-ai-7-350-gaming.jpg?v=1763971973973" alt="ASUS NUC AI 350">
                        <div class="gallery-nav-btn gallery-nav-next" onclick="event.stopPropagation(); navigateGallery(1)"><i class="ph-bold ph-caret-right"></i></div>
                    </div>
                    
                    <div class="gallery-dots">
                        <div class="gallery-dot active" onclick="document.querySelectorAll('.gallery-thumb')[0].click()"></div>
                        <div class="gallery-dot" onclick="document.querySelectorAll('.gallery-thumb')[1].click()"></div>
                        <div class="gallery-dot" onclick="document.querySelectorAll('.gallery-thumb')[2].click()"></div>
                        <div class="gallery-dot" onclick="document.querySelectorAll('.gallery-thumb')[3].click()"></div>
                        <div class="gallery-dot" onclick="document.querySelectorAll('.gallery-thumb')[4].click()"></div>
                    </div>
                    
                    <div class="thumbnail-list" id="thumbnail-list" style="display: flex; justify-content: center; gap: 12px; overflow-x: auto; padding-bottom: 8px; scrollbar-width: none;">
                        <div class="gallery-thumb active" onclick="changeMainImage(this, '//bizweb.dktcdn.net/thumb/large/100/543/817/products/mini-pc-asus-nuc-ai-350-pn54-ryzen-ai-7-350-gaming.jpg?v=1763971973973')">
                            <img src="//bizweb.dktcdn.net/thumb/compact/100/543/817/products/mini-pc-asus-nuc-ai-350-pn54-ryzen-ai-7-350-gaming.jpg?v=1763971973973" style="width: 100%; height: 100%; object-fit: contain;">
                        </div>
                        <div class="gallery-thumb" onclick="changeMainImage(this, '//bizweb.dktcdn.net/thumb/large/100/543/817/products/w692-01a37475-f53f-4188-84a0-d46b8f01d6d6.png')">
                            <img src="//bizweb.dktcdn.net/thumb/compact/100/543/817/products/w692-01a37475-f53f-4188-84a0-d46b8f01d6d6.png" style="width: 100%; height: 100%; object-fit: contain;">
                        </div>
                        <div class="gallery-thumb" onclick="changeMainImage(this, '//bizweb.dktcdn.net/thumb/large/100/543/817/products/bia1-fc2ef492-2792-4c14-9b3f-5c7d6995afdc.png')">
                            <img src="//bizweb.dktcdn.net/thumb/compact/100/543/817/products/bia1-fc2ef492-2792-4c14-9b3f-5c7d6995afdc.png" style="width: 100%; height: 100%; object-fit: contain;">
                        </div>
                        <div class="gallery-thumb" onclick="changeMainImage(this, '//bizweb.dktcdn.net/thumb/large/100/543/817/products/asus-nuc-ai-350.jpg')">
                            <img src="//bizweb.dktcdn.net/thumb/compact/100/543/817/products/asus-nuc-ai-350.jpg" style="width: 100%; height: 100%; object-fit: contain;">
                        </div>
                        <div class="gallery-thumb" onclick="changeMainImage(this, '//bizweb.dktcdn.net/thumb/large/100/543/817/products/asus-nuc-ai-350-2.jpg')">
                            <img src="//bizweb.dktcdn.net/thumb/compact/100/543/817/products/asus-nuc-ai-350-2.jpg" style="width: 100%; height: 100%; object-fit: contain;">
                        </div>
                    </div>
                </div>
                
                <!-- Info -->
                <div class="nava-prod-info">
                    <div class="prod-brand">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/2/2e/ASUS_Logo.svg" alt="ASUS">
                    </div>
                    <h1 class="prod-title">ASUS NUC AI 350 (ExpertCenter PN54) Mini PC Ryzen AI 7 350</h1>
                    
                    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px; color: #64748b; font-size: 0.9rem;">
                        <span style="display: flex; align-items: center; gap: 4px; color: #f59e0b; font-weight: 600;"><i class="ph-fill ph-star"></i> 5.0</span>
                        <span>|</span>
                        <span>Đã bán: 85</span>
                        <span>|</span>
                        <span style="color: #059669; display: flex; align-items: center; gap: 4px;"><i class="ph-fill ph-check-circle"></i> Sẵn hàng</span>
                    </div>
                    
                    <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 24px;">
                        <div style="display: flex; align-items: center; gap: 6px; background: #f1f5f9; padding: 6px 12px; border-radius: 8px; font-size: 0.85rem; font-weight: 600; color: #334155; border: 1px solid #e2e8f0;">
                            <i class="ph ph-cpu" style="font-size: 1.1rem; color: var(--primary);"></i> Ryzen AI 7
                        </div>
                        <div style="display: flex; align-items: center; gap: 6px; background: #f1f5f9; padding: 6px 12px; border-radius: 8px; font-size: 0.85rem; font-weight: 600; color: #334155; border: 1px solid #e2e8f0;">
                            <i class="ph ph-graphics-card" style="font-size: 1.1rem; color: var(--primary);"></i> Radeon 860M
                        </div>
                        <div style="display: flex; align-items: center; gap: 6px; background: #f1f5f9; padding: 6px 12px; border-radius: 8px; font-size: 0.85rem; font-weight: 600; color: #334155; border: 1px solid #e2e8f0;">
                            <i class="ph ph-brain" style="font-size: 1.1rem; color: var(--primary);"></i> 50 TOPS
                        </div>
                        <a href="#thong-so" style="display: flex; align-items: center; gap: 4px; padding: 6px 12px; font-size: 0.85rem; font-weight: 600; color: #1e3a8a; text-decoration: none; transition: 0.2s;" onmouseover="this.style.textDecoration='underline'" onmouseout="this.style.textDecoration='none'">Xem chi tiết <i class="ph-bold ph-caret-right"></i></a>
                    </div>
                    
                    <div class="prod-price-wrap">
                        <div class="prod-price" id="main-price">12.390.000₫</div>
                        <div class="prod-vat">Giá đã bao gồm VAT</div>
                    </div>

                    <!-- Variants -->
                    <div class="variant-group">
                        <div class="variant-label"><span>RAM DDR5</span></div>
                        <div class="variant-options">
                            <div class="variant-card active" onclick="selectVariant(this, 'ram', 0)">
                                <span class="variant-card-title">0GB</span>
                                <span class="variant-card-price">Cơ bản</span>
                            </div>
                            <div class="variant-card" onclick="selectVariant(this, 'ram', 1890000)">
                                <span class="variant-card-title">8GB - 4800</span>
                                <span class="variant-card-price">+1.890.000₫</span>
                            </div>
                            <div class="variant-card" onclick="selectVariant(this, 'ram', 2090000)">
                                <span class="variant-card-title">8GB - 5600</span>
                                <span class="variant-card-price">+2.090.000₫</span>
                            </div>
                            <div class="variant-card" onclick="selectVariant(this, 'ram', 3790000)">
                                <span class="variant-card-title">16GB - 4800</span>
                                <span class="variant-card-price">+3.790.000₫</span>
                            </div>
                            <div class="variant-card" onclick="selectVariant(this, 'ram', 4190000)">
                                <span class="variant-card-title">16GB - 5600</span>
                                <span class="variant-card-price">+4.190.000₫</span>
                            </div>
                            <div class="variant-card" onclick="selectVariant(this, 'ram', 6990000)">
                                <span class="variant-card-title">32GB - 4800</span>
                                <span class="variant-card-price">+6.990.000₫</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="variant-group" style="margin-bottom: 32px;">
                        <div class="variant-label"><span>Ổ cứng SSD NVMe</span></div>
                        <div class="variant-options">
                            <div class="variant-card active" onclick="selectVariant(this, 'ssd', 0)">
                                <span class="variant-card-title">0GB</span>
                                <span class="variant-card-price">Cơ bản</span>
                            </div>
                            <div class="variant-card" onclick="selectVariant(this, 'ssd', 1190000)">
                                <span class="variant-card-title">256GB</span>
                                <span class="variant-card-price">+1.190.000₫</span>
                            </div>
                            <div class="variant-card" onclick="selectVariant(this, 'ssd', 2290000)">
                                <span class="variant-card-title">500GB</span>
                                <span class="variant-card-price">+2.290.000₫</span>
                            </div>
                            <div class="variant-card" onclick="selectVariant(this, 'ssd', 3990000)">
                                <span class="variant-card-title">1TB</span>
                                <span class="variant-card-price">+3.990.000₫</span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Actions -->
                    <div class="action-row">
                        <div class="qty-input-group">
                            <button class="qty-btn" onclick="let input=this.nextElementSibling; if(input.value>1) input.value--">-</button>
                            <input type="text" value="1" class="qty-input" readonly>
                            <button class="qty-btn" onclick="let input=this.previousElementSibling; input.value++">+</button>
                        </div>
                        <button class="btn-add-cart">THÊM VÀO GIỎ</button>
                    </div>
                    
                    <div class="mobile-actions-col" style="display: flex; gap: 12px; margin-bottom: 24px;">
                        <button class="btn-buy-now" style="flex: 7; margin-bottom: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; line-height: 1.4;">
                            <span style="font-size: 1.1rem; font-weight: 700;">MUA NGAY</span>
                            <span class="btn-buy-now-subtext" style="font-size: 0.8rem; font-weight: 500; opacity: 0.9;">Giao tận nơi hoặc nhận tại cửa hàng</span>
                        </button>
                        <button style="flex: 3; background: #fff; border: 1px solid var(--primary); border-radius: 8px; color: var(--primary); font-weight: 700; cursor: pointer; transition: 0.2s; display: flex; flex-direction: column; align-items: center; justify-content: center; line-height: 1.4;" onmouseover="this.style.background='var(--primary)'; this.style.color='#fff';" onmouseout="this.style.background='#fff'; this.style.color='var(--primary)';">
                            <i class="ph-bold ph-storefront" style="font-size: 1.4rem;"></i>
                            <span style="margin-top: 4px; text-align: center;">ĐẾN CỬA HÀNG</span>
                        </button>
                    </div>
                    
                    <div class="policy-box" style="border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; background: #f8fafc;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                            <h3 style="font-size: 1.05rem; font-weight: 800; color: #0f172a; margin: 0;">Chính sách sản phẩm</h3>
                            <a href="#" style="font-size: 0.85rem; color: #1e3a8a; text-decoration: none; font-weight: 600;">Tìm hiểu thêm</a>
                        </div>
                        
                        <div class="policy-mobile-box" style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                            <div class="policy-item" style="display: flex; align-items: flex-start; gap: 10px; font-size: 0.85rem; color: #334155; font-weight: 600;">
                                <i class="ph ph-shield-check" style="font-size: 1.4rem; color: var(--primary);"></i> Hàng chính hãng - Bảo hành 36 tháng
                            </div>
                            <div class="policy-item" style="display: flex; align-items: flex-start; gap: 10px; font-size: 0.85rem; color: #334155; font-weight: 600;">
                                <i class="ph ph-truck" style="font-size: 1.4rem; color: var(--primary);"></i> Giao hàng miễn phí toàn quốc
                            </div>
                            <div class="policy-item" style="display: flex; align-items: flex-start; gap: 10px; font-size: 0.85rem; color: #334155; font-weight: 600;">
                                <i class="ph ph-arrows-left-right" style="font-size: 1.4rem; color: var(--primary);"></i> 1 đổi 1 trong 30 ngày
                            </div>
                            <div class="policy-item" style="display: flex; align-items: flex-start; gap: 10px; font-size: 0.85rem; color: #334155; font-weight: 600;">
                                <i class="ph ph-headset" style="font-size: 1.4rem; color: var(--primary);"></i> Hỗ trợ kỹ thuật trọn đời
                            </div>
                        </div>
                    </div>
                    

                </div>
            </div>
            
            <!-- Product Details Grid -->
            <div style="margin-bottom: 80px; width: 100%;">
                <style>
                    .product-details-grid { display: flex; flex-direction: column; gap: 30px; }
                    .desc-column { background: #fff; border-radius: 16px; border: 1px solid #e2e8f0; padding: 32px; flex: 1; }
                    .specs-column { background: #f8fafc; border-radius: 16px; padding: 24px; border: 1px solid #e2e8f0; }
                    .nava-spec-grid { display: flex; flex-direction: column; }
                    .nava-spec-row { display: grid; grid-template-columns: 120px 1fr; gap: 16px; padding: 12px 0; border-bottom: 1px solid #e2e8f0; }
                    .nava-spec-row:last-child { border-bottom: none; }
                    .nava-spec-label { color: #64748b; font-weight: 500; font-size: 0.85rem; }
                    .nava-spec-value { color: #0f172a; font-weight: 600; font-size: 0.85rem; line-height: 1.4; word-break: break-word; }
                    @media (min-width: 992px) {
                        .product-details-grid { flex-direction: row; align-items: flex-start; gap: 40px; }
                        .desc-column { width: 60%; }
                        .specs-column { width: 40%; position: sticky; top: 130px; }
                    }
                </style>
                
                <div class="product-details-grid">
                    <!-- Left: Description -->
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
                    </div>
                    
                    <!-- Right: Technical Specs -->
                    <div class="specs-column">
                        <h2 style="font-size: 1.2rem; font-weight: 700; margin-bottom: 20px; color: #0f172a; display: flex; align-items: center; gap: 8px;">
                            <i class="ph-fill ph-cpu" style="color: var(--primary);"></i> Thông số kỹ thuật
                        </h2>
                        
                        <div class="nava-spec-grid">
                            <div class="nava-spec-row">
                                <div class="nava-spec-label">CPU</div>
                                <div class="nava-spec-value">AMD Ryzen™ AI 7 350 (up to 5.1 GHz)</div>
                            </div>
                            <div class="nava-spec-row">
                                <div class="nava-spec-label">Đồ họa</div>
                                <div class="nava-spec-value">AMD Radeon™ 860M</div>
                            </div>
                            <div class="nava-spec-row">
                                <div class="nava-spec-label">NPU (AI)</div>
                                <div class="nava-spec-value">Lên đến 50 TOPS</div>
                            </div>
                            <div class="nava-spec-row">
                                <div class="nava-spec-label">RAM</div>
                                <div class="nava-spec-value">Hỗ trợ DDR5-5600 (Max 64GB)</div>
                            </div>
                            <div class="nava-spec-row">
                                <div class="nava-spec-label">Lưu trữ</div>
                                <div class="nava-spec-value">2 x M.2 2280 PCIe Gen4x4 NVMe</div>
                            </div>
                            <div class="nava-spec-row">
                                <div class="nava-spec-label">Kết nối</div>
                                <div class="nava-spec-value">Wi-Fi 6E, Bluetooth 5.3, 2.5G LAN</div>
                            </div>
                            <div class="nava-spec-row">
                                <div class="nava-spec-label">Cổng xuất hình</div>
                                <div class="nava-spec-value">Hỗ trợ 4 màn hình 4K</div>
                            </div>
                            <div class="nava-spec-row">
                                <div class="nava-spec-label">Trọng lượng</div>
                                <div class="nava-spec-value">0.75 kg</div>
                            </div>
                            <div class="nava-spec-row">
                                <div class="nava-spec-label">Bảo hành</div>
                                <div class="nava-spec-value">36 tháng chính hãng</div>
                            </div>
                        </div>
                        
                        <button class="action-btn" style="width: 100%; margin-top: 30px; border: 1px solid #cbd5e1; background: #fff; color: var(--primary); font-weight: 700; height: 48px; border-radius: 12px; display: flex; justify-content: center; align-items: center; gap: 8px; cursor: pointer; transition: all 0.2s;" onmouseover="this.style.borderColor='var(--primary)'; this.style.boxShadow='0 4px 10px rgba(14,165,233,0.1)';" onmouseout="this.style.borderColor='#cbd5e1'; this.style.boxShadow='none';">
                            <i class="ph-bold ph-download-simple"></i> Tải Datasheet (PDF)
                        </button>
                    </div>
                </div>
            </div>
            
            <!-- Recommended Products Section -->
            <div style="margin-top: 20px; margin-bottom: 80px; width: 100%;">
                <h2 style="font-size: 1.6rem; font-weight: 800; margin-bottom: 24px; color: #0f172a; display: flex; justify-content: space-between; align-items: center;">
                    Sản phẩm liên quan
                    <div style="display: flex; gap: 8px;">
                        <button style="width: 36px; height: 36px; border-radius: 50%; border: 1px solid var(--border-color); background: var(--bg-white); display: flex; justify-content: center; align-items: center; cursor: pointer; color: var(--text-gray); transition: all 0.2s;" onmouseover="this.style.borderColor='var(--primary)'; this.style.color='var(--primary)';" onmouseout="this.style.borderColor='var(--border-color)'; this.style.color='var(--text-gray)';"><i class="ph-bold ph-caret-left"></i></button>
                        <button style="width: 36px; height: 36px; border-radius: 50%; border: 1px solid var(--border-color); background: var(--bg-white); display: flex; justify-content: center; align-items: center; cursor: pointer; color: var(--text-dark); transition: all 0.2s;" onmouseover="this.style.borderColor='var(--primary)'; this.style.color='var(--primary)';" onmouseout="this.style.borderColor='var(--border-color)'; this.style.color='var(--text-dark)';"><i class="ph-bold ph-caret-right"></i></button>
                    </div>
                </h2>
                
                <style>
                    .related-product-grid {
                        display: grid;
                        grid-template-columns: repeat(4, 1fr);
                        gap: 20px;
                        padding-bottom: 20px;
                    }
                    @media (max-width: 1199px) { .related-product-grid { grid-template-columns: repeat(3, 1fr); } }
                    @media (max-width: 991px) { .related-product-grid { grid-template-columns: repeat(2, 1fr); } }
                    @media (max-width: 575px) { .related-product-grid { grid-template-columns: repeat(2, 1fr); gap: 10px; } }
                    
                    .product-card {
                        background: #fff;
                        border-radius: 16px;
                        border: 1px solid var(--border-color);
                        padding: 15px;
                        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                        position: relative;
                        display: flex;
                        flex-direction: column;
                        height: 100%;
                        cursor: pointer;
                        overflow: hidden;
                    }
                    .product-card:hover {
                        box-shadow: 0 20px 40px -10px rgba(0,0,0,0.1);
                        transform: translateY(-4px);
                        border-color: var(--primary);
                    }
                    .card-glow { position: absolute; inset: 0; background: radial-gradient(circle at 50% 0%, rgba(14, 165, 233, 0.08) 0%, transparent 70%); opacity: 0; transition: opacity 0.4s ease; pointer-events: none; z-index: 1; }
                    .product-card:hover .card-glow { opacity: 1; }
                    
                    .card-image-wrap {
                        height: 180px; position: relative; background: transparent; padding: 0; z-index: 2;
                    }
                    .compare-btn {
                        position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: #fff; border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);
                    }
                    .compare-btn:hover {
                        border-color: var(--primary); color: var(--primary);
                    }
                    .product-img {
                        object-fit: contain; width: 100%; height: 100%; transition: transform 0.4s ease;
                    }
                    .product-card:hover .product-img {
                        transform: scale(1.05);
                    }
                    .card-content {
                        padding: 15px 0 0 0; flex: 1; display: flex; flex-direction: column; z-index: 2;
                    }
                    .card-specs {
                        display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 12px;
                    }
                    .spec-pill {
                        background: linear-gradient(135deg, #1e3a8a, #3b82f6); color: white; padding: 4px 8px; border-radius: 6px; font-size: 0.7rem; font-weight: 800; display: inline-block; white-space: nowrap; box-shadow: 0 2px 4px rgba(30, 58, 138, 0.2);
                    }
                    .spec-pill.secondary {
                        background: var(--bg-gray); color: var(--text-gray); border: 1px solid var(--border-color); box-shadow: none; font-weight: 600;
                    }
                    .card-title {
                        font-size: 1rem; line-height: 1.4; margin-bottom: 10px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; height: 40px; font-weight: 700; color: #0f172a; transition: color 0.2s;
                    }
                    .product-card:hover .card-title {
                        color: var(--primary);
                    }
                </style>
                
                <div class="related-product-grid">
                    <!-- Product 1 -->
                    <div class="product-card" onclick="window.location.href='demo_product.html'">
                        <div class="card-glow"></div>
                        <div class="card-image-wrap">
                            <button class="compare-btn" data-name="ASUS NUC 14 Essential Int" title="Thêm vào so sánh" onclick="event.stopPropagation(); toggleCompare(this, 'ASUS NUC 14 Essential Int', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png', '4.490.000₫')"><i class="ph ph-arrows-left-right"></i></button>
                            <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" alt="ASUS NUC 14" class="product-img">
                        </div>
                        <div class="card-content">
                            <div class="card-specs">
                                <span class="spec-pill">CPU 6.000</span>
                                <span class="spec-pill secondary">MARK</span>
                                <span class="spec-pill secondary">GPU 1.200</span>
                                <span class="spec-pill">WIFI 6E</span>
                                <span class="spec-pill secondary">4 USB 3.2</span>
                                <span class="spec-pill secondary">2 TYPE C</span>
                            </div>
                            <h2 class="card-title">ASUS NUC 14 Essential Int...</h2>
                            <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">4.490.000₫</span>
                                <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Product 2 -->
                    <div class="product-card" onclick="window.location.href='demo_product.html'">
                        <div class="card-glow"></div>
                        <div class="card-image-wrap">
                            <button class="compare-btn" data-name="AtomMan G7 PT Mini PC" title="Thêm vào so sánh" onclick="event.stopPropagation(); toggleCompare(this, 'AtomMan G7 PT Mini PC', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png', '34.490.000₫')"><i class="ph ph-arrows-left-right"></i></button>
                            <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" alt="AtomMan G7 PT" class="product-img">
                        </div>
                        <div class="card-content">
                            <div class="card-specs">
                                <span class="spec-pill">CPU 40.000</span>
                                <span class="spec-pill secondary">MARK</span>
                                <span class="spec-pill secondary">GPU 17...</span>
                                <span class="spec-pill">4 FAN S...</span>
                                <span class="spec-pill secondary">WIFI 7</span>
                            </div>
                            <h2 class="card-title">AtomMan G7 PT Mini PC...</h2>
                            <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">34.490.000₫</span>
                                <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Product 3 -->
                    <div class="product-card" onclick="window.location.href='demo_product.html'">
                        <div class="card-glow"></div>
                        <div class="card-image-wrap">
                            <button class="compare-btn" data-name="Mini PC GMK EVO X1 32G" title="Thêm vào so sánh" onclick="event.stopPropagation(); toggleCompare(this, 'Mini PC GMK EVO X1 32G', '//bizweb.dktcdn.net/thumb/large/100/543/817/products/mini-pc-gmk-evo-x1-ai.jpg', '31.190.000₫')"><i class="ph ph-arrows-left-right"></i></button>
                            <img src="//bizweb.dktcdn.net/thumb/large/100/543/817/products/mini-pc-gmk-evo-x1-ai.jpg" alt="Mini PC GMK EVO" class="product-img">
                        </div>
                        <div class="card-content">
                            <div class="card-specs">
                                <span class="spec-pill">CPU 38.500</span>
                                <span class="spec-pill secondary">MARK</span>
                                <span class="spec-pill secondary">GPU ...</span>
                                <span class="spec-pill">2 NVME</span>
                                <span class="spec-pill secondary">USB4</span>
                            </div>
                            <h2 class="card-title">Mini PC GMK EVO X1 32G...</h2>
                            <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">31.190.000₫</span>
                                <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Product 4 -->
                    <div class="product-card" onclick="window.location.href='demo_product.html'">
                        <div class="card-glow"></div>
                        <div class="card-image-wrap">
                            <button class="compare-btn" data-name="Tablet Minisforum V3 SE" title="Thêm vào so sánh" onclick="event.stopPropagation(); toggleCompare(this, 'Tablet Minisforum V3 SE', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_2.png', '23.090.000₫')"><i class="ph ph-arrows-left-right"></i></button>
                            <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_2.png" alt="Tablet Minisforum" class="product-img">
                        </div>
                        <div class="card-content">
                            <div class="card-specs">
                                <span class="spec-pill">CPU 22.000</span>
                                <span class="spec-pill secondary">MARK</span>
                                <span class="spec-pill secondary">CPU ...</span>
                                <span class="spec-pill">WIFI 6</span>
                                <span class="spec-pill secondary">2 USB4</span>
                            </div>
                            <h2 class="card-title">Tablet Minisforum V3 SE...</h2>
                            <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">23.090.000₫</span>
                                <a href="demo_product.html" style="display:inline-flex;align-items:center;gap:6px;background:#1e3a8a;color:white;padding:7px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'"><i class="ph ph-shopping-cart-simple"></i> Xem ngay</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Sticky Add to Cart -->
            <style>
                .sticky-cart-left { display: flex; align-items: center; gap: 20px; }
                .sticky-cart-right { display: flex; gap: 16px; align-items: center; }
                .sticky-title { font-weight: 700; font-size: 1.1rem; color: var(--text-dark); margin-bottom: 4px; }
                .sticky-price-display { color: var(--primary); font-weight: 800; font-size: 1.3rem; letter-spacing: -0.5px; }
                @media (max-width: 768px) {
                    #sticky-cart-bar { padding: 10px 0 !important; background: rgba(255, 255, 255, 0.98) !important; }
                    .sticky-cart-left { flex-direction: column; align-items: flex-start; gap: 0 !important; flex: 1; min-width: 0; }
                    .sticky-cart-left > div:nth-child(2) { display: flex; flex-direction: column; }
                    .sticky-cart-left .img-wrap { display: none !important; }
                    .sticky-title { display: block !important; font-size: 0.75rem !important; font-weight: 500 !important; color: var(--text-gray) !important; margin: 0 !important; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; width: 100%; order: 2; }
                    .sticky-price-display { font-size: 1.15rem !important; margin-bottom: 0; order: 1; }
                    .sticky-cart-right { gap: 8px !important; flex-shrink: 0; }
                    .btn-add-cart-sticky { width: auto !important; min-width: 54px !important; padding: 0 20px !important; height: 42px !important; border-radius: 8px !important; }
                    .btn-add-cart-sticky i { font-size: 1.3rem !important; }
                    .btn-buy-now-sticky { height: 42px !important; padding: 0 15px !important; font-size: 0.9rem !important; border-radius: 8px !important; }
                    #sticky-cart-bar .container { padding: 0 12px !important; gap: 10px; }
                }
            </style>
            <div id="sticky-cart-bar" style="position: fixed; bottom: 0; left: 0; width: 100%; background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(20px); box-shadow: 0 -10px 40px rgba(0,0,0,0.08); padding: 16px 0; z-index: 1000; transform: translateY(100%); transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); border-top: 1px solid rgba(255,255,255,0.5);">
                <div class="container" style="display: flex; justify-content: space-between; align-items: center; max-width: 1250px; padding: 0 20px;">
                    <div class="sticky-cart-left">
                        <div class="img-wrap" style="width: 64px; height: 64px; background: #fff; border-radius: 12px; border: 1px solid #e2e8f0; padding: 6px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                            <img src="//bizweb.dktcdn.net/thumb/large/100/543/817/products/mini-pc-asus-nuc-ai-350-pn54-ryzen-ai-7-350-gaming.jpg?v=1763971973973" style="width: 100%; height: 100%; object-fit: contain;">
                        </div>
                        <div style="width: 100%;">
                            <div class="sticky-title">ASUS NUC AI 350</div>
                            <div class="sticky-price-display" id="sticky-price">12.390.000₫</div>
                        </div>
                    </div>
                    <div class="sticky-cart-right">
                        <button class="action-btn btn-add-cart btn-add-cart-sticky" style="width: auto; min-width: 64px; height: 48px; padding: 0 24px; border-radius: 8px !important; display: flex; align-items: center; justify-content: center; flex-shrink: 0;" title="Thêm vào giỏ">
                            <i class="ph ph-shopping-cart-simple" style="font-size: 1.4rem;"></i>
                        </button>
                        <button class="action-btn btn-buy-now btn-buy-now-sticky" style="height: 48px; margin-bottom: 0; border-radius: 8px !important; padding: 0 32px; box-shadow: 0 8px 15px -3px rgba(14, 165, 233, 0.3);">Mua ngay</button>
                    </div>
                </div>
            </div>
            
            <script>
                // Image Gallery Logic
                function changeMainImage(element, src) {
                    const img = document.getElementById('main-product-img');
                    if (img.src.includes(src)) return; // prevent clicking same image
                    
                    img.style.opacity = '0';
                    
                    setTimeout(() => {
                        img.src = src;
                        img.onload = () => { img.style.opacity = '1'; };
                        setTimeout(() => { img.style.opacity = '1'; }, 50); // fallback
                    }, 200);
                    
                    const thumbs = Array.from(document.querySelectorAll('.gallery-thumb'));
                    const dots = Array.from(document.querySelectorAll('.gallery-dot'));
                    
                    thumbs.forEach(t => t.classList.remove('active'));
                    element.classList.add('active');
                    
                    const index = thumbs.indexOf(element);
                    dots.forEach(d => d.classList.remove('active'));
                    if (dots[index]) dots[index].classList.add('active');
                    
                    element.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
                }
                
                function navigateGallery(direction) {
                    const thumbs = Array.from(document.querySelectorAll('.gallery-thumb'));
                    let activeIndex = thumbs.findIndex(t => t.classList.contains('active'));
                    
                    if (activeIndex === -1) return;
                    
                    let newIndex = activeIndex + direction;
                    if (newIndex >= thumbs.length) newIndex = 0;
                    if (newIndex < 0) newIndex = thumbs.length - 1;
                    
                    thumbs[newIndex].click();
                }
                
                // Variant Price Calculation Logic
                const basePrice = 12390000;
                let activeRamPrice = 0;
                let activeSsdPrice = 0;
                let activeRamName = '0GB';
                let activeSsdName = '0GB';
                
                function selectVariant(element, type, price) {
                    const siblings = element.parentNode.querySelectorAll('.variant-card');
                    siblings.forEach(el => el.classList.remove('active'));
                    element.classList.add('active');
                    
                    const titleEl = element.querySelector('.variant-card-title');
                    const name = titleEl ? titleEl.innerText : '';
                    
                    if (type === 'ram') { activeRamPrice = price; activeRamName = name; }
                    if (type === 'ssd') { activeSsdPrice = price; activeSsdName = name; }
                    
                    const total = basePrice + activeRamPrice + activeSsdPrice;
                    
                    document.getElementById('main-price').innerHTML = total.toLocaleString('vi-VN') + '₫';
                    const stickyPrice = document.getElementById('sticky-price');
                    if(stickyPrice) stickyPrice.innerHTML = total.toLocaleString('vi-VN') + '₫';
                    
                    const stickyTitle = document.querySelector('.sticky-title');
                    if(stickyTitle) {
                        let opts = [];
                        if(activeRamName && activeRamName !== '0GB') opts.push(activeRamName);
                        if(activeSsdName && activeSsdName !== '0GB') opts.push(activeSsdName);
                        let optString = opts.length > 0 ? ` - ${opts.join(', ')}` : '';
                        stickyTitle.innerHTML = 'ASUS NUC AI 350' + optString;
                    }
                }

                // Show sticky bar on scroll
                // Show sticky bar on scroll
                // Show sticky bar on scroll
                function toggleStickyBar(e) {
                    const stickyBar = document.getElementById('sticky-cart-bar');
                    if (!stickyBar) return;
                    
                    const threshold = window.innerWidth <= 768 ? 400 : 600;
                    let scrollY = window.scrollY || document.documentElement.scrollTop || document.body.scrollTop || 0;
                    
                    // Fallback for Sapo themes using wrapper scrolling
                    if (scrollY === 0) {
                        const wrappers = document.querySelectorAll('.bodywrap, .wrapper, #wrapper, .page-body, main, #main');
                        for (let i=0; i<wrappers.length; i++) {
                            if (wrappers[i].scrollTop > scrollY) scrollY = wrappers[i].scrollTop;
                        }
                    }
                    
                    // Trust event target if it's a large scrollable area
                    if (e && e.target && e.target.scrollTop > scrollY) {
                        if (e.target.clientHeight && e.target.clientHeight > window.innerHeight * 0.5) {
                            scrollY = e.target.scrollTop;
                        }
                    }
                    
                    if (scrollY > threshold) {
                        stickyBar.style.setProperty('transform', 'translateY(0)', 'important');
                        stickyBar.style.setProperty('display', 'block', 'important');
                    } else {
                        stickyBar.style.setProperty('transform', 'translateY(120%)', 'important');
                    }
                }

                document.addEventListener('DOMContentLoaded', function() {
                    const stickyBar = document.getElementById('sticky-cart-bar');
                    if (stickyBar) {
                        stickyBar.style.setProperty('z-index', '2147483647', 'important');
                        if (stickyBar.parentNode !== document.body) {
                            document.body.appendChild(stickyBar);
                        }
                    }
                    toggleStickyBar(); // Check immediately on load
                });

                window.addEventListener('scroll', toggleStickyBar, true);
                
                // Magnifier Effect
                const mainImgContainer = document.getElementById('main-image-container');
                const mainImgObj = document.getElementById('main-product-img');
                
                mainImgContainer.addEventListener('mousemove', (e) => {
                    if(window.innerWidth < 992) return; // Only zoom on desktop
                    const rect = mainImgContainer.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;
                    const xPercent = (x / rect.width) * 100;
                    const yPercent = (y / rect.height) * 100;
                    
                    mainImgObj.style.transformOrigin = `${xPercent}% ${yPercent}%`;
                    mainImgObj.style.transform = 'scale(2)';
                });
                
                mainImgContainer.addEventListener('mouseleave', () => {
                    mainImgObj.style.transformOrigin = 'center center';
                    mainImgObj.style.transform = 'scale(1)';
                });
                mainImgContainer.addEventListener('mouseenter', () => {
                    mainImgObj.style.transition = 'opacity 0.3s ease, transform 0.1s ease-out';
                });
                
                // Lightbox
                const galleryImages = [
                    '//bizweb.dktcdn.net/thumb/large/100/543/817/products/mini-pc-asus-nuc-ai-350-pn54-ryzen-ai-7-350-gaming.jpg?v=1763971973973',
                    '//bizweb.dktcdn.net/thumb/large/100/543/817/products/w692-01a37475-f53f-4188-84a0-d46b8f01d6d6.png',
                    '//bizweb.dktcdn.net/thumb/large/100/543/817/products/bia1-fc2ef492-2792-4c14-9b3f-5c7d6995afdc.png',
                    '//bizweb.dktcdn.net/thumb/large/100/543/817/products/asus-nuc-ai-350.jpg',
                    '//bizweb.dktcdn.net/thumb/large/100/543/817/products/asus-nuc-ai-350-2.jpg'
                ];
                let currentLightboxIndex = 0;
                
                function openLightbox() {
                    let lightbox = document.getElementById('nava-lightbox');
                    if (!lightbox) {
                        lightbox = document.createElement('div');
                        lightbox.id = 'nava-lightbox';
                        lightbox.innerHTML = `
                            <div style="position: fixed; inset: 0; background: rgba(0,0,0,0.9); z-index: 10000; display: flex; align-items: center; justify-content: center; backdrop-filter: blur(8px); opacity: 0; transition: opacity 0.3s;">
                                <button onclick="closeLightbox()" style="position: absolute; top: 20px; right: 20px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: white; width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; font-size: 1.5rem; transition: 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.2)'" onmouseout="this.style.background='rgba(255,255,255,0.1)'"><i class="ph ph-x"></i></button>
                                <button onclick="event.stopPropagation(); navigateLightbox(-1)" style="position: absolute; left: 20px; top: 50%; transform: translateY(-50%); background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: white; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; font-size: 1.5rem; transition: 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.2)'" onmouseout="this.style.background='rgba(255,255,255,0.1)'"><i class="ph-bold ph-caret-left"></i></button>
                                <img id="lightbox-img" src="" style="max-width: 90%; max-height: 90vh; object-fit: contain; transition: 0.3s; transform: scale(0.95); opacity: 0;" onclick="event.stopPropagation();">
                                <button onclick="event.stopPropagation(); navigateLightbox(1)" style="position: absolute; right: 20px; top: 50%; transform: translateY(-50%); background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: white; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; font-size: 1.5rem; transition: 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.2)'" onmouseout="this.style.background='rgba(255,255,255,0.1)'"><i class="ph-bold ph-caret-right"></i></button>
                                <div id="lightbox-counter" style="position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); color: rgba(255,255,255,0.6); font-weight: 600; letter-spacing: 2px;"></div>
                            </div>
                        `;
                        lightbox.querySelector('div').onclick = closeLightbox; // close when clicking background
                        document.body.appendChild(lightbox);
                    }
                    
                    const currentSrc = mainImgObj.src;
                    currentLightboxIndex = galleryImages.findIndex(src => currentSrc.includes(src.split('?')[0]));
                    if(currentLightboxIndex === -1) currentLightboxIndex = 0;
                    
                    const lightboxDiv = lightbox.querySelector('div');
                    lightbox.style.display = 'block';
                    void lightboxDiv.offsetWidth; // trigger reflow
                    lightboxDiv.style.opacity = '1';
                    
                    updateLightboxImage();
                    document.body.style.overflow = 'hidden';
                }
                
                function closeLightbox() {
                    const lightbox = document.getElementById('nava-lightbox');
                    if (!lightbox) return;
                    const lightboxDiv = lightbox.querySelector('div');
                    lightboxDiv.style.opacity = '0';
                    setTimeout(() => {
                        lightbox.style.display = 'none';
                        document.body.style.overflow = '';
                    }, 300);
                }
                
                function navigateLightbox(dir) {
                    currentLightboxIndex += dir;
                    if(currentLightboxIndex < 0) currentLightboxIndex = galleryImages.length - 1;
                    if(currentLightboxIndex >= galleryImages.length) currentLightboxIndex = 0;
                    updateLightboxImage();
                }
                
                function updateLightboxImage() {
                    const lightboxImg = document.getElementById('lightbox-img');
                    const counter = document.getElementById('lightbox-counter');
                    lightboxImg.style.opacity = '0';
                    lightboxImg.style.transform = 'scale(0.95)';
                    
                    setTimeout(() => {
                        lightboxImg.src = galleryImages[currentLightboxIndex];
                        counter.textContent = `${currentLightboxIndex + 1} / ${galleryImages.length}`;
                        lightboxImg.onload = () => {
                            lightboxImg.style.opacity = '1';
                            lightboxImg.style.transform = 'scale(1)';
                        };
                    }, 200);
                }
            </script>
        </div>
    """
    full_html = clean_liquid_tags(header_part + product_html + local_footer_part)
    
    # Inject sticky compare bar HTML from post_build.py
    try:
        with open("post_build.py", "r", encoding="utf-8") as f:
            pb_content = f.read()
            start_idx = pb_content.find('sticky_compare_html = """') + len('sticky_compare_html = """')
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

    with open(os.path.join(base_dir, "demo_product.html"), "w", encoding="utf-8") as f:
        f.write(full_html)

def build_auth_pages(base_dir):
    # CSS & Boilerplate for Glassmorphism Fullscreen Auth Pages
    auth_css = """
        <style>
            :root {
                --primary: #0ea5e9;
                --secondary: #3b82f6;
                --bg-white: #ffffff;
                --bg-gray: #f8fafc;
                --text-color: #0f172a;
                --text-gray: #64748b;
                --border-color: #e2e8f0;
                --radius-md: 12px;
                --radius-lg: 24px;
            }
            body {
                margin: 0;
                padding: 0;
                overflow: hidden;
                font-family: 'Plus Jakarta Sans', sans-serif;
                background: var(--bg-gray);
                color: var(--text-dark);
                -webkit-font-smoothing: antialiased;
            }
            .auth-page-wrapper {
                height: 100vh;
                width: 100vw;
                display: flex;
                align-items: center;
                justify-content: center;
                background: linear-gradient(45deg, #020617, #0f172a, #0b1120, #172554);
                background-size: 400% 400%;
                animation: gradientBG 15s ease infinite;
                padding: 10px;
                box-sizing: border-box;
                position: relative;
            }
            @keyframes gradientBG {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            .auth-page-wrapper::before {
                content: '';
                position: absolute;
                inset: 0;
                background-image: radial-gradient(rgba(255, 255, 255, 0.05) 1px, transparent 1px);
                background-size: 30px 30px;
                pointer-events: none;
            }
            .glass-card {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.8);
                border-radius: var(--radius-lg);
                padding: 30px 40px;
                width: 100%;
                max-width: 440px;
                max-height: 95vh;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
                position: relative;
                z-index: 10;
                overflow-y: auto;
                scrollbar-width: none; /* Firefox */
            }
            .glass-card::-webkit-scrollbar {
                display: none; /* Chrome */
            }
            .glass-card::before {
                content: '';
                position: absolute;
                top: 0; left: 0; width: 100%; height: 4px;
                background: linear-gradient(90deg, var(--primary), var(--secondary), var(--primary));
                background-size: 200% 100%;
                animation: gradientMove 3s linear infinite;
            }
            @keyframes gradientMove {
                0% { background-position: 100% 0; }
                100% { background-position: -100% 0; }
            }
            .auth-title {
                font-size: 1.8rem;
                font-weight: 800;
                color: var(--text-dark);
                text-align: center;
                margin: 0 0 5px 0;
            }
            .auth-desc {
                text-align: center;
                color: var(--text-gray);
                margin: 0 0 20px 0;
                font-size: 0.9rem;
            }
            .form-group-nava {
                margin-bottom: 15px;
                position: relative;
            }
            .form-group-nava i {
                position: absolute;
                left: 15px;
                top: 50%;
                transform: translateY(-50%);
                color: var(--text-gray);
                font-size: 1.1rem;
            }
            .input-nava {
                width: 100%;
                padding: 12px 15px 12px 42px;
                border: 1px solid var(--border-color);
                border-radius: var(--radius-md);
                background: #f8fafc;
                color: var(--text-dark);
                font-size: 0.95rem;
                outline: none;
                transition: all 0.3s;
                box-sizing: border-box;
            }
            .input-nava:focus {
                border-color: var(--primary);
                box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.15);
                background: #fff;
            }
            .btn-nava {
                width: 100%;
                padding: 12px;
                border-radius: var(--radius-md);
                border: none;
                font-size: 1.05rem;
                font-weight: 700;
                cursor: pointer;
                transition: all 0.3s;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
            }
            .btn-primary-nava {
                background: linear-gradient(90deg, var(--primary), var(--secondary));
                color: white;
                box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3);
            }
            .btn-primary-nava:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 20px rgba(14, 165, 233, 0.4);
            }
            .social-divider {
                display: flex;
                align-items: center;
                text-align: center;
                margin: 20px 0;
                color: var(--text-gray);
                font-size: 0.85rem;
            }
            .social-divider::before, .social-divider::after {
                content: '';
                flex: 1;
                border-bottom: 1px solid var(--border-color);
            }
            .social-divider span {
                padding: 0 10px;
            }
            .social-login-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 12px;
            }
            .btn-social {
                background: white;
                border: 1px solid var(--border-color);
                color: var(--text-dark);
                font-size: 0.95rem;
                padding: 10px;
            }
            .btn-social:hover {
                background: var(--bg-gray);
                border-color: #cbd5e1;
            }
            .link-nava {
                color: var(--primary);
                text-decoration: none;
                font-weight: 600;
                transition: 0.2s;
            }
            .link-nava:hover {
                text-decoration: underline;
            }
            
            /* Toggle forms */
            #recover_customer_password { display: none; }
            .show-recover #customer_login_wrapper { display: none; }
            .show-recover #recover_customer_password { display: block; }
        </style>
    """

    header_wrapper = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nava Store - Đăng Nhập / Đăng Ký</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/@phosphor-icons/web"></script>
    {auth_css}
</head>
<body>
"""

    footer_wrapper = "</body></html>"

    # 1. Login HTML
    login_html = header_wrapper + """
        <div class="auth-page-wrapper" id="login-container">
            <div class="glass-card">
                <a href="demo_collection.html" class="link-nava" style="position: absolute; top: 25px; left: 25px; display: inline-flex; align-items: center; gap: 5px; font-size: 0.85rem;"><i class="ph-bold ph-arrow-left"></i> Quay lại</a>
                
                <!-- Main Login Form -->
                <div id="customer_login_wrapper">
                    <div style="text-align: center; margin-top: 10px;">
                        <img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/logo.png?1775454528082" alt="Nava Store" style="height: 45px; margin-bottom: 15px;">
                        <h1 class="auth-title">Đăng Nhập</h1>
                        <p class="auth-desc">Chào mừng bạn quay trở lại Nava Store</p>
                    </div>
                    
                    <form method="post" action="/account/login" id="customer_login" accept-charset="UTF-8">
                        <input name="FormType" type="hidden" value="customer_login"/>
                        <input name="utf8" type="hidden" value="true"/>
                        
                        <div class="form-group-nava">
                            <i class="ph-bold ph-envelope"></i>
                            <input type="email" placeholder="Nhập địa chỉ Email" class="input-nava" pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$" name="email" id="customer_email" required>
                        </div>
                        
                        <div class="form-group-nava">
                            <i class="ph-bold ph-lock"></i>
                            <input type="password" placeholder="Mật khẩu" class="input-nava" name="password" id="customer_password" required>
                        </div>
                        
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
                            <label style="display: flex; align-items: center; gap: 8px; cursor: pointer; color: var(--text-gray); font-size: 0.95rem;">
                                <input type="checkbox" style="width: 16px; height: 16px; accent-color: var(--primary);">
                                Ghi nhớ đăng nhập
                            </label>
                            <a href="#recover" onclick="toggleRecover(); return false;" class="link-nava">Quên mật khẩu?</a>
                        </div>
                        
                        <button type="submit" class="btn-nava btn-primary-nava">Đăng Nhập Ngay</button>
                    </form>
                    
                    <div class="social-divider"><span>HOẶC ĐĂNG NHẬP BẰNG</span></div>
                    
                    <div class="social-login-grid">
                        <button class="btn-nava btn-social" onclick="if(typeof loginGoogle === 'function') loginGoogle(); else alert('Chức năng Google Auth đang giả lập trên Sapo.'); return false;">
                            <img src="https://images.seeklogo.com/logo-png/27/2/google-logo-png_seeklogo-273191.png" width="18" height="18" alt="Google"> Google
                        </button>
                        <button class="btn-nava btn-social" onclick="if(typeof loginFacebook === 'function') loginFacebook(); else alert('Chức năng Facebook Auth đang giả lập trên Sapo.'); return false;" style="color: #1877F2;">
                            <i class="ph-fill ph-facebook-logo" style="font-size: 1.2rem;"></i> Facebook
                        </button>
                    </div>
                    
                    <p style="text-align: center; margin-top: 20px; color: var(--text-gray); font-size: 0.95rem;">
                        Chưa có tài khoản? <a href="demo_register.html" class="link-nava">Đăng ký ngay</a>
                    </p>
                </div>

                <!-- Recover Password Form -->
                <form method="post" action="/account/recover" id="recover_customer_password" accept-charset="UTF-8">
                    <input name="FormType" type="hidden" value="recover_customer_password"/>
                    <input name="utf8" type="hidden" value="true"/>
                    
                    <div style="text-align: center; margin-top: 10px;">
                        <img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/logo.png?1775454528082" alt="Nava Store" style="height: 45px; margin-bottom: 15px;">
                        <h1 class="auth-title">Quên Mật Khẩu</h1>
                        <p class="auth-desc">Chúng tôi sẽ gửi một email kèm liên kết để bạn đặt lại mật khẩu an toàn.</p>
                    </div>
                    
                    <div class="form-group-nava">
                        <i class="ph-bold ph-envelope"></i>
                        <input type="email" class="input-nava" placeholder="Nhập Email của bạn" pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$" name="email" id="customer_email1" required>
                    </div>
                    
                    <button type="submit" class="btn-nava btn-primary-nava" style="margin-top: 5px;">Gửi Liên Kết Khôi Phục</button>
                    
                    <p style="text-align: center; margin-top: 20px;">
                        <a href="#" onclick="toggleRecover(); return false;" class="link-nava"><i class="ph-bold ph-arrow-left"></i> Quay lại đăng nhập</a>
                    </p>
                </form>
                
            </div>
        </div>

        <script>
            function toggleRecover() {
                const container = document.getElementById('login-container');
                container.classList.toggle('show-recover');
            }
            if (window.location.hash == "#recover") { toggleRecover(); }
        </script>
    """ + footer_wrapper
    
    with open(os.path.join(base_dir, "demo_login.html"), "w", encoding="utf-8") as f:
        f.write(login_html)

    # 2. Register HTML
    register_html = header_wrapper + """
        <div class="auth-page-wrapper">
            <div class="glass-card">
                <a href="demo_collection.html" class="link-nava" style="position: absolute; top: 25px; left: 25px; display: inline-flex; align-items: center; gap: 5px; font-size: 0.85rem;"><i class="ph-bold ph-arrow-left"></i> Quay lại</a>
                <div style="text-align: center; margin-top: 10px;">
                    <img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/logo.png?1775454528082" alt="Nava Store" style="height: 45px; margin-bottom: 15px;">
                    <h1 class="auth-title">Tạo Tài Khoản</h1>
                    <p class="auth-desc">Đăng ký thành viên để nhận ngay nhiều ưu đãi</p>
                </div>
                
                <form method="post" action="/account/register" id="customer_register" accept-charset="UTF-8">
                    <input name="FormType" type="hidden" value="customer_register"/>
                    <input name="utf8" type="hidden" value="true"/>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px;">
                        <div style="position: relative;">
                            <i class="ph-bold ph-user" style="position: absolute; left: 15px; top: 50%; transform: translateY(-50%); color: var(--text-gray); font-size: 1.1rem;"></i>
                            <input type="text" placeholder="Họ" class="input-nava" name="lastName" required>
                        </div>
                        <div style="position: relative;">
                            <input type="text" placeholder="Tên" class="input-nava" style="padding-left: 15px;" name="firstName" required>
                        </div>
                    </div>
                    
                    <div class="form-group-nava">
                        <i class="ph-bold ph-phone"></i>
                        <input type="text" placeholder="Số điện thoại" class="input-nava" pattern="\\d+" name="Phone" required>
                    </div>
                    
                    <div class="form-group-nava">
                        <i class="ph-bold ph-envelope"></i>
                        <input type="email" placeholder="E-mail" class="input-nava" pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$" name="email" required>
                    </div>
                    
                    <div class="form-group-nava">
                        <i class="ph-bold ph-lock"></i>
                        <input type="password" placeholder="Mật khẩu" class="input-nava" name="password" required>
                    </div>
                    
                    <button type="submit" class="btn-nava btn-primary-nava" style="margin-top: 5px;">Đăng Ký Tài Khoản</button>
                </form>
                
                <div class="social-divider"><span>HOẶC ĐĂNG NHẬP BẰNG</span></div>
                
                <div class="social-login-grid">
                    <button class="btn-nava btn-social" onclick="if(typeof loginGoogle === 'function') loginGoogle(); else alert('Chức năng Google Auth đang giả lập trên Sapo.'); return false;">
                        <img src="https://images.seeklogo.com/logo-png/27/2/google-logo-png_seeklogo-273191.png" width="18" height="18" alt="Google"> Google
                    </button>
                    <button class="btn-nava btn-social" onclick="if(typeof loginFacebook === 'function') loginFacebook(); else alert('Chức năng Facebook Auth đang giả lập trên Sapo.'); return false;" style="color: #1877F2;">
                        <i class="ph-fill ph-facebook-logo" style="font-size: 1.2rem;"></i> Facebook
                    </button>
                </div>
                
                <p style="text-align: center; margin-top: 20px; color: var(--text-gray); font-size: 0.95rem;">
                    Đã có tài khoản? <a href="demo_login.html" class="link-nava">Đăng nhập</a>
                </p>
            </div>
        </div>
    """ + footer_wrapper
    
    with open(os.path.join(base_dir, "demo_register.html"), "w", encoding="utf-8") as f:
        f.write(register_html)

def build_compare_page(base_dir, header_part, footer_part):
    # Extract sticky stuff from index.bwt like others
    sticky_stuff = ""
    with open(os.path.join(base_dir, "index.bwt"), "r", encoding="utf-8") as f:
        idx_content = f.read()
        if "<!-- Mobile Sidebar Drawer -->" in idx_content:
            sticky_stuff = idx_content[idx_content.find("<!-- Mobile Sidebar Drawer -->"):]
            if "<!-- /MASTER SAPO ESCAPE WRAPPER -->" in sticky_stuff:
                sticky_stuff = sticky_stuff.split("<!-- /MASTER SAPO ESCAPE WRAPPER -->")[0]
                
    local_footer_part = sticky_stuff + '<script src="assets/main.js" defer></script>\n' + footer_part

    compare_html = """
        <style>
            .compare-page { padding: 40px 15px; max-width: 1200px; margin: 100px auto 40px; }
            .compare-hero { text-align: center; margin-bottom: 40px; }
            .compare-hero h1 { font-size: 2.5rem; font-weight: 800; color: var(--text-dark); margin-bottom: 10px; background: linear-gradient(135deg, var(--primary), var(--secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
            .compare-hero p { color: var(--text-gray); font-size: 1.1rem; }
            
            .compare-grid { display: grid; grid-template-columns: 250px 1fr 1fr; background: var(--bg-white); border-radius: var(--radius-lg); overflow: hidden; box-shadow: var(--shadow-sm); border: 1px solid var(--border-color); }
            
            /* Header Row */
            .compare-row-header { display: contents; }
            .compare-cell-header { padding: 30px 20px; text-align: center; border-bottom: 2px solid var(--border-color); border-right: 1px solid var(--border-color); background: var(--bg-gray); position: relative; }
            .compare-cell-header:last-child { border-right: none; }
            .compare-cell-header.empty { background: var(--bg-white); border-right: 1px solid var(--border-color); display: flex; align-items: center; justify-content: center;}
            
            .compare-prod-img { width: 140px; height: 140px; object-fit: contain; margin-bottom: 15px; mix-blend-mode: multiply; transition: transform 0.3s; }
            .compare-prod-img:hover { transform: translateY(-5px); }
            .compare-prod-title { font-weight: 800; font-size: 1.2rem; color: var(--text-dark); margin-bottom: 8px; }
            .compare-prod-price { font-weight: 900; font-size: 1.4rem; color: var(--primary); margin-bottom: 15px; }
            
            /* Data Rows */
            .compare-row { display: contents; }
            .compare-row:hover .compare-cell { background: rgba(14, 165, 233, 0.02); }
            .compare-cell { padding: 20px; border-bottom: 1px solid var(--border-color); border-right: 1px solid var(--border-color); font-size: 0.95rem; color: var(--text-dark); display: flex; align-items: center; justify-content: center; text-align: center; }
            .compare-cell:last-child { border-right: none; }
            .compare-label { background: #f8fafc; font-weight: 700; color: var(--text-gray); justify-content: flex-start; text-align: left; text-transform: uppercase; letter-spacing: 0.5px; font-size: 0.85rem; }
            
            .highlight-cell { background: rgba(16, 185, 129, 0.05); color: #059669; font-weight: 700; }
            .compare-row:hover .highlight-cell { background: rgba(16, 185, 129, 0.08); }
            
            .remove-btn { position: absolute; top: 15px; right: 15px; width: 30px; height: 30px; border-radius: 50%; background: #fee2e2; color: #ef4444; display: flex; align-items: center; justify-content: center; cursor: pointer; border: none; transition: all 0.2s; }
            .remove-btn:hover { background: #ef4444; color: white; }
            
            @media (max-width: 768px) {
                .compare-grid { grid-template-columns: 100px 1fr 1fr; }
                .compare-label { font-size: 0.75rem; padding: 10px; }
                .compare-cell { font-size: 0.85rem; padding: 10px; }
                .compare-prod-img { width: 80px; height: 80px; }
                .compare-prod-title { font-size: 1rem; }
                .compare-prod-price { font-size: 1.1rem; }
            }
        </style>
        
        <div class="compare-page">
            <div class="breadcrumb" style="background: transparent; padding: 0; margin-bottom: 20px; justify-content: center;">
                <a href="/" style="color: var(--text-gray); text-decoration: none;"><i class="ph ph-house"></i> Trang chủ</a> 
                <span style="margin: 0 10px; color: var(--text-gray);">/</span> 
                <span style="color: var(--primary); font-weight: bold;">So sánh sản phẩm</span>
            </div>
            
            <div class="compare-hero">
                <h1>So Sánh Sản Phẩm</h1>
                <p>Khám phá sự khác biệt để lựa chọn cấu hình phù hợp nhất với bạn</p>
            </div>
            
            <div class="compare-grid">
                <!-- Header -->
                <div class="compare-row-header">
                    <div class="compare-cell-header empty">
                        <button class="btn-pill" style="border: 2px dashed var(--border-color); background: transparent; color: var(--text-gray); border-radius: var(--radius-md); padding: 10px 15px; display: flex; align-items: center; gap: 5px; font-weight: 600; cursor: pointer;"><i class="ph-bold ph-plus"></i> Thêm SP</button>
                    </div>
                    <div class="compare-cell-header">
                        <button class="remove-btn" title="Xóa khỏi so sánh"><i class="ph-bold ph-x"></i></button>
                        <img src="//bizweb.dktcdn.net/thumb/large/100/543/817/products/mini-pc-asus-nuc-ai-350-pn54-ryzen-ai-7-350-gaming.jpg?v=1763971973973" alt="ASUS NUC" class="compare-prod-img">
                        <div class="compare-prod-title">ASUS NUC AI 350</div>
                        <div class="compare-prod-price">12.390.000₫</div>
                        <a href="demo_product.html" class="btn-pill btn-blue" style="width: 100%; border-radius: var(--radius-md); padding: 12px; font-weight: bold; text-decoration: none; display: block; box-sizing: border-box;">Mua ngay</a>
                    </div>
                    <div class="compare-cell-header">
                        <button class="remove-btn" title="Xóa khỏi so sánh"><i class="ph-bold ph-x"></i></button>
                        <img src="https://bizweb.dktcdn.net/thumb/large/100/543/817/products/minisforum-um880-pro.jpg?v=1723521250260" alt="UM890 PRO" class="compare-prod-img">
                        <div class="compare-prod-title">MINISFORUM UM890 Pro</div>
                        <div class="compare-prod-price">14.990.000₫</div>
                        <button class="btn-pill" style="width: 100%; border-radius: var(--radius-md); padding: 12px; font-weight: bold; background: rgba(14, 165, 233, 0.1); color: var(--primary); border: 2px solid var(--primary); cursor: pointer;">Mua ngay</button>
                    </div>
                </div>
                
                <!-- Specs -->
                <div class="compare-row">
                    <div class="compare-cell compare-label">Vi xử lý (CPU)</div>
                    <div class="compare-cell highlight-cell"><i class="ph-fill ph-cpu" style="margin-right: 5px;"></i> AMD Ryzen™ AI 7 350</div>
                    <div class="compare-cell">AMD Ryzen™ 9 8945HS</div>
                </div>
                
                <div class="compare-row">
                    <div class="compare-cell compare-label">Đồ họa (GPU)</div>
                    <div class="compare-cell highlight-cell">Radeon™ 860M (RDNA 3.5)</div>
                    <div class="compare-cell">Radeon™ 780M (RDNA 3)</div>
                </div>
                
                <div class="compare-row">
                    <div class="compare-cell compare-label">NPU (Xử lý AI)</div>
                    <div class="compare-cell highlight-cell">Lên đến 50 TOPS</div>
                    <div class="compare-cell">Lên đến 39 TOPS</div>
                </div>
                
                <div class="compare-row">
                    <div class="compare-cell compare-label">Hỗ trợ RAM</div>
                    <div class="compare-cell">DDR5 Dual 5600MHz (Max 96GB)</div>
                    <div class="compare-cell highlight-cell">DDR5 Dual 5600MHz (Max 96GB)</div>
                </div>
                
                <div class="compare-row">
                    <div class="compare-cell compare-label">Lưu trữ (SSD)</div>
                    <div class="compare-cell">2x M.2 2280 PCIe 4.0 x4</div>
                    <div class="compare-cell highlight-cell">2x M.2 2280 PCIe 4.0 x4</div>
                </div>
                
                <div class="compare-row">
                    <div class="compare-cell compare-label">Cổng kết nối đặc biệt</div>
                    <div class="compare-cell">Wi-Fi 6E, Bluetooth 5.3</div>
                    <div class="compare-cell highlight-cell"><i class="ph-bold ph-plugs" style="margin-right: 5px;"></i> Cổng OCuLink 64Gbps (Gắn eGPU)</div>
                </div>
                
                <div class="compare-row">
                    <div class="compare-cell compare-label">Bảo hành</div>
                    <div class="compare-cell highlight-cell"><i class="ph-fill ph-shield-check" style="margin-right: 5px;"></i> 36 tháng chính hãng ASUS</div>
                    <div class="compare-cell">12 tháng MINISFORUM</div>
                </div>
            </div>
        </div>
    """
    full_html = clean_liquid_tags(header_part + compare_html + local_footer_part)
    with open(os.path.join(base_dir, "demo_compare.html"), "w", encoding="utf-8") as f:
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
    
    build_compare_page(base_dir, header_part, footer_part)
    print("Generated demo_compare.html successfully!")
    
    build_auth_pages(base_dir)
    print("Generated demo_login.html and demo_register.html successfully!")

if __name__ == "__main__":
    build_all()
