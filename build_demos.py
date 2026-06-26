import os
import re

def resolve_conditionals(text, template='index'):
    def eval_cond(cond_str):
        cond_str = cond_str.strip()
        if "template contains" in cond_str:
            val = cond_str.split("contains")[-1].strip().strip("'\"")
            return val in template
        if "template ==" in cond_str:
            val = cond_str.split("==")[-1].strip().strip("'\"")
            return template == val
        if "template !=" in cond_str:
            val = cond_str.split("!=")[-1].strip().strip("'\"")
            return template != val
        if "settings.use_sapo_app" in cond_str:
            return False
        if "settings.ena_popup_news" in cond_str:
            return False
        if "settings.ena_isocial_bubble" in cond_str:
            return False
        if "customer" in cond_str:
            return False
        return False

    tokens = re.split(r'({%-?\s*.*?\s*-?%})', text)
    output = []
    stack = []
    
    for token in tokens:
        if token.startswith('{%') and token.endswith('%}'):
            tag_content = token[2:-2].strip()
            if tag_content.startswith('-'): tag_content = tag_content[1:]
            if tag_content.endswith('-'): tag_content = tag_content[:-1]
            tag_content = tag_content.strip()
            
            parts = tag_content.split(None, 1)
            cmd = parts[0] if parts else ""
            args = parts[1] if len(parts) > 1 else ""
            
            if cmd == 'if' or cmd == 'unless':
                parent_active = stack[-1][0] if stack else True
                cond_val = eval_cond(args)
                if cmd == 'unless':
                    cond_val = not cond_val
                
                is_executed = parent_active and cond_val
                stack.append([is_executed, is_executed, parent_active])
            elif cmd == 'elsif':
                if stack:
                    parent_active = stack[-1][2]
                    has_run = stack[-1][1]
                    if parent_active and not has_run:
                        cond_val = eval_cond(args)
                        stack[-1][0] = cond_val
                        stack[-1][1] = cond_val or has_run
                    else:
                        stack[-1][0] = False
            elif cmd == 'else':
                if stack:
                    parent_active = stack[-1][2]
                    has_run = stack[-1][1]
                    stack[-1][0] = parent_active and not has_run
            elif cmd == 'endif' or cmd == 'endunless':
                if stack:
                    stack.pop()
            else:
                current_active = stack[-1][0] if stack else True
                if current_active:
                    output.append(token)
        else:
            current_active = stack[-1][0] if stack else True
            if current_active:
                output.append(token)
                
    return "".join(output)

def clean_liquid_tags(text, template='index'):
    text = re.sub(r'{%\s*comment\s*%}.*?{%\s*endcomment\s*%}', '', text, flags=re.DOTALL)
    
    # Evaluate conditionals
    text = resolve_conditionals(text, template)
    
    # Convert asset_url and img_url liquid tags to static URLs
    def replace_asset(match):
        filename = match.group(1)
        full_tag = match.group(0)
        url = f"assets/{filename}"
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

    # Remove any broken/empty meta keywords tags
    text = re.sub(r'<meta name="keywords" content="[^"]*"\s*/?>', '', text)

    return text

def inject_seo_metadata(html, title, description, keywords):
    # 1. Replace title tag
    if "<title>" in html:
        html = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', html, flags=re.DOTALL)
    else:
        html = html.replace('<head>', f'<head>\n    <title>{title}</title>')
        
    # 2. Replace description tag
    desc_tag = f'<meta name="description" content="{description}">'
    if 'name="description"' in html:
        html = re.sub(r'<meta\s+name="description"\s+content="[^"]*"\s*/?>', desc_tag, html)
        html = re.sub(r'<meta\s+content="[^"]*"\s+name="description"\s*/?>', desc_tag, html)
    else:
        if f'<title>{title}</title>' in html:
            html = html.replace(f'<title>{title}</title>', f'<title>{title}</title>\n    {desc_tag}')
        else:
            html = html.replace('</head>', f'    {desc_tag}\n</head>')
            
    # 3. Inject keywords tag
    keywords_tag = f'<meta name="keywords" content="{keywords}">'
    if desc_tag in html:
        html = html.replace(desc_tag, f'{desc_tag}\n    {keywords_tag}')
    else:
        html = html.replace('</head>', f'    {keywords_tag}\n</head>')
        
    return html

def get_core_layout(base_dir):
    with open(os.path.join(base_dir, "theme.bwt"), "r", encoding="utf-8") as f:
        theme = f.read()
        
    # Force stylesheet and fonts block to be kept for all templates in local compilation
    theme_norm = theme.replace('\r\n', '\n')
    theme_norm = theme_norm.replace(
        "            {%- if template contains 'index' -%}\n            <!-- Google Fonts Optimized -->",
        "            <!-- Google Fonts Optimized -->"
    )
    theme_norm = theme_norm.replace(
        "            </script>\n            {%- endif -%}",
        "            </script>"
    )
    theme = theme_norm.replace('\n', os.linesep)

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
    if "</body>" in footer_part:
        footer_part = footer_part.replace("</body>", f"{demo_auth_interceptor}\n</body>")
    elif "</html>" in footer_part:
        footer_part = footer_part.replace("</html>", f"{demo_auth_interceptor}\n</html>")
    else:
        footer_part += demo_auth_interceptor
    
    return header_part, footer_part

def build_index(base_dir, header_part, footer_part):
    with open(os.path.join(base_dir, "index.bwt"), "r", encoding="utf-8") as f:
        index_content = f.read()
        
    full_index = header_part.replace(open(os.path.join(base_dir, "extracted_header.html"), "r", encoding="utf-8").read(), "") + index_content + footer_part
    full_index = clean_liquid_tags(full_index, 'index')
    full_index = inject_seo_metadata(
        full_index, 
        title="Nava Store - Mini PC & eGPU Chính Hãng", 
        description="Nava Store chuyên cung cấp các dòng sản phẩm Mini PC, eGPU, RAM, SSD, linh kiện máy tính chính hãng chất lượng cao.", 
        keywords="Mini PC, eGPU, Asus NUC, Minisforum, Beelink, Nava Store"
    )
    
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
        <div class="container" id="nava-col-container" style="max-width: 1600px !important; width: 100% !important; box-sizing: border-box !important; margin: 0 auto !important; padding: 10px 30px 80px;">
            <div class="breadcrumb" style="background: transparent; padding: 0; margin-bottom: 25px; font-size: 0.95rem;">
                <a href="/" style="color: var(--text-gray); text-decoration: none; display: inline-flex; align-items: center; gap: 5px;"><i class="ph ph-house"></i> Trang chủ</a> 
                <span style="margin: 0 10px; color: var(--text-gray);">/</span> 
                <span style="color: var(--primary); font-weight: bold;">ASUS NUC</span>
            </div>

            <!-- Techy Hero Banner -->
            <div class="collection-hero" style="background: linear-gradient(135deg, rgba(14,165,233,0.1) 0%, rgba(15,23,42,0.02) 100%); border-radius: var(--radius-lg); padding: 40px 50px; margin-top: 25px; margin-bottom: 40px; border: 1px solid var(--border-color); position: relative; overflow: hidden; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 10px 30px rgba(0,0,0,0.02);">
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
                .category-list li { margin-bottom: 12px; }
                .category-list a { display: flex; align-items: center; width: 100%; color: var(--text-dark); text-decoration: none; font-weight: 600; font-size: 0.95rem; transition: color 0.2s; }
                .category-list a:hover, .category-list a.active { color: var(--primary); }
                .category-list .cat-name { flex: 1; margin-right: 10px; text-align: left; }
                .category-list .count { background: #f1f5f9 !important; color: #64748b !important; font-size: 0.72rem !important; font-weight: 700 !important; padding: 2px 8px !important; border-radius: 12px !important; min-width: 22px !important; height: 18px !important; display: inline-flex !important; align-items: center !important; justify-content: center !important; box-sizing: border-box !important; line-height: 1 !important; margin-left: 0 !important; transition: all 0.2s !important; }
                .category-list a:hover .count { background: rgba(37, 99, 235, 0.1) !important; color: var(--primary) !important; }
                .parent-cat .caret-icon { margin-left: 6px; color: #94a3b8; transition: transform 0.2s, color 0.2s; }
                .parent-cat:hover .caret-icon { color: var(--primary); }
                
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
                .spec-pill { background: var(--bg-gray); color: var(--text-gray); border: 1px solid var(--border-color); padding: 4px 8px; border-radius: 6px; font-size: 0.7rem; font-weight: 600; display: inline-block; white-space: nowrap; box-shadow: none; }
                .spec-pill.secondary { background: var(--bg-gray); color: var(--text-gray); border: 1px solid var(--border-color); box-shadow: none; font-weight: 600; }
                .card-title { height: 2.8em; line-height: 1.4; overflow: hidden; font-size: 1rem; font-weight: 700; margin-bottom: 10px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; color: var(--text-dark); transition: color 0.2s; }
                .product-card:hover .card-title { color: var(--primary); }
                
                .product-card { transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease; border: 1px solid var(--border-color); border-radius: var(--radius-lg); overflow: hidden; background: var(--bg-white) !important; }
                .product-card .card-glow { display: none !important; }
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
                
                .product-img { transition: transform 0.4s ease; filter: none !important; }
                .product-card:hover .product-img { transform: scale(1.05); filter: none !important; }
                
                /* Collapsible Category Description Section */
                .category-description-section {
                    margin-top: 50px;
                    border-top: 1px solid var(--border-color);
                    padding-top: 40px;
                    padding-bottom: 50px;
                    position: relative;
                    width: 100%;
                    box-sizing: border-box;
                }
                .cat-desc-wrapper {
                    max-height: 220px;
                    overflow: hidden;
                    position: relative;
                    transition: max-height 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                }
                .cat-desc-wrapper.expanded {
                    max-height: 2000px;
                }
                .cat-desc-fade {
                    position: absolute;
                    bottom: 0;
                    left: 0;
                    width: 100%;
                    height: 100px;
                    background: linear-gradient(to bottom, transparent, var(--bg-white, #ffffff));
                    pointer-events: none;
                    transition: opacity 0.3s ease;
                }
                .cat-desc-wrapper.expanded .cat-desc-fade {
                    opacity: 0;
                }
                .btn-cat-more {
                    background: var(--bg-white);
                    border: 1px solid var(--primary);
                    color: var(--primary);
                    font-weight: 700;
                    padding: 10px 28px;
                    border-radius: 20px;
                    cursor: pointer;
                    transition: all 0.3s;
                    font-size: 0.9rem;
                    display: inline-flex;
                    align-items: center;
                    gap: 6px;
                    box-shadow: 0 4px 10px rgba(14,165,233,0.05);
                }
                .btn-cat-more:hover {
                    background: var(--primary);
                    color: #fff;
                    box-shadow: 0 6px 16px rgba(14,165,233,0.25);
                }
                
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
                    .card-title { font-size: 0.85rem !important; height: auto !important; max-height: 36px !important; margin-bottom: 6px !important; display: -webkit-box !important; -webkit-line-clamp: 2 !important; -webkit-box-orient: vertical !important; overflow: hidden !important; }
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
                <div class="nava-sidebar" data-lenis-prevent>
                    <div class="filter-sidebar" style="background: var(--bg-white); padding: 25px 20px; border-radius: var(--radius-lg); border: 1px solid var(--border-color); box-shadow: var(--shadow-sm); box-sizing: border-box; width: 100%;">
                        
                        <div class="sidebar-block">
                            <h4 class="sidebar-title">DANH MỤC SẢN PHẨM</h4>
                            <ul class="category-list">
                                <li><a href="demo_collection.html"><img src="//bizweb.dktcdn.net/thumb/small/100/543/817/themes/1000289/assets/icon_dmenu_2.png?1775454528082" style="width:22px;height:22px;object-fit:contain;"> <span class="cat-name">Tất cả sản phẩm</span> <span class="count">229</span></a></li>
                                <li><a href="#" style="color: var(--primary);"><img src="//bizweb.dktcdn.net/thumb/small/100/543/817/themes/1000289/assets/icon_dmenu_3.png?1775454528082" style="width:22px;height:22px;object-fit:contain;"> <span class="cat-name">Mini PC</span> <span class="count">145</span> <i class="ph-bold ph-caret-down caret-icon"></i></a></li>
                                <li><a href="#"><img src="//bizweb.dktcdn.net/thumb/small/100/543/817/themes/1000289/assets/icon_dmenu_4.png?1775454528082" style="width:22px;height:22px;object-fit:contain;"> <span class="cat-name">eGPU</span> <span class="count">14</span> <i class="ph-bold ph-caret-down caret-icon"></i></a></li>
                                <li><a href="#"><img src="//bizweb.dktcdn.net/thumb/small/100/543/817/themes/1000289/assets/icon_dmenu_6.png?1775454528082" style="width:22px;height:22px;object-fit:contain;"> <span class="cat-name">RAM/SSD</span> <span class="count">11</span></a></li>
                                <li><a href="#"><img src="//bizweb.dktcdn.net/thumb/small/100/543/817/themes/1000289/assets/icon_dmenu_6.png?1775454528082" style="width:22px;height:22px;object-fit:contain;"> <span class="cat-name">Màn hình</span> <span class="count">28</span></a></li>
                                <li><a href="#"><img src="//bizweb.dktcdn.net/thumb/small/100/543/817/themes/1000289/assets/icon_dmenu_7.png?1775454528082" style="width:22px;height:22px;object-fit:contain;"> <span class="cat-name">Phụ kiện</span> <span class="count">25</span></a></li>
                                <li><a href="#"><img src="//bizweb.dktcdn.net/thumb/small/100/543/817/themes/1000289/assets/icon_dmenu_8.png?1775454528082" style="width:22px;height:22px;object-fit:contain;"> <span class="cat-name">Like new</span> <span class="count">6</span></a></li>
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
                                    <div class="range-track"><div class="range-fill" id="priceFill" style="left: 0%; right: 0%;"></div></div>
                                    <input type="range" min="0" max="50000000" step="500000" value="0" id="priceMin" oninput="updatePriceVisuals()" onchange="if(typeof applyFiltersAndSort === 'function') applyFiltersAndSort()">
                                    <input type="range" min="0" max="50000000" step="500000" value="50000000" id="priceMax" oninput="updatePriceVisuals()" onchange="if(typeof applyFiltersAndSort === 'function') applyFiltersAndSort()">
                                </div>
                                <div style="display: flex; justify-content: space-between; align-items: center; gap: 10px;">
                                    <input type="text" id="priceInputMin" value="0đ" readonly style="flex: 1; min-width: 0; padding: 8px 4px; border: 1px solid var(--border-color); border-radius: 6px; font-size: 0.85rem; color: var(--text-dark); font-weight: 700; text-align: center; outline: none; box-shadow: inset 0 1px 2px rgba(0,0,0,0.02); background: var(--bg-gray);">
                                    <span style="color: var(--text-gray); flex-shrink: 0; font-weight: bold;">-</span>
                                    <input type="text" id="priceInputMax" value="50.000.000đ" readonly style="flex: 1; min-width: 0; padding: 8px 4px; border: 1px solid var(--border-color); border-radius: 6px; font-size: 0.85rem; color: var(--text-dark); font-weight: 700; text-align: center; outline: none; box-shadow: inset 0 1px 2px rgba(0,0,0,0.02); background: var(--bg-gray);">
                                </div>
                                <script>
                                    function updatePriceVisuals() {
                                        let minVal = parseInt(document.getElementById('priceMin').value);
                                        let maxVal = parseInt(document.getElementById('priceMax').value);
                                        if(minVal > maxVal) { let tmp = minVal; minVal = maxVal; maxVal = tmp; }
                                        document.getElementById('priceInputMin').value = minVal.toLocaleString('vi-VN') + 'đ';
                                        document.getElementById('priceInputMax').value = maxVal.toLocaleString('vi-VN') + 'đ';
                                        const fill = document.getElementById('priceFill');
                                        fill.style.left = (minVal / 50000000 * 100) + '%';
                                        fill.style.right = (100 - (maxVal / 50000000 * 100)) + '%';
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
                                    <input type="text" class="ai-input" id="aiSearchInput" placeholder="Máy chơi được Wukong tầm 15 củ">
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
                                                    <strong>NAVA AI:</strong> Đang xử lý yêu cầu...
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
                                            <div class="ai-result-price" style="background: linear-gradient(135deg, #b45309, #d97706); box-shadow: 0 2px 6px rgba(217,119,6,0.2);">14.200.000đ</div>
                                        </div>
                                    </a>
                                    
                                    <!-- Other Options -->
                                    <div style="padding: 10px 20px 5px; font-size: 0.75rem; color: #94a3b8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; border-top: 1px solid #f1f5f9;">
                                        Các lựa chọn thay thế khác
                                    </div>
                                    <a href="#" class="ai-result-item">
                                        <img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" class="ai-result-img" alt="ASUS NUC">
                                        <div class="ai-result-info"><h5>ASUS NUC 14 Pro Core Ultra 5 (16GB/512GB)</h5><div class="ai-result-price">12.500.000đ</div></div>
                                    </a>
                                    <a href="#" class="ai-view-more">Xem thêm tất cả 8 kết quả &nbsp;<i class="ph-bold ph-arrow-right"></i></a>
                                </div>
                            </div>
                            <script>
                                (function() {
                                    var aiSearchInput = document.getElementById('aiSearchInput');
                                    var btn = document.getElementById('aiSearchBtn');
                                    var drop = document.getElementById('aiResultsDropdown');
                                    var loading = document.getElementById('aiLoading');
                                    var list = document.getElementById('aiResultsList');
                                    var header = document.getElementById('aiResultHeader');
                                    var summary = document.getElementById('aiSummaryText');
                                    var timer = null;
                                    function doSearch() {
                                        var q = aiSearchInput.value.trim();
                                        if (!q) { drop.classList.remove('active'); return; }
                                        drop.classList.add('active');
                                        loading.style.display = 'block';
                                        list.style.display = 'none';
                                        header.textContent = '\uD83E\uDD16 AI đang phân tích: "' + q + '"...';
                                        
                                        // Cập nhật text mockup
                                        summary.innerHTML = '<strong>NAVA AI:</strong> Bạn đang tìm kiếm <em>"' + q + '"</em>. Dựa trên dữ liệu, AI ưu tiên đề xuất máy có GPU tích hợp mạnh, RAM tối thiểu 16GB và tản nhiệt tốt trong phân khúc.';
                                        
                                        setTimeout(function() {
                                            loading.style.display = 'none';
                                            list.style.display = 'block';
                                            header.textContent = '\u2728 HOÀN TẤT PHÂN TÍCH & TÌM KIẾM';
                                        }, 1200);
                                    }
                                    aiSearchInput.addEventListener('keypress', function(e) { if (e.key==='Enter') { doSearch(); } });
                                    btn.addEventListener('click', function() { doSearch(); });
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
                                    <button class="compare-btn" data-name="ASUS NUC 14 Essential" title="Thêm vào so sánh" style="position: absolute; top: -5px; right: -5px; width: 28px; height: 28px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'ASUS NUC 14 Essential', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png', '4.490.000đ')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right" style="font-size: 0.8rem;"></i></button>
                                
                                    <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" alt="Featured" style="width: 100%; height: 100%; object-fit: contain;">
                                </div>
                                <div style="flex: 1; min-width: 0;">
                                    <span class="spec-pill" style="margin-bottom: 8px;">HOT SALE</span>
                                    <h4 style="margin: 0 0 6px 0; font-size: 0.95rem; font-weight: 700; color: var(--text-dark); display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; line-height: 1.4;">ASUS NUC 14 Essential</h4>
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.1rem;">4.490.000đ</span>
                                </div>
                            </div>
                            
                            <div class="product-card" style="margin:0; display: flex; align-items: center; padding: 15px; gap: 15px;" onclick="window.location.href='demo_product.html'">
                                <div style="width: 90px; height: 90px; flex-shrink: 0; position: relative;">
                                    <button class="compare-btn" data-name="AtomMan G7 PT Mini PC" title="Thêm vào so sánh" style="position: absolute; top: -5px; right: -5px; width: 28px; height: 28px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'AtomMan G7 PT Mini PC', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png', '34.490.000đ')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right" style="font-size: 0.8rem;"></i></button>
                                
                                    <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" alt="Featured" style="width: 100%; height: 100%; object-fit: contain;">
                                </div>
                                <div style="flex: 1; min-width: 0;">
                                    <span class="spec-pill" style="margin-bottom: 8px;">BÁN CHẠY</span>
                                    <h4 style="margin: 0 0 6px 0; font-size: 0.95rem; font-weight: 700; color: var(--text-dark); display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; line-height: 1.4;">AtomMan G7 PT Mini PC</h4>
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.1rem;">34.490.000đ</span>
                                </div>
                            </div>
                            
                            <div class="product-card" style="margin:0; display: flex; align-items: center; padding: 15px; gap: 15px;" onclick="window.location.href='demo_product.html'">
                                <div style="width: 90px; height: 90px; flex-shrink: 0; position: relative;">
                                    <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_1.png" alt="Featured" style="width: 100%; height: 100%; object-fit: contain;">
                                </div>
                                <div style="flex: 1; min-width: 0;">
                                    <span class="spec-pill" style="margin-bottom: 8px;">MỚI RA MẮT</span>
                                    <h4 style="margin: 0 0 6px 0; font-size: 0.95rem; font-weight: 700; color: var(--text-dark); display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; line-height: 1.4;">GMK EVO X1 32G</h4>
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.1rem;">31.190.000đ</span>
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
                                <button class="compare-btn" data-name="ASUS NUC 14 Essential Int" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'ASUS NUC 14 Essential Int', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png', '4.490.000đ')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
                                <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" alt="ASUS NUC 14" class="product-img" style="object-fit: contain; width: 100%; height: 100%; transition: transform 0.4s ease;">
                            </div>
                            <div class="card-content" style="padding: 15px 0 0 0; flex: 1; display: flex; flex-direction: column;">
                                <!-- Specs Badges -->
                                <div class="card-specs">
                                    <span class="spec-pill">CPU 6.000</span>                                    <span class="spec-pill secondary">GPU 1.200</span>
                                    <span class="spec-pill">WIFI 6E</span>
                                    <span class="spec-pill secondary">4 USB 3.2</span>
                                    <span class="spec-pill secondary">2 TYPE C</span>
                                </div>
                                
                                <h2 class="card-title">ASUS NUC 14 Essential Intel</h2>
                                
                                <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">4.490.000đ</span>
                                    
                                </div>
                            </div>
                        </div>

                        <!-- Product 2 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="AtomMan G7 PT Mini PC" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'AtomMan G7 PT Mini PC', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png', '34.490.000đ')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
                                <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" alt="AtomMan G7 PT" class="product-img" style="object-fit: contain; width: 100%; height: 100%; transition: transform 0.4s ease;">
                            </div>
                            <div class="card-content" style="padding: 15px 0 0 0; flex: 1; display: flex; flex-direction: column;">
                                <div class="card-specs">
                                    <span class="spec-pill">CPU 40.000</span>                                    <span class="spec-pill secondary">GPU 17...</span>
                                    <span class="spec-pill">4 FAN S...</span>
                                    <span class="spec-pill secondary">WIFI 7</span>
                                </div>
                                
                                <h2 class="card-title">AtomMan G7 PT Mini PC</h2>
                                
                                <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">34.490.000đ</span>
                                    
                                </div>
                            </div>
                        </div>

                        <!-- Product 3 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="Mini PC GMK EVO X1 32G" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'Mini PC GMK EVO X1 32G', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_1.png', '31.190.000đ')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
                                <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_1.png" alt="GMK EVO X1" class="product-img" style="object-fit: contain; width: 100%; height: 100%; transition: transform 0.4s ease;">
                            </div>
                            <div class="card-content" style="padding: 15px 0 0 0; flex: 1; display: flex; flex-direction: column;">
                                <div class="card-specs">
                                    <span class="spec-pill">CPU 38.500</span>                                    <span class="spec-pill secondary">GPU ...</span>
                                    <span class="spec-pill">2 NVME</span>
                                    <span class="spec-pill secondary">USB4</span>
                                </div>
                                
                                <h2 class="card-title">Mini PC GMK EVO X1 32G</h2>
                                
                                <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">31.190.000đ</span>
                                    
                                </div>
                            </div>
                        </div>

                        <!-- Product 4 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="Tablet Minisforum V3 SE" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'Tablet Minisforum V3 SE', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_2.png', '23.090.000đ')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
                                <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_2.png" alt="Tablet Minisforum" class="product-img" style="object-fit: contain; width: 100%; height: 100%; transition: transform 0.4s ease;">
                            </div>
                            <div class="card-content" style="padding: 15px 0 0 0; flex: 1; display: flex; flex-direction: column;">
                                <div class="card-specs">
                                    <span class="spec-pill">CPU 22.000</span>                                    <span class="spec-pill secondary">CPU ...</span>
                                    <span class="spec-pill">WIFI 6</span>
                                    <span class="spec-pill secondary">2 USB4</span>
                                </div>
                                
                                <h2 class="card-title">Tablet Minisforum V3 SE</h2>
                                
                                <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">23.090.000đ</span>
                                    
                                </div>
                            </div>
                        </div>
                        
                        <!-- Product 5 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="Beelink SER8 AMD 884" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'Beelink SER8 AMD 884', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_2.png', '11.990.000đ')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
                                <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_2.png" alt="Beelink SER8" class="product-img" style="object-fit: contain; width: 100%; height: 100%; transition: transform 0.4s ease;">
                            </div>
                            <div class="card-content" style="padding: 15px 0 0 0; flex: 1; display: flex; flex-direction: column;">
                                <div class="card-specs">
                                    <span class="spec-pill">CPU 26.000</span>                                    <span class="spec-pill secondary">GPU 16...</span>
                                    <span class="spec-pill">WIFI 6</span>
                                </div>
                                
                                <h2 class="card-title">Beelink SER8 AMD 884</h2>
                                
                                <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">11.990.000đ</span>
                                    
                                </div>
                            </div>
                        </div>
                        
<!-- Product 6 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="ASUS NUC 14 Essential Int" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'ASUS NUC 14 Essential Int', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png', '4.490.000đ')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
                                <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" alt="ASUS NUC 14" class="product-img" style="object-fit: contain; width: 100%; height: 100%; transition: transform 0.4s ease;">
                            </div>
                            <div class="card-content" style="padding: 15px 0 0 0; flex: 1; display: flex; flex-direction: column;">
                                <!-- Specs Badges -->
                                <div class="card-specs">
                                    <span class="spec-pill">CPU 6.000</span>                                    <span class="spec-pill secondary">GPU 1.200</span>
                                    <span class="spec-pill">WIFI 6E</span>
                                    <span class="spec-pill secondary">4 USB 3.2</span>
                                    <span class="spec-pill secondary">2 TYPE C</span>
                                </div>
                                
                                <h2 class="card-title">ASUS NUC 14 Essential Intel</h2>
                                
                                <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">4.490.000đ</span>
                                    
                                </div>
                            </div>
                        </div>

                        <!-- Product 7 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="AtomMan G7 PT Mini PC" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'AtomMan G7 PT Mini PC', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png', '34.490.000đ')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
                                <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" alt="AtomMan G7 PT" class="product-img" style="object-fit: contain; width: 100%; height: 100%; transition: transform 0.4s ease;">
                            </div>
                            <div class="card-content" style="padding: 15px 0 0 0; flex: 1; display: flex; flex-direction: column;">
                                <div class="card-specs">
                                    <span class="spec-pill">CPU 40.000</span>                                    <span class="spec-pill secondary">GPU 17...</span>
                                    <span class="spec-pill">4 FAN S...</span>
                                    <span class="spec-pill secondary">WIFI 7</span>
                                </div>
                                
                                <h2 class="card-title">AtomMan G7 PT Mini PC</h2>
                                
                                <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">34.490.000đ</span>
                                    
                                </div>
                            </div>
                        </div>

                        <!-- Product 8 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="Mini PC GMK EVO X1 32G" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'Mini PC GMK EVO X1 32G', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_1.png', '31.190.000đ')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
                                <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_1.png" alt="GMK EVO X1" class="product-img" style="object-fit: contain; width: 100%; height: 100%; transition: transform 0.4s ease;">
                            </div>
                            <div class="card-content" style="padding: 15px 0 0 0; flex: 1; display: flex; flex-direction: column;">
                                <div class="card-specs">
                                    <span class="spec-pill">CPU 38.500</span>                                    <span class="spec-pill secondary">GPU ...</span>
                                    <span class="spec-pill">2 NVME</span>
                                    <span class="spec-pill secondary">USB4</span>
                                </div>
                                
                                <h2 class="card-title">Mini PC GMK EVO X1 32G</h2>
                                
                                <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">31.190.000đ</span>
                                    
                                </div>
                            </div>
                        </div>

                        <!-- Product 9 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="Tablet Minisforum V3 SE" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'Tablet Minisforum V3 SE', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_2.png', '23.090.000đ')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
                                <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_2.png" alt="Tablet Minisforum" class="product-img" style="object-fit: contain; width: 100%; height: 100%; transition: transform 0.4s ease;">
                            </div>
                            <div class="card-content" style="padding: 15px 0 0 0; flex: 1; display: flex; flex-direction: column;">
                                <div class="card-specs">
                                    <span class="spec-pill">CPU 22.000</span>                                    <span class="spec-pill secondary">CPU ...</span>
                                    <span class="spec-pill">WIFI 6</span>
                                    <span class="spec-pill secondary">2 USB4</span>
                                </div>
                                
                                <h2 class="card-title">Tablet Minisforum V3 SE</h2>
                                
                                <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">23.090.000đ</span>
                                    
                                </div>
                            </div>
                        </div>
                        
                        <!-- Product 10 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="Beelink SER8 AMD 884" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'Beelink SER8 AMD 884', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_2.png', '11.990.000đ')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
                                <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_2.png" alt="Beelink SER8" class="product-img" style="object-fit: contain; width: 100%; height: 100%; transition: transform 0.4s ease;">
                            </div>
                            <div class="card-content" style="padding: 15px 0 0 0; flex: 1; display: flex; flex-direction: column;">
                                <div class="card-specs">
                                    <span class="spec-pill">CPU 26.000</span>                                    <span class="spec-pill secondary">GPU 16...</span>
                                    <span class="spec-pill">WIFI 6</span>
                                </div>
                                
                                <h2 class="card-title">Beelink SER8 AMD 884</h2>
                                
                                <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">11.990.000đ</span>
                                    
                                </div>
                            </div>
                        </div>
                        
<!-- Product 11 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="ASUS NUC 14 Essential Int" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'ASUS NUC 14 Essential Int', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png', '4.490.000đ')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
                                <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" alt="ASUS NUC 14" class="product-img" style="object-fit: contain; width: 100%; height: 100%; transition: transform 0.4s ease;">
                            </div>
                            <div class="card-content" style="padding: 15px 0 0 0; flex: 1; display: flex; flex-direction: column;">
                                <!-- Specs Badges -->
                                <div class="card-specs">
                                    <span class="spec-pill">CPU 6.000</span>                                    <span class="spec-pill secondary">GPU 1.200</span>
                                    <span class="spec-pill">WIFI 6E</span>
                                    <span class="spec-pill secondary">4 USB 3.2</span>
                                    <span class="spec-pill secondary">2 TYPE C</span>
                                </div>
                                
                                <h2 class="card-title">ASUS NUC 14 Essential Intel</h2>
                                
                                <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">4.490.000đ</span>
                                    
                                </div>
                            </div>
                        </div>

                        <!-- Product 12 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="AtomMan G7 PT Mini PC" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'AtomMan G7 PT Mini PC', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png', '34.490.000đ')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
                                <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" alt="AtomMan G7 PT" class="product-img" style="object-fit: contain; width: 100%; height: 100%; transition: transform 0.4s ease;">
                            </div>
                            <div class="card-content" style="padding: 15px 0 0 0; flex: 1; display: flex; flex-direction: column;">
                                <div class="card-specs">
                                    <span class="spec-pill">CPU 40.000</span>                                    <span class="spec-pill secondary">GPU 17...</span>
                                    <span class="spec-pill">4 FAN S...</span>
                                    <span class="spec-pill secondary">WIFI 7</span>
                                </div>
                                
                                <h2 class="card-title">AtomMan G7 PT Mini PC</h2>
                                
                                <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">34.490.000đ</span>
                                    
                                </div>
                            </div>
                        </div>

                        <!-- Product 13 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="Mini PC GMK EVO X1 32G" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'Mini PC GMK EVO X1 32G', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_1.png', '31.190.000đ')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
                                <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_1.png" alt="GMK EVO X1" class="product-img" style="object-fit: contain; width: 100%; height: 100%; transition: transform 0.4s ease;">
                            </div>
                            <div class="card-content" style="padding: 15px 0 0 0; flex: 1; display: flex; flex-direction: column;">
                                <div class="card-specs">
                                    <span class="spec-pill">CPU 38.500</span>                                    <span class="spec-pill secondary">GPU ...</span>
                                    <span class="spec-pill">2 NVME</span>
                                    <span class="spec-pill secondary">USB4</span>
                                </div>
                                
                                <h2 class="card-title">Mini PC GMK EVO X1 32G</h2>
                                
                                <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">31.190.000đ</span>
                                    
                                </div>
                            </div>
                        </div>

                        <!-- Product 14 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="Tablet Minisforum V3 SE" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'Tablet Minisforum V3 SE', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_2.png', '23.090.000đ')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
                                <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_2.png" alt="Tablet Minisforum" class="product-img" style="object-fit: contain; width: 100%; height: 100%; transition: transform 0.4s ease;">
                            </div>
                            <div class="card-content" style="padding: 15px 0 0 0; flex: 1; display: flex; flex-direction: column;">
                                <div class="card-specs">
                                    <span class="spec-pill">CPU 22.000</span>                                    <span class="spec-pill secondary">CPU ...</span>
                                    <span class="spec-pill">WIFI 6</span>
                                    <span class="spec-pill secondary">2 USB4</span>
                                </div>
                                
                                <h2 class="card-title">Tablet Minisforum V3 SE</h2>
                                
                                <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">23.090.000đ</span>
                                    
                                </div>
                            </div>
                        </div>
                        
                        <!-- Product 15 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="Beelink SER8 AMD 884" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'Beelink SER8 AMD 884', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_2.png', '11.990.000đ')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
                                <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_2.png" alt="Beelink SER8" class="product-img" style="object-fit: contain; width: 100%; height: 100%; transition: transform 0.4s ease;">
                            </div>
                            <div class="card-content" style="padding: 15px 0 0 0; flex: 1; display: flex; flex-direction: column;">
                                <div class="card-specs">
                                    <span class="spec-pill">CPU 26.000</span>                                    <span class="spec-pill secondary">GPU 16...</span>
                                    <span class="spec-pill">WIFI 6</span>
                                </div>
                                
                                <h2 class="card-title">Beelink SER8 AMD 884</h2>
                                
                                <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">11.990.000đ</span>
                                    
                                </div>
                            </div>
                        </div>
                        
<!-- Product 16 -->
                        <div class="product-card" style="margin:0; height: 100%; display: flex; flex-direction: column; padding: 15px; cursor: pointer;" onclick="window.location.href='demo_product.html'">
                            <div class="card-glow"></div>
                            <div class="card-image-wrap" style="height: 180px; position: relative; background: transparent; padding: 0;">
                                <button class="compare-btn" data-name="ASUS NUC 14 Essential Int" title="Thêm vào so sánh" style="position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; z-index: 5; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.05);" onclick="event.stopPropagation(); toggleCompare(this, 'ASUS NUC 14 Essential Int', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png', '4.490.000đ')" onmouseover="if(this.style.background!=='var(--primary)'){this.style.borderColor='var(--primary)'; this.style.color='var(--primary)'}"><i class="ph ph-arrows-left-right"></i></button>
                            
                                <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" alt="ASUS NUC 14" class="product-img" style="object-fit: contain; width: 100%; height: 100%; transition: transform 0.4s ease;">
                            </div>
                            <div class="card-content" style="padding: 15px 0 0 0; flex: 1; display: flex; flex-direction: column;">
                                <!-- Specs Badges -->
                                <div class="card-specs">
                                    <span class="spec-pill">CPU 6.000</span>                                    <span class="spec-pill secondary">GPU 1.200</span>
                                    <span class="spec-pill">WIFI 6E</span>
                                    <span class="spec-pill secondary">4 USB 3.2</span>
                                    <span class="spec-pill secondary">2 TYPE C</span>
                                </div>
                                
                                <h2 class="card-title">ASUS NUC 14 Essential Intel</h2>
                                
                                <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                    <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">4.490.000đ</span>
                                    
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
            
            <!-- Category Description Section -->
            <div class="category-description-section">
                <div id="cat-desc-wrapper" class="cat-desc-wrapper">
                    <h2 style="font-size: 1.5rem; font-weight: 800; color: var(--text-dark); margin-bottom: 16px;">Giới thiệu về dòng Mini PC ASUS NUC</h2>
                    <p style="color: var(--text-gray); line-height: 1.8; margin-bottom: 15px; font-size: 0.95rem;">
                        Mini PC ASUS NUC (Next Unit of Computing) là dòng máy tính nhỏ gọn thế hệ mới, mang trong mình sức mạnh hiệu năng vượt trội tương đương các dòng máy tính để bàn truyền thống. Kể từ khi ASUS chính thức tiếp quản và phát triển thương hiệu NUC từ Intel, các dòng sản phẩm này đã được nâng cấp mạnh mẽ về cả thiết kế, độ bền lẫn các giải pháp tản nhiệt tiên tiến.
                    </p>
                    <h3 style="font-size: 1.2rem; font-weight: 700; color: var(--text-dark); margin-top: 20px; margin-bottom: 12px;">Những ưu điểm vượt trội của ASUS NUC</h3>
                    <ul style="color: var(--text-gray); line-height: 1.8; margin-left: 20px; margin-bottom: 15px; font-size: 0.95rem; list-style-type: disc;">
                        <li style="margin-bottom: 8px;"><strong>Thiết kế siêu nhỏ gọn:</strong> Với kích thước chỉ nằm gọn trong lòng bàn tay, ASUS NUC giúp tối ưu hóa không gian làm việc, dễ dàng lắp đặt phía sau màn hình thông qua khung treo VESA tiêu chuẩn.</li>
                        <li style="margin-bottom: 8px;"><strong>Hiệu năng mạnh mẽ:</strong> Trang bị các bộ vi xử lý Intel Core hoặc AMD Ryzen thế hệ mới nhất, đáp ứng hoàn hảo từ công việc văn phòng, lập trình, đồ họa nhẹ cho tới các giải pháp tự động hóa chuyên sâu.</li>
                        <li style="margin-bottom: 8px;"><strong>Độ bền chuẩn quân đội:</strong> Tất cả sản phẩm ASUS NUC đều trải qua các bài kiểm tra nghiêm ngặt về nhiệt độ, độ rung và rơi tự do đạt tiêu chuẩn MIL-STD-810H, hoạt động bền bỉ 24/7.</li>
                        <li style="margin-bottom: 8px;"><strong>Khả năng nâng cấp linh hoạt:</strong> Hỗ trợ khe cắm RAM DDR5 kép và các cổng lưu trữ SSD M.2 PCIe tốc độ cao, cho phép người dùng tùy biến cấu hình theo đúng nhu cầu sử dụng thực tế.</li>
                    </ul>
                    <p style="color: var(--text-gray); line-height: 1.8; margin-bottom: 15px; font-size: 0.95rem;">
                        Hiện nay, NAVA Store tự hào là đối tác Gold Partner của ASUS tại Việt Nam, mang đến cho quý khách hàng các sản phẩm Mini PC ASUS NUC chính hãng với chế độ bảo hành vàng 36 tháng, lỗi 1 đổi 1 trong vòng 30 ngày và dịch vụ hỗ trợ kỹ thuật trọn đời từ đội ngũ chuyên gia giàu kinh nghiệm.
                    </p>
                    <div class="cat-desc-fade"></div>
                </div>
                <div style="text-align: center; margin-top: 20px; position: relative; z-index: 5;">
                    <button id="cat-desc-btn" class="btn-cat-more" onclick="toggleCatDescription()">
                        Xem thêm <i class="ph ph-caret-down"></i>
                    </button>
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
                        const maxVal = maxInput ? parseInt(maxInput.value) : 50000000;
                        
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
                        }
                    });
                });
                
                // 4. Mobile Off-canvas Sidebar
                function toggleMobileSidebar() {
                    document.querySelector('.nava-sidebar').classList.toggle('active');
                    document.querySelector('.sidebar-overlay').classList.toggle('active');
                }
                
                // 5. Category Description Toggle
                function toggleCatDescription() {
                    const wrapper = document.getElementById('cat-desc-wrapper');
                    const btn = document.getElementById('cat-desc-btn');
                    if (!wrapper || !btn) return;
                    
                    const isExpanded = wrapper.classList.toggle('expanded');
                    if (isExpanded) {
                        btn.innerHTML = 'Thu gọn <i class="ph ph-caret-up"></i>';
                    } else {
                        btn.innerHTML = 'Xem thêm <i class="ph ph-caret-down"></i>';
                        wrapper.scrollIntoView({ behavior: 'smooth' });
                    }
                }
            </script>
        </div>
    """
    full_html = clean_liquid_tags(header_part + collection_html + local_footer_part, 'collection')
    
    try:
        with open(os.path.join(base_dir, "post_build.py"), "r", encoding="utf-8") as pb_file:
            pb_content = pb_file.read()
            start_pos = pb_content.find('sticky_html = """')
            end_idx = pb_content.find('"""\n\nfile_path')
            if start_pos != -1 and end_idx != -1:
                start_idx = start_pos + len('sticky_html = """')
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
    full_html = inject_seo_metadata(
        full_html,
        title="Mini PC ASUS NUC Chính Hãng - Nava Store",
        description="Mua Mini PC ASUS NUC chính hãng tại Nava Store. Hỗ trợ trả góp, bảo hành 36 tháng, giao hàng nhanh toàn quốc.",
        keywords="Mini PC Asus, Asus NUC, Mini PC Asus NUC, Nava Store"
    )
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
                .nava-product-layout { 
                    display: flex; flex-direction: column; gap: 40px; margin-top: 20px; width: 100%; box-sizing: border-box; 
                    background: #ffffff; padding: 24px; border-radius: 16px; box-shadow: 0 4px 24px rgba(0,0,0,0.03); border: 1px solid #e2e8f0;
                }
                .nava-prod-gallery { width: 100%; box-sizing: border-box; }
                .nava-prod-info { width: 100%; display: flex; flex-direction: column; box-sizing: border-box; }
                @media (min-width: 992px) {
                    .nava-product-layout { flex-direction: row; align-items: flex-start; gap: 60px; padding: 40px; }
                    .nava-prod-gallery { width: 55%; position: sticky; top: 130px; }
                    .nava-prod-info { width: 45%; }
                }
                @media (max-width: 767px) {
                    .container {
                        padding-left: 12px !important;
                        padding-right: 12px !important;
                    }
                    .nava-product-layout {
                        padding: 15px !important;
                        margin-left: 0 !important;
                        margin-right: 0 !important;
                        border-radius: 12px !important;
                        width: 100% !important;
                    }
                    .ai-compare-input-row {
                        flex-direction: column !important;
                        align-items: stretch !important;
                        gap: 12px !important;
                    }
                    .ai-compare-input-row input {
                        width: 100% !important;
                        flex: none !important;
                    }
                    .ai-compare-input-row button {
                        width: 100% !important;
                        justify-content: center !important;
                        flex: none !important;
                    }
                }
                @media (max-width: 991px) {
                    .nava-spec-grid {
                        max-height: 380px !important;
                        overflow-y: auto !important;
                        -webkit-overflow-scrolling: touch !important;
                        padding-right: 8px;
                        scrollbar-width: none;
                        -ms-overflow-style: none;
                    }
                    .nava-spec-grid::-webkit-scrollbar {
                        display: none;
                    }
                }
                
                /* Clean Gallery */
                .main-image-container { 
                    background: #ffffff; 
                    border-radius: 16px; 
                    padding: 24px; 
                    text-align: center; 
                    margin-bottom: 32px; 
                    display: flex; 
                    align-items: center; 
                    justify-content: center; 
                    position: relative;
                    aspect-ratio: 4/3;
                    border: 1px solid #e2e8f0;
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
                .gallery-dots { display: flex; justify-content: center; gap: 8px; margin-bottom: 32px; }
                .gallery-dot { width: 8px; height: 8px; border-radius: 50%; background: #cbd5e1; cursor: pointer; transition: 0.3s; }
                .gallery-dot.active { background: var(--primary); width: 24px; border-radius: 4px; }
                .gallery-thumb { 
                    width: 72px; height: 72px; border-radius: 12px; background: #ffffff; padding: 8px; 
                    cursor: pointer; border: 1px solid #e2e8f0; transition: 0.2s; flex-shrink: 0;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
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
                .variants-row-container {
                    display: flex;
                    gap: 16px;
                    margin-bottom: 24px;
                }
                .variants-row-container .variant-group {
                    flex: 1;
                    margin-bottom: 0;
                }
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
                .variant-card-price { display: none !important; }
                
                .variant-price-display {
                    font-size: 0.9rem;
                    font-weight: 700;
                    color: var(--primary);
                    margin-left: auto;
                    background: rgba(14, 165, 233, 0.08);
                    padding: 4px 10px;
                    border-radius: 6px;
                }
                
                /* Premium Dropdown Styles */
                .nava-dropdown-wrapper {
                    position: relative;
                    width: 100%;
                }
                .nava-dropdown-display {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    border: 1px solid #cbd5e1;
                    border-radius: 10px;
                    padding: 12px 18px;
                    background: #fff;
                    cursor: default;
                    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
                    font-size: 0.95rem;
                    font-weight: 600;
                    color: #0f172a;
                    user-select: none;
                    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
                }
                .nava-dropdown-display:hover {
                    border-color: var(--primary);
                    box-shadow: 0 4px 12px rgba(14, 165, 233, 0.05);
                }
                .nava-dropdown-selected {
                    display: inline-block;
                }
                .nava-dropdown-arrow {
                    font-size: 1rem;
                    color: #64748b;
                    transition: transform 0.2s ease;
                }
                .nava-dropdown-wrapper.active .nava-dropdown-arrow {
                    transform: rotate(180deg);
                    color: var(--primary);
                }
                .nava-dropdown-wrapper:hover .nava-dropdown-display {
                    border-color: var(--primary);
                }
                .nava-dropdown-list {
                    position: absolute;
                    top: 100%;
                    left: 0;
                    width: 100%;
                    margin-top: 6px;
                    padding: 6px;
                    background: rgba(255, 255, 255, 0.98);
                    backdrop-filter: blur(10px);
                    border: 1px solid #e2e8f0;
                    border-radius: 12px;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08), 0 4px 12px rgba(0, 0, 0, 0.03);
                    list-style: none;
                    z-index: 1000;
                    margin-bottom: 0;
                    opacity: 0;
                    visibility: hidden;
                    transform: translateY(-10px) scale(0.98);
                    transition: opacity 0.2s cubic-bezier(0.4, 0, 0.2, 1), transform 0.2s cubic-bezier(0.4, 0, 0.2, 1), visibility 0.2s;
                }
                .nava-dropdown-wrapper.active .nava-dropdown-list {
                    opacity: 1;
                    visibility: visible;
                    transform: translateY(0) scale(1);
                }
                .nava-dropdown-item {
                    padding: 10px 16px;
                    cursor: pointer;
                    font-size: 0.9rem;
                    font-weight: 550;
                    color: #334155;
                    border-radius: 8px;
                    transition: all 0.15s ease;
                    margin-bottom: 2px;
                }
                .nava-dropdown-item:last-child {
                    margin-bottom: 0;
                }
                .nava-dropdown-item:hover {
                    background: #f1f5f9;
                    color: var(--primary);
                }
                .nava-dropdown-item.active {
                    background: #e0f2fe;
                    color: var(--primary);
                    font-weight: 700;
                }
                [data-theme="dark"] .variant-price-display {
                    background: rgba(51, 133, 255, 0.15);
                    color: #66a3ff;
                }
                
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
                
                .btn-goto-store { 
                    background: #fff; border: 1px solid var(--primary); border-radius: 8px; color: var(--primary); font-weight: 700; cursor: pointer; transition: 0.2s; display: flex; align-items: center; justify-content: center;
                }
                .btn-goto-store:hover { background: var(--primary); color: #fff; }
                
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
                [data-theme="dark"] .btn-goto-store { background: var(--bg-gray) !important; border-color: var(--border-color) !important; color: var(--text-dark) !important; }
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
                
                [data-theme="dark"] .nava-product-layout { background: var(--bg-white) !important; border-color: var(--border-color) !important; box-shadow: none !important; }
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
                

                /* Aligned text in dropdown and align arrow */
                .nava-dropdown-display {
                    position: relative !important;
                    display: flex !important;
                    align-items: center !important;
                    justify-content: space-between !important;
                    padding-right: 40px !important;
                }
                .nava-dropdown-selected-price {
                    font-weight: 700;
                    font-size: 0.9rem;
                    color: var(--primary);
                    margin-left: auto;
                    margin-right: 5px;
                }
                [data-theme="dark"] .nava-dropdown-selected-price {
                    color: #66a3ff;
                }
                .nava-dropdown-arrow {
                    position: absolute !important;
                    right: 18px !important;
                    top: 50% !important;
                    transform: translateY(-50%) !important;
                    margin: 0 !important;
                }
                .nava-dropdown-wrapper.active .nava-dropdown-arrow {
                    transform: translateY(-50%) rotate(180deg) !important;
                }

                /* Bottom Sheet Overlay & Drawer */
                #nava-bs-overlay {
                    position: fixed;
                    inset: 0;
                    background: rgba(15, 23, 42, 0.6);
                    backdrop-filter: blur(4px);
                    z-index: 2147483640;
                    display: none;
                    opacity: 0;
                    transition: opacity 0.3s ease;
                }
                #nava-bottom-sheet {
                    position: fixed;
                    bottom: 0;
                    left: 0;
                    width: 100%;
                    background: var(--bg-white, #ffffff);
                    border-radius: 20px 20px 0 0;
                    box-shadow: 0 -10px 40px rgba(0,0,0,0.15);
                    z-index: 2147483641;
                    transform: translateY(100%);
                    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                    box-sizing: border-box;
                    max-height: 85vh;
                    display: none;
                    flex-direction: column;
                    height: 360px;
                    --glow-color: rgba(30, 58, 138, 0.15);
                    --glow-border: var(--primary, #1e3a8a);
                }
                #nava-bottom-sheet.open {
                    transform: translateY(0);
                }
                @keyframes bs-glow-attention {
                    0%, 100% {
                        border-color: var(--border-color, #cbd5e1);
                        box-shadow: none;
                    }
                    50% {
                        border-color: var(--glow-border);
                        box-shadow: 0 0 0 4px var(--glow-color), 0 4px 12px var(--glow-color);
                    }
                }
                #nava-bottom-sheet.open .nava-dropdown-display {
                    animation: bs-glow-attention 1.2s ease-in-out 3;
                }
                #nava-bottom-sheet .bs-header {
                    display: flex;
                    align-items: center;
                    padding: 20px;
                    border-bottom: 1px solid var(--border-color, #e2e8f0);
                    position: relative;
                    gap: 15px;
                }
                #nava-bottom-sheet .bs-header .bs-thumb {
                    width: 70px;
                    height: 70px;
                    object-fit: contain;
                    background: #fff;
                    border-radius: 8px;
                    border: 1px solid var(--border-color, #e2e8f0);
                    padding: 4px;
                }
                #nava-bottom-sheet .bs-header .bs-header-info {
                    flex: 1;
                    min-width: 0;
                }
                #nava-bottom-sheet .bs-header .bs-price-val {
                    font-size: 1.4rem;
                    font-weight: 800;
                    color: var(--primary);
                }
                #nava-bottom-sheet .bs-header .bs-close-btn {
                    position: absolute;
                    top: 15px;
                    right: 15px;
                    background: none;
                    border: none;
                    font-size: 1.5rem;
                    color: var(--text-gray, #64748b);
                    cursor: pointer;
                    transition: color 0.2s;
                }
                #nava-bottom-sheet .bs-header .bs-close-btn:hover {
                    color: #ef4444;
                }
                #nava-bottom-sheet .bs-body {
                    padding: 24px 30px;
                    flex: 1;
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                    overflow: visible;
                }
                #nava-bottom-sheet .bs-options-row {
                    display: flex;
                    align-items: center;
                    gap: 20px;
                    width: 100%;
                }
                #nava-bottom-sheet .bs-option-col {
                    flex: 1;
                    display: flex;
                    flex-direction: column;
                    gap: 8px;
                }
                #nava-bottom-sheet .bs-qty-col {
                    flex: 0 0 auto;
                    align-items: flex-end;
                    margin-left: auto;
                }
                #nava-bottom-sheet .nava-dropdown-list {
                    top: auto;
                    bottom: 100%;
                    margin-top: 0;
                    margin-bottom: 6px;
                    transform: translateY(10px) scale(0.98);
                }
                #nava-bottom-sheet .nava-dropdown-wrapper.active .nava-dropdown-list {
                    transform: translateY(0) scale(1);
                }
                @media (max-width: 768px) {
                    #nava-bottom-sheet {
                        height: auto !important;
                    }
                    #nava-bottom-sheet .bs-body {
                        overflow: visible;
                    }
                    #nava-bottom-sheet .bs-options-row {
                        flex-direction: column;
                        align-items: stretch;
                        gap: 15px;
                    }
                    #nava-bottom-sheet .bs-qty-col {
                        align-items: flex-start;
                        margin-left: 0;
                    }
                }
                #nava-bottom-sheet .bs-buy-btn {
                    width: 100%;
                    height: 50px;
                    border-radius: 8px;
                    border: none;
                    background: linear-gradient(90deg, var(--primary), var(--secondary));
                    color: white;
                    font-weight: 800;
                    font-size: 1rem;
                    cursor: pointer;
                    text-transform: uppercase;
                    transition: all 0.2s;
                    box-shadow: 0 4px 15px rgba(0, 51, 102, 0.2);
                }
                #nava-bottom-sheet .bs-buy-btn:hover {
                    box-shadow: 0 6px 20px rgba(0, 51, 102, 0.35);
                    transform: translateY(-1px);
                }
                [data-theme="dark"] #nava-bottom-sheet {
                    background: var(--bg-white, #1e293b) !important;
                    --glow-color: rgba(102, 163, 255, 0.25);
                    --glow-border: #66a3ff;
                }

                /* Spec badges styling */
                .prod-spec-tag {
                    display: flex;
                    align-items: center;
                    gap: 6px;
                    background: #f1f5f9;
                    padding: 6px 12px;
                    border-radius: 8px;
                    font-size: 0.85rem;
                    font-weight: 600;
                    color: #334155;
                    border: 1px solid #e2e8f0;
                    text-decoration: none;
                    transition: all 0.2s ease;
                }
                .prod-spec-tag i {
                    font-size: 1.1rem;
                    color: var(--primary);
                    transition: color 0.2s ease;
                }
                .prod-spec-tag:hover {
                    border-color: var(--primary);
                    background: #f0f9ff;
                    color: var(--primary);
                }
                .prod-spec-tag:hover i {
                    color: var(--primary);
                }
                [data-theme="dark"] .prod-spec-tag {
                    background: var(--bg-gray);
                    border-color: var(--border-color);
                    color: var(--text-dark);
                }
                [data-theme="dark"] .prod-spec-tag i {
                    color: var(--primary);
                }
                [data-theme="dark"] .prod-spec-tag:hover {
                    background: rgba(51, 133, 255, 0.15);
                    border-color: var(--primary);
                    color: var(--primary);
                }

                /* Actions redesign styling */
                .product-actions-container {
                    display: flex;
                    flex-direction: column;
                    width: 100%;
                    margin-bottom: 24px;
                    margin-top: 10px;
                }

                .warranty-badge-container {
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 10px;
                    background: #fefce8;
                    border: 1px solid #fef08a;
                    color: #854d0e;
                    padding: 12px 16px;
                    border-radius: 12px;
                    font-weight: 700;
                    font-size: 0.95rem;
                    margin-bottom: 16px;
                    box-shadow: 0 4px 12px rgba(234, 179, 8, 0.05);
                    transition: all 0.2s ease;
                }
                .warranty-badge-container i {
                    font-size: 1.3rem;
                    color: #ca8a04;
                }
                [data-theme="dark"] .warranty-badge-container {
                    background: rgba(234, 179, 8, 0.08);
                    border-color: rgba(234, 179, 8, 0.2);
                    color: #fef08a;
                    box-shadow: none;
                }
                [data-theme="dark"] .warranty-badge-container i {
                    color: #facc15;
                }

                .btn-buy-now-primary {
                    width: 100%;
                    height: 54px;
                    background: var(--primary);
                    color: #ffffff;
                    border: none;
                    border-radius: 12px;
                    font-weight: 700;
                    font-size: 1.05rem;
                    letter-spacing: 0.5px;
                    cursor: pointer;
                    transition: all 0.2s ease;
                    margin-bottom: 12px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 0 4px 14px rgba(30, 58, 138, 0.2);
                }
                .btn-buy-now-primary:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 6px 20px rgba(30, 58, 138, 0.3);
                    opacity: 0.95;
                }
                .btn-buy-now-primary:active {
                    transform: translateY(0);
                }

                .btn-add-to-cart-secondary {
                    width: 100%;
                    height: 54px;
                    background: #ffffff;
                    color: var(--primary);
                    border: 2px solid var(--primary);
                    border-radius: 12px;
                    font-weight: 700;
                    font-size: 1.05rem;
                    letter-spacing: 0.5px;
                    cursor: pointer;
                    transition: all 0.2s ease;
                    margin-bottom: 16px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                .btn-add-to-cart-secondary:hover {
                    background: rgba(30, 58, 138, 0.04);
                    transform: translateY(-2px);
                }
                .btn-add-to-cart-secondary:active {
                    transform: translateY(0);
                }
                [data-theme="dark"] .btn-add-to-cart-secondary {
                    background: transparent;
                    color: #66a3ff;
                    border-color: #66a3ff;
                }
                [data-theme="dark"] .btn-add-to-cart-secondary:hover {
                    background: rgba(102, 163, 255, 0.08);
                }

                .actions-bottom-row {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    width: 100%;
                }
                .qty-label {
                    font-size: 0.95rem;
                    font-weight: 600;
                    color: #475569;
                    white-space: nowrap;
                    margin-right: auto;
                }
                [data-theme="dark"] .qty-label {
                    color: var(--text-dark);
                }
                .qty-selector {
                    display: flex;
                    align-items: center;
                    border: 1px solid #cbd5e1;
                    border-radius: 10px;
                    height: 46px;
                    background: #ffffff;
                    overflow: hidden;
                }
                [data-theme="dark"] .qty-selector {
                    border-color: var(--border-color);
                    background: var(--bg-gray);
                }
                .qty-adjust {
                    width: 36px;
                    height: 100%;
                    background: transparent;
                    border: none;
                    font-size: 1.2rem;
                    font-weight: 600;
                    cursor: pointer;
                    color: #475569;
                    transition: background 0.15s ease;
                }
                .qty-adjust:hover {
                    background: #f1f5f9;
                }
                [data-theme="dark"] .qty-adjust:hover {
                    background: rgba(255,255,255,0.05);
                }
                [data-theme="dark"] .qty-adjust {
                    color: var(--text-dark);
                }
                .qty-val {
                    width: 40px;
                    height: 100%;
                    text-align: center;
                    border: none;
                    background: transparent;
                    font-weight: 700;
                    font-size: 1rem;
                    color: #0f172a;
                }
                [data-theme="dark"] .qty-val {
                    color: var(--text-dark);
                }
                .btn-icon-secondary {
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    width: 46px;
                    height: 46px;
                    border-radius: 10px;
                    border: 1px solid #cbd5e1;
                    background: #ffffff;
                    color: var(--primary);
                    cursor: pointer;
                    transition: all 0.2s ease;
                }
                .btn-icon-secondary i {
                    font-size: 1.3rem;
                }
                .btn-icon-secondary:hover {
                    border-color: var(--primary);
                    background: rgba(30, 58, 138, 0.04);
                    transform: translateY(-1px);
                }
                [data-theme="dark"] .btn-icon-secondary {
                    border-color: var(--border-color);
                    background: var(--bg-gray);
                    color: var(--text-dark);
                }
                [data-theme="dark"] .btn-icon-secondary:hover {
                    border-color: var(--primary);
                    color: var(--primary);
                    background: rgba(51, 133, 255, 0.1);
                }

                .desktop-qty-label { display: inline; }
                .mobile-qty-label { display: none; }

                /* Simple Policy */
                .simple-policies { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; padding-top: 24px; border-top: 1px dashed #cbd5e1; }
                .sp-item { display: flex; align-items: center; gap: 10px; font-size: 0.85rem; color: #334155; font-weight: 600; background: #f8fafc; padding: 12px; border-radius: 8px; border: 1px solid #e2e8f0; }
                .sp-item i { font-size: 1.2rem; color: var(--primary); background: #fff; padding: 6px; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
                
                @media (max-width: 768px) {
                    .prod-title { font-size: 1.15rem !important; margin-bottom: 12px; }
                    .prod-price { font-size: 1.4rem; }
                    .prod-price-wrap { margin-bottom: 20px; padding-bottom: 16px; flex-direction: column; gap: 4px; border-bottom: none; }
                    
                    .desktop-qty-label { display: none !important; }
                    .mobile-qty-label { display: inline !important; }

                    /* Narrow quantity selector on mobile */
                    .qty-selector {
                        height: 32px !important;
                    }
                    .qty-selector .qty-adjust {
                        width: 28px !important;
                        height: 100% !important;
                        font-size: 0.95rem !important;
                    }
                    .qty-selector .qty-val {
                        width: 28px !important;
                        height: 100% !important;
                        font-size: 0.85rem !important;
                    }

                    /* Fix product details grid padding */
                    .desc-column { padding: 16px !important; }
                    .specs-column { padding: 16px !important; }
                    
                    /* Fix variants layout */
                    .variants-row-container { flex-direction: column; gap: 12px; }
                    .variant-options { display: grid !important; grid-template-columns: repeat(3, 1fr); gap: 6px; }
                    .variant-card { flex-direction: column; align-items: flex-start; gap: 2px; padding: 6px 8px; width: 100%; box-sizing: border-box; text-align: left; }
                    .variant-card-title { font-size: 0.8rem; }
                    .variant-card-price { font-size: 0.7rem; }
                    
                    /* Fix actions layout */
                    .nava-product-layout { gap: 24px; margin-bottom: 30px !important; }
                    .action-row { margin-bottom: 16px; }
                    .btn-buy-now-subtext { display: none !important; }
                    .mobile-actions-col button { height: 52px !important; padding: 4px !important; display: flex !important; flex-direction: column !important; align-items: center !important; justify-content: center !important; box-sizing: border-box !important; }
                    .mobile-actions-col button span { font-size: 0.75rem !important; }
                    .mobile-actions-col button i { font-size: 1.2rem !important; }
                    
                    /* Fix policies box */
                    .policy-mobile-box { display: flex !important; flex-direction: column !important; gap: 12px !important; }
                    
                    /* Fix gallery thumbnails cutoff on mobile */
                    .thumbnail-list { justify-content: flex-start !important; padding-left: 8px !important; padding-right: 8px !important; }

                    /* Make slide/gallery images smaller on mobile */
                    .main-image-container {
                        max-width: 300px !important;
                        margin: 0 auto 20px auto !important;
                        aspect-ratio: 1/1 !important;
                        padding: 15px !important;
                    }
                    .gallery-thumb {
                        width: 56px !important;
                        height: 56px !important;
                        padding: 4px !important;
                    }

                    /* Stack Quantity & Price vertically to avoid overlap */
                    .qty-price-row {
                        flex-direction: column !important;
                        align-items: flex-start !important;
                        gap: 12px !important;
                    }
                    .qty-price-row .prod-price {
                        font-size: 1.3rem !important;
                        margin-top: 4px !important;
                    }
                    
                    /* Compact action buttons row */
                    .action-buttons-row {
                        height: 46px !important;
                        gap: 8px !important;
                    }
                    .action-buttons-row #btn-add-to-cart-main {
                        width: 46px !important;
                        height: 46px !important;
                    }
                    .action-buttons-row button {
                        height: 46px !important;
                        font-size: 0.8rem !important;
                        padding: 0 8px !important;
                    }
                    .action-buttons-row #btn-buy-now-main span {
                        font-size: 0.85rem !important;
                    }

                    /* Reduce review paddings on mobile */
                    #danh-gia-shopee {
                        padding: 16px !important;
                    }
                    .sr-overview-card,
                    .sr-distribution-card {
                        padding: 15px !important;
                    }
                    .shopee-comment-item {
                        padding: 15px !important;
                    }
                }
                
                /* Magnifier */
                .main-image-container { position: relative; overflow: hidden; cursor: zoom-in; }
                #main-product-img { width: 100%; height: 100%; object-fit: contain; }
            </style>
            
            <div class="nava-product-layout" style="margin-bottom: 60px;">
                <!-- Gallery -->
                <div class="nava-prod-gallery">
                    <div class="main-image-container" id="main-image-container" onclick="window.openLightbox(event)">
                        <span class="badge" style="position: absolute; top: 16px; left: 16px; background: var(--primary); color: white; padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; z-index: 2;">MỚI NHẤT</span>
                        
                        <button type="button" onclick="window.openLightbox(event)" style="position: absolute; top: 16px; right: 16px; background: rgba(255,255,255,0.8); border: 1px solid var(--border-color); width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; color: var(--text-dark); z-index: 5; backdrop-filter: blur(4px); transition: all 0.2s; box-shadow: 0 2px 8px rgba(0,0,0,0.05);" onmouseover="this.style.background='var(--primary)'; this.style.color='white'; this.style.borderColor='var(--primary)';" onmouseout="this.style.background='rgba(255,255,255,0.8)'; this.style.color='var(--text-dark)'; this.style.borderColor='var(--border-color)';"><i class="ph-bold ph-arrows-out"></i></button>
                        
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
                    
                    <div class="thumbnail-list" id="thumbnail-list" style="position: relative; display: flex; justify-content: center; gap: 12px; overflow-x: auto; padding-bottom: 8px; scrollbar-width: none;">
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
                        <a href="#danh-gia-shopee" id="rating-scroll-btn" style="display: flex; align-items: center; gap: 4px; color: #f59e0b; font-weight: 600; text-decoration: none;">
                            <i class="ph-fill ph-star"></i> 5.0
                        </a>
                        <span>|</span>
                        <span>Đã bán: 85</span>
                        <span>|</span>
                        <span id="main-stock-status" style="color: #059669; display: flex; align-items: center; gap: 4px;"><i class="ph-fill ph-check-circle"></i> Sẵn hàng</span>
                    </div>
                    
                    <div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 10px; margin-bottom: 24px; border-bottom: 1px dashed var(--border-color); padding-bottom: 15px;">
                        <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                            <a href="#thong-so" class="prod-spec-tag" style="background: var(--bg-gray); border: 1px solid var(--border-color); border-radius: 6px; padding: 6px 12px; text-decoration: none; color: var(--text-dark); font-weight: 600; font-size: 0.85rem; display: inline-flex; align-items: center; gap: 6px;">
                                <i class="ph ph-cpu" style="color: var(--primary);"></i> Ryzen AI 7
                            </a>
                            <a href="#thong-so" class="prod-spec-tag" style="background: var(--bg-gray); border: 1px solid var(--border-color); border-radius: 6px; padding: 6px 12px; text-decoration: none; color: var(--text-dark); font-weight: 600; font-size: 0.85rem; display: inline-flex; align-items: center; gap: 6px;">
                                <i class="ph ph-graphics-card" style="color: var(--primary);"></i> Radeon 860M
                            </a>
                            <a href="#thong-so" class="prod-spec-tag" style="background: var(--bg-gray); border: 1px solid var(--border-color); border-radius: 6px; padding: 6px 12px; text-decoration: none; color: var(--text-dark); font-weight: 600; font-size: 0.85rem; display: inline-flex; align-items: center; gap: 6px;">
                                <i class="ph ph-brain" style="color: var(--primary);"></i> 50 TOPS
                            </a>
                        </div>
                        <button type="button" class="btn-nava-compare-trigger" onclick="openCompareDrawerDirect()" style="background: transparent; border: 1px solid var(--border-color); border-radius: 6px; padding: 6px 12px; font-weight: 700; font-size: 0.85rem; color: var(--text-dark); cursor: pointer; display: inline-flex; align-items: center; gap: 6px; transition: all 0.2s;" onmouseover="this.style.borderColor='var(--primary)'; this.style.color='var(--primary)';" onmouseout="this.style.borderColor='var(--border-color)'; this.style.color='var(--text-dark)';">
                            <i class="ph-bold ph-arrows-left-right"></i> So sánh
                        </button>
                    </div>
                    
                    <!-- Variants (Horizontal Full Width Rows) -->
                    <div style="display: flex; flex-direction: column; gap: 15px; margin-bottom: 25px; border-bottom: 1px dashed var(--border-color); padding-bottom: 20px;">
                        <!-- RAM Row -->
                        <div style="display: flex; align-items: center; gap: 15px; width: 100%;">
                            <span style="font-weight: 700; font-size: 0.95rem; color: var(--text-dark); width: 120px; flex-shrink: 0;">RAM DDR5</span>
                            <div class="nava-dropdown-wrapper" data-dropdown-type="ram" style="max-width: 395px; flex: 1; position: relative;">
                                <div class="nava-dropdown-display" style="width: 100%; border: 1px solid var(--border-color); border-radius: 8px; padding: 12px 15px; padding-right: 40px; background: var(--bg-gray); cursor: default; display: flex; justify-content: space-between; align-items: center; box-sizing: border-box; position: relative;">
                                    <span class="nava-dropdown-selected" id="ram-selected-text" style="font-weight: 700; font-size: 0.9rem; color: var(--text-dark);">NO RAM</span>
                                    <span class="nava-dropdown-selected-price" id="ram-selected-price" style="font-weight: 700; font-size: 0.9rem; color: var(--primary); margin-left: auto; margin-right: 5px;">+0đ</span>
                                    <i class="ph-bold ph-caret-down nava-dropdown-arrow" style="color: var(--text-gray); transition: transform 0.2s; position: absolute; right: 15px; top: 50%; transform: translateY(-50%);"></i>
                                </div>
                                <ul class="nava-dropdown-list">
                                    <li class="nava-dropdown-item active" onclick="selectVariantDropdown(this, 'ram', 0, 'NO RAM')" style="display: flex; justify-content: space-between; align-items: center; width: 100%; box-sizing: border-box;">
                                        <span>NO RAM</span>
                                        <span style="color: var(--primary); font-weight: 700;">+0đ</span>
                                    </li>
                                    <li class="nava-dropdown-item" onclick="selectVariantDropdown(this, 'ram', 1890000, '8GB - 4800')" style="display: flex; justify-content: space-between; align-items: center; width: 100%; box-sizing: border-box;">
                                        <span>8GB - 4800</span>
                                        <span style="color: var(--primary); font-weight: 700;">+1.890.000đ</span>
                                    </li>
                                    <li class="nava-dropdown-item" onclick="selectVariantDropdown(this, 'ram', 2090000, '8GB - 5600')" style="display: flex; justify-content: space-between; align-items: center; width: 100%; box-sizing: border-box;">
                                        <span>8GB - 5600</span>
                                        <span style="color: var(--primary); font-weight: 700;">+2.090.000đ</span>
                                    </li>
                                    <li class="nava-dropdown-item" onclick="selectVariantDropdown(this, 'ram', 3790000, '16GB - 4800')" style="display: flex; justify-content: space-between; align-items: center; width: 100%; box-sizing: border-box;">
                                        <span>16GB - 4800</span>
                                        <span style="color: var(--primary); font-weight: 700;">+3.790.000đ</span>
                                    </li>
                                    <li class="nava-dropdown-item" onclick="selectVariantDropdown(this, 'ram', 4190000, '16GB - 5600')" style="display: flex; justify-content: space-between; align-items: center; width: 100%; box-sizing: border-box;">
                                        <span>16GB - 5600</span>
                                        <span style="color: var(--primary); font-weight: 700;">+4.190.000đ</span>
                                    </li>
                                    <li class="nava-dropdown-item" onclick="selectVariantDropdown(this, 'ram', 6990000, '32GB - 4800')" style="display: flex; justify-content: space-between; align-items: center; width: 100%; box-sizing: border-box;">
                                        <span>32GB - 4800</span>
                                        <span style="color: var(--primary); font-weight: 700;">+6.990.000đ</span>
                                    </li>
                                </ul>
                            </div>
                        </div>
                        
                        <!-- SSD Row -->
                        <div style="display: flex; align-items: center; gap: 15px; width: 100%;">
                            <span style="font-weight: 700; font-size: 0.95rem; color: var(--text-dark); width: 120px; flex-shrink: 0;">SSD NVMe</span>
                            <div class="nava-dropdown-wrapper" data-dropdown-type="ssd" style="max-width: 395px; flex: 1; position: relative;">
                                <div class="nava-dropdown-display" style="width: 100%; border: 1px solid var(--border-color); border-radius: 8px; padding: 12px 15px; padding-right: 40px; background: var(--bg-gray); cursor: default; display: flex; justify-content: space-between; align-items: center; box-sizing: border-box; position: relative;">
                                    <span class="nava-dropdown-selected" id="ssd-selected-text" style="font-weight: 700; font-size: 0.9rem; color: var(--text-dark);">NO SSD</span>
                                    <span class="nava-dropdown-selected-price" id="ssd-selected-price" style="font-weight: 700; font-size: 0.9rem; color: var(--primary); margin-left: auto; margin-right: 5px;">+0đ</span>
                                    <i class="ph-bold ph-caret-down nava-dropdown-arrow" style="color: var(--text-gray); transition: transform 0.2s; position: absolute; right: 15px; top: 50%; transform: translateY(-50%);"></i>
                                </div>
                                <ul class="nava-dropdown-list">
                                    <li class="nava-dropdown-item active" onclick="selectVariantDropdown(this, 'ssd', 0, 'NO SSD')" style="display: flex; justify-content: space-between; align-items: center; width: 100%; box-sizing: border-box;">
                                        <span>NO SSD</span>
                                        <span style="color: var(--primary); font-weight: 700;">+0đ</span>
                                    </li>
                                    <li class="nava-dropdown-item" onclick="selectVariantDropdown(this, 'ssd', 1190000, '256GB')" style="display: flex; justify-content: space-between; align-items: center; width: 100%; box-sizing: border-box;">
                                        <span>256GB</span>
                                        <span style="color: var(--primary); font-weight: 700;">+1.190.000đ</span>
                                    </li>
                                    <li class="nava-dropdown-item" onclick="selectVariantDropdown(this, 'ssd', 2290000, '500GB')" style="display: flex; justify-content: space-between; align-items: center; width: 100%; box-sizing: border-box;">
                                        <span>500GB</span>
                                        <span style="color: var(--primary); font-weight: 700;">+2.290.000đ</span>
                                    </li>
                                    <li class="nava-dropdown-item" onclick="selectVariantDropdown(this, 'ssd', 3990000, '1TB')" style="display: flex; justify-content: space-between; align-items: center; width: 100%; box-sizing: border-box;">
                                        <span>1TB</span>
                                        <span style="color: var(--primary); font-weight: 700;">+3.990.000đ</span>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Actions (Updated to column N layout) -->
                    <div style="display: flex; flex-direction: column; gap: 15px; margin-bottom: 25px;">
                        <!-- Row 1: Quantity Spinner & Price -->
                        <div class="qty-price-row" style="display: flex; align-items: center; justify-content: space-between; gap: 15px; width: 100%;">
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <span style="font-weight: 700; font-size: 0.95rem; color: var(--text-dark);"><span class="desktop-qty-label">Số lượng</span><span class="mobile-qty-label">SL</span></span>
                                <div class="qty-selector" style="display: inline-flex; align-items: center; border: 1px solid var(--border-color); border-radius: 8px; overflow: hidden; background: var(--bg-gray);">
                                    <button class="qty-adjust" onclick="adjustQty(-1)" style="width: 32px; height: 32px; border: none; background: transparent; cursor: pointer; font-weight: bold; color: var(--text-dark); transition: 0.2s;" onmouseover="this.style.background='rgba(0,0,0,0.05)'" onmouseout="this.style.background='transparent'">-</button>
                                    <input type="text" value="1" class="qty-val" id="qty-val-main" readonly style="width: 36px; height: 32px; text-align: center; border: none; background: transparent; font-weight: 700; font-size: 0.9rem; color: var(--text-dark); outline: none;">
                                    <button class="qty-adjust" onclick="adjustQty(1)" style="width: 32px; height: 32px; border: none; background: transparent; cursor: pointer; font-weight: bold; color: var(--text-dark); transition: 0.2s;" onmouseover="this.style.background='rgba(0,0,0,0.05)'" onmouseout="this.style.background='transparent'">+</button>
                                </div>
                            </div>
                            <div class="prod-price" id="main-price" style="font-size: 1.8rem; font-weight: 900; color: var(--primary); letter-spacing: -0.5px; margin: 0;">12.390.000đ</div>
                        </div>
 
                        <!-- Row 2: Add-to-cart, Trả Góp 0%, MUA NGAY -->
                        <div class="action-buttons-row" style="display: flex; align-items: center; gap: 10px; width: 100%; height: 50px;">
                            <!-- Icon Cart Button -->
                            <button id="btn-add-to-cart-main" style="width: 50px; height: 50px; border-radius: 8px; border: 1px solid var(--primary); background: transparent; color: var(--primary); font-family: inherit; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s;" onmouseover="this.style.background='rgba(0, 51, 102, 0.05)'" onmouseout="this.style.background='transparent'">
                                <i class="ph-bold ph-shopping-cart" style="font-size: 1.4rem;"></i>
                            </button>
                            
                            <!-- Trả góp 0% Button -->
                            <button id="btn-installment-main" onclick="window.location.href='demo_checkout.html'" style="flex: 1; height: 50px; border-radius: 8px; border: 1.5px solid var(--primary); background: transparent; color: var(--primary); font-family: inherit; font-weight: 800; font-size: 0.95rem; cursor: pointer; text-transform: uppercase; transition: all 0.2s;" onmouseover="this.style.background='rgba(0, 51, 102, 0.05)'" onmouseout="this.style.background='transparent'">
                                TRẢ GÓP 0%
                            </button>
                            
                            <!-- Mua Ngay Button -->
                            <button id="btn-buy-now-main" style="flex: 1.5; height: 50px; border-radius: 8px; border: none; background: linear-gradient(90deg, var(--primary), var(--secondary)); color: white; font-family: inherit; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.2s; box-shadow: 0 4px 15px rgba(0, 51, 102, 0.2);" onmouseover="this.style.transform='translateY(-1px)'; this.style.boxShadow='0 6px 20px rgba(0, 51, 102, 0.35)';" onmouseout="this.style.transform='none'; this.style.boxShadow='0 4px 15px rgba(0, 51, 102, 0.2)';">
                                <span style="font-weight: 800; font-size: 0.95rem; text-transform: uppercase; letter-spacing: 0.5px;">MUA NGAY</span>
                            </button>
                        </div>
                    </div>
                    
                    <div class="policy-box" style="border: 1px solid #e2e8f0; border-radius: 12px; padding: 12px 16px; background: #f8fafc;">
                        <div class="policy-mobile-box" style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                            <div class="policy-item" style="display: flex; align-items: center; gap: 8px; font-size: 0.85rem; color: #334155; font-weight: 600;">
                                <i class="ph ph-shield-check" style="font-size: 1.3rem; color: var(--primary);"></i> Bảo hành chính hãng 36 tháng
                            </div>
                            <div class="policy-item" style="display: flex; align-items: center; gap: 8px; font-size: 0.85rem; color: #334155; font-weight: 600;">
                                <i class="ph ph-truck" style="font-size: 1.3rem; color: var(--primary);"></i> Giao hàng miễn phí
                            </div>
                        </div>
                    </div>
                    

                </div>
            </div>
            
            <!-- Product Details Grid -->
            <div style="margin-bottom: 80px; width: 100%;">
                <style>
                    .product-details-grid { display: flex; flex-direction: column; gap: 30px; }
                    .desc-column { background: #fff; border-radius: 16px; border: 1px solid #e2e8f0; padding: 32px; flex: 1; min-width: 0; }
                    .desc-column iframe { display: block; margin: 0 auto 20px auto; border-radius: 16px; width: 100%; aspect-ratio: 16/9; height: auto; border: none; }
                    .desc-column img { max-width: 100%; height: auto; display: block; margin: 24px auto; border-radius: 12px; }
                    .desc-column p { line-height: 1.8; color: #475569; margin-bottom: 20px; font-size: 0.95rem; }
                    .desc-column h2 { font-size: 1.3rem; font-weight: 700; color: #0f172a; margin-top: 32px; margin-bottom: 16px; }
                    .desc-column h3 { font-size: 1.15rem; font-weight: 700; color: #0f172a; margin-top: 24px; margin-bottom: 12px; }
                    .desc-column hr { border: 0; border-top: 1px dashed #e2e8f0; margin: 32px 0; }
                    .desc-column ul { margin-bottom: 20px; padding-left: 20px; }
                    .desc-column li { margin-bottom: 8px; line-height: 1.7; color: #475569; font-size: 0.95rem; }
                    
                    .desc-content-wrapper {
                        position: relative;
                        max-height: 1200px;
                        overflow: hidden;
                        transition: max-height 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                    }
                    .desc-content-wrapper.expanded {
                        max-height: 5000px;
                    }
                    .desc-overlay {
                        position: absolute;
                        bottom: 0;
                        left: 0;
                        width: 100%;
                        height: 140px;
                        background: linear-gradient(to bottom, rgba(255,255,255,0), #ffffff);
                        pointer-events: none;
                        transition: opacity 0.3s ease;
                    }
                    [data-theme="dark"] .desc-overlay {
                        background: linear-gradient(to bottom, rgba(15,23,42,0), var(--bg-white, #1e293b));
                    }
                    .desc-content-wrapper.expanded .desc-overlay {
                        opacity: 0;
                    }
                    .btn-show-more {
                        background: #fff;
                        border: 1px solid var(--primary);
                        color: var(--primary);
                        font-weight: 700;
                        padding: 10px 28px;
                        border-radius: 8px;
                        cursor: pointer;
                        display: inline-flex;
                        align-items: center;
                        gap: 8px;
                        font-size: 0.9rem;
                        transition: all 0.2s;
                        box-shadow: 0 4px 12px rgba(14,165,233,0.05);
                    }
                    .btn-show-more:hover {
                        background: var(--primary);
                        color: #fff;
                        box-shadow: 0 6px 16px rgba(14,165,233,0.25);
                    }
                    [data-theme="dark"] .btn-show-more {
                        background: rgba(51, 133, 255, 0.1);
                        border-color: rgba(51, 133, 255, 0.4);
                        color: #66a3ff;
                    }
                    [data-theme="dark"] .btn-show-more:hover {
                        background: var(--primary);
                        color: #fff;
                    }
                    
                    .specs-column { background: #ffffff; border-radius: 16px; padding: 24px; border: 1px solid #e2e8f0; }
                    .nava-spec-grid { display: flex; flex-direction: column; }
                    .nava-spec-row { display: grid; grid-template-columns: 120px 1fr; gap: 16px; padding: 12px 0; border-bottom: 1px solid #e2e8f0; }
                    .nava-spec-row:last-child { border-bottom: none; }
                    .nava-spec-label { color: #64748b; font-weight: 500; font-size: 0.85rem; }
                    .nava-spec-value { color: #0f172a; font-weight: 600; font-size: 0.85rem; line-height: 1.4; word-break: break-word; }
                    @media (min-width: 992px) {
                        .product-details-grid { flex-direction: row; align-items: flex-start; gap: 40px; }
                        .desc-column { flex: 1; min-width: 0; }
                        .specs-column { width: 380px; flex-shrink: 0; position: sticky; top: 160px; }
                        .nava-spec-grid {
                            max-height: calc(100vh - 280px);
                            overflow-y: auto;
                            -webkit-overflow-scrolling: touch !important;
                            padding-right: 8px;
                        }
                        /* Scrollbar styling */
                        .nava-spec-grid::-webkit-scrollbar {
                            width: 6px;
                        }
                        .nava-spec-grid::-webkit-scrollbar-track {
                            background: transparent;
                        }
                        .nava-spec-grid::-webkit-scrollbar-thumb {
                            background: #cbd5e1;
                            border-radius: 3px;
                        }
                        .nava-spec-grid::-webkit-scrollbar-thumb:hover {
                            background: #94a3b8;
                        }
                    }
                    @media (max-width: 991px) {
                        .nava-spec-grid {
                            max-height: 380px !important;
                            overflow-y: auto !important;
                            -webkit-overflow-scrolling: touch !important;
                            padding-right: 8px;
                            scrollbar-width: none;
                            -ms-overflow-style: none;
                        }
                        .nava-spec-grid::-webkit-scrollbar {
                            display: none;
                        }
                    }
                </style>
                
                <div class="product-details-grid">
                    <!-- Left: Description -->
                    <div class="desc-column">
                        <h2 style="font-size: 1.4rem; font-weight: 700; margin-bottom: 24px; color: #0f172a;">Đặc điểm nổi bật</h2>
                        <div class="desc-content-wrapper" id="desc-wrapper">
                            <div class="position-relative rte">
 <p>
  <lite-youtube videoid="g5x0nIzBEWU" style="background-image: url('https://img.youtube.com/vi/g5x0nIzBEWU/maxresdefault.jpg'); border-radius: 8px;"></lite-youtube>
 </p>
 <p>
  <lite-youtube videoid="Wrc43VVRJnA" style="background-image: url('https://img.youtube.com/vi/Wrc43VVRJnA/maxresdefault.jpg'); border-radius: 8px;"></lite-youtube>
 </p>
 <h2 data-pm-slice="1 1 []" dir="ltr">
  <strong>
   Đỉnh Cao Hiệu Suất Trong Thiết Kế Nhỏ Gọn
  </strong>
 </h2>
 <p dir="ltr">
  ASUS NUC AI 350 (PN54) là mẫu Mini PC tiên phong được trang bị bộ vi xử lý AMD Ryzen™ AI 300 Series, mang đến hiệu suất vượt trội và khả năng xử lý trí tuệ nhân tạo (AI) tiên tiến. Với thiết kế siêu nhỏ gọn, độ bền đạt chuẩn quân đội MIL-STD-810H, và tích hợp công nghệ Copilot+ PC, ASUS NUC AI 350 (PN54) là giải pháp lý tưởng cho các ứng dụng văn phòng, bán lẻ thông minh, biển báo kỹ thuật số, và giải trí tại gia. Được tối ưu hóa cho các tác vụ đòi hỏi hiệu suất cao, sản phẩm này không chỉ đáp ứng nhu cầu hiện tại mà còn định hình tương lai công nghệ với khả năng AI vượt trội.
 </p>
 <p dir="ltr" style="text-align: center;">
  <img data-thumb="original" original-height="692" original-width="692" src="//bizweb.dktcdn.net/100/543/817/files/w692-646e17e0-bbb8-46a8-abc4-7d7c5c7a9734.png?v=1763981380383"/>
 </p>
 <p dir="ltr">
  <img data-thumb="original" original-height="699" original-width="1632" src="//bizweb.dktcdn.net/100/543/817/files/asus-nuc-ai-350-pn54-overview.jpg?v=1760324778855"/>
 </p>
 <hr/>
 <h2 dir="ltr">
  <strong>
   Hiệu Suất Vượt Trội Với Bộ Vi Xử Lý AMD Ryzen™ AI 300 Series
  </strong>
 </h2>
 <p dir="ltr">
  ASUS NUC AI 350 (PN54) được trang bị bộ vi xử lý AMD Ryzen™ AI 300 Series với tối đa 12 lõi siêu nhanh và kiến trúc XDNA2 NPU, cung cấp hiệu suất AI lên đến 50 TOPS. So với thế hệ XDNA™ đầu tiên, ASUS NUC AI 350 (PN54) mang lại hiệu suất AI nhanh hơn gấp 5 lần, đảm bảo xử lý mượt mà các tác vụ AI phức tạp như tạo nội dung, phân tích dữ liệu lớn, và tối ưu hóa quy trình làm việc. Bộ vi xử lý này được tối ưu hóa cho các ứng dụng AI mới nhất và hệ điều hành Windows, mang đến trải nghiệm mượt mà, nhanh chóng và thông minh hơn.
 </p>
 <p dir="ltr">
  <img data-thumb="original" original-height="688" original-width="1527" src="//bizweb.dktcdn.net/100/543/817/files/asus-nuc-ai-350-pn54-wifi6e-bt-2c9d7913-7d53-46e3-b646-beb021384ff2.jpg?v=1760950730370"/>
 </p>
 <p dir="ltr">
  Bộ nhớ
  <strong>
   DDR5
  </strong>
  max 5600 tốc độ cao, với băng thông tăng 50% ở mức điện áp chỉ 1.1V, giúp
  <strong>
   ASUS NUC AI 350 (PN54)
  </strong>
  xử lý các tác vụ nặng như chỉnh sửa video 4K, quản lý cơ sở dữ liệu lớn, và đa nhiệm hiệu quả. Công nghệ làm mát thông minh đảm bảo hiệu suất ổn định ngay cả trong môi trường làm việc liên tục 24/7, giúp tối ưu hóa năng lượng và giảm thiểu tiếng ồn.
 </p>
 <hr/>
 <h2 dir="ltr">
  <strong>
   Điểm Nổi Bật Của Hiệu Suất
  </strong>
 </h2>
 <ul data-tight="true" dir="ltr">
  <li>
   <p dir="ltr">
    Hiệu Suất AI Vượt Trội: Lên đến 50 TOPS, hỗ trợ các công cụ AI như Text to Image, Generative Fill, và Object Add/Remove, giúp đơn giản hóa quy trình sáng tạo nội dung.
   </p>
  </li>
  <li>
   <p dir="ltr">
    Đa Nhiệm Mượt Mà: 12 lõi siêu nhanh và bộ nhớ DDR5 đảm bảo xử lý nhanh chóng các tác vụ phức tạp.
   </p>
  </li>
  <li>
   <p dir="ltr">
    Tiết Kiệm Năng Lượng: Tiêu thụ năng lượng thấp hơn 40% so với các dòng Mini PC thông thường, phù hợp với các tiêu chuẩn tiết kiệm năng lượng nghiêm ngặt.
   </p>
  </li>
 </ul>
 <p dir="ltr">
  <img data-thumb="original" original-height="753" original-width="1757" src="//bizweb.dktcdn.net/100/543/817/files/asus-nuc-ai-350-pn54-cpu.jpg?v=1760325120134"/>
 </p>
 <hr/>
 <h2 dir="ltr">
  <strong>
   AMD Radeon™ 860M Graphics
  </strong>
 </h2>
 <p dir="ltr">
  <strong>
   ASUS NUC AI 350 (PN54)
  </strong>
  tích hợp card đồ họa
  <strong>
   AMD Radeon™ 860M
  </strong>
  , mang đến khả năng hiển thị xuất sắc với độ phân giải 4K trên tối đa bốn màn hình đồng thời. Điều này khiến
  <strong>
   ASUS NUC AI 350 (PN54)
  </strong>
  trở thành lựa chọn lý tưởng cho các ứng dụng như biển báo kỹ thuật số, trình chiếu đa phương tiện, hoặc thiết lập không gian làm việc đa màn hình. Card đồ họa Radeon™ 860M còn hỗ trợ chơi game nhẹ, đáp ứng nhu cầu giải trí của người dùng trong giờ nghỉ.
 </p>
 <p dir="ltr">
  <img data-thumb="original" original-height="720" original-width="1280" src="//bizweb.dktcdn.net/100/543/817/files/860m.jpg?v=1755682730132"/>
 </p>
 <h3 dir="ltr">
  Ứng Dụng Đồ Họa
 </h3>
 <ul data-tight="true" dir="ltr">
  <li>
   <p dir="ltr">
    <strong>
     Hiển Thị Đa Màn Hình
    </strong>
    : Kết nối đồng thời bốn màn hình 4K, lý tưởng cho các ứng dụng bán lẻ, văn phòng, hoặc giải trí tại gia.
   </p>
  </li>
  <li>
   <p dir="ltr">
    <strong>
     Chỉnh Sửa Video 4K
    </strong>
    : Khả năng xử lý đồ họa mạnh mẽ giúp chỉnh sửa video mượt mà, đáp ứng nhu cầu của các nhà sáng tạo nội dung.
   </p>
  </li>
  <li>
   <p dir="ltr">
    <strong>
     Hiệu Suất Đồ Họa Cao
    </strong>
    : Radeon™ 800M đảm bảo trải nghiệm hình ảnh sắc nét, màu sắc sống động, và hiệu ứng mượt mà.
   </p>
  </li>
 </ul>
 <p dir="ltr">
 </p>
 <hr/>
 <h2 dir="ltr">
  <strong>
   Kết Nối Siêu Nhanh Và Linh Hoạt
  </strong>
 </h2>
 <p dir="ltr">
  <strong>
   ASUS NUC AI 350 (PN54)
  </strong>
  được trang bị bộ kết nối tiên tiến, bao gồm Wi-Fi 6E từ MediaTek, Bluetooth 5.3, và tùy chọn LAN 2.5G, đảm bảo tốc độ truyền dữ liệu nhanh chóng và ổn định. Với sáu cổng USB, hai cổng DisplayPort, và hỗ trợ USB 4, PN54 đáp ứng mọi nhu cầu kết nối từ văn phòng hiện đại đến các hệ thống bán lẻ thông minh. Công nghệ Wi-Fi 6E cho phép kết nối đồng thời lên đến 16 thiết bị, đảm bảo hiệu suất mạng tối ưu ngay cả trong môi trường đông đúc.
 </p>
 <p dir="ltr">
  <br/>
  <img data-thumb="original" original-height="1035" original-width="1500" src="//bizweb.dktcdn.net/100/543/817/files/mini-pc-asus-nuc-ai-350-2.jpg?v=1763981401892">
   <img data-thumb="original" original-height="990" original-width="1300" src="//bizweb.dktcdn.net/100/543/817/files/vn-11134208-820l4-mfp9kvo3rtal15-resize-w1750-nl.jpg?v=1760325260948"/>
  </img>
 </p>
 <hr/>
 <h2 dir="ltr">
  <strong>
   Đặc Điểm Kết Nối
  </strong>
 </h2>
 <ul data-tight="true" dir="ltr">
  <li>
   <p dir="ltr">
    <strong>
     Wi-Fi 6E:
    </strong>
    Tốc độ tải xuống nhanh hơn và truyền dữ liệu ổn định, lý tưởng cho các ứng dụng trực tuyến và đám mây.
   </p>
  </li>
  <li>
   <p dir="ltr">
    <strong>
     LAN 2.5G
    </strong>
    : Hỗ trợ kết nối mạng đa thiết bị, phù hợp với các hệ thống phức tạp như trung tâm dữ liệu hoặc bán lẻ thông minh.
   </p>
  </li>
  <li>
   <p dir="ltr">
    <strong>
     USB 4
    </strong>
    : Tốc độ truyền dữ liệu siêu nhanh, đáp ứng nhu cầu kết nối với các thiết bị ngoại vi hiện đại.
   </p>
  </li>
 </ul>
 <p dir="ltr">
 </p>
 <hr/>
 <h2 dir="ltr">
  <strong>
   Bảo Mật Cao Cấp Với Công Nghệ Tiên Tiến
  </strong>
 </h2>
 <p dir="ltr">
  Bảo mật là ưu tiên hàng đầu của ASUS ExpertCenter PN54. Sản phẩm tích hợp công nghệ nhận diện dấu vân tay, cho phép đăng nhập Windows Hello nhanh chóng và an toàn, thay thế mật khẩu truyền thống bằng dữ liệu sinh trắc học mã hóa. Mô-đun TPM (Trusted Platform Module) tùy chọn cung cấp mã hóa dựa trên phần cứng, bảo vệ dữ liệu khỏi các truy cập trái phép. Ngoài ra, phím Copilot chuyên dụng cho phép kích hoạt tức thì các tính năng AI, nâng cao hiệu quả công việc và bảo mật.
 </p>
 <p dir="ltr">
  <img data-thumb="original" original-height="953" original-width="1653" src="//bizweb.dktcdn.net/100/543/817/files/asus-nuc-ai-350-pn54-npu-copilot-plus-pc.jpg?v=1760325275931"/>
 </p>
 <h3 dir="ltr">
  <strong>
   Tính Năng Bảo Mật
  </strong>
 </h3>
 <ul data-tight="true" dir="ltr">
  <li>
   <p dir="ltr">
    <strong>
     Nhận Diện Dấu Vân Tay
    </strong>
    : Đăng nhập an toàn và tiện lợi, bảo vệ dữ liệu cá nhân và doanh nghiệp.
   </p>
  </li>
  <li>
   <p dir="ltr">
    TPM Tùy Chọn: Mã hóa phần cứng giúp bảo vệ dữ liệu khỏi các mối đe dọa an ninh mạng.
   </p>
  </li>
  <li>
   <p dir="ltr">
    <strong>
     Phím Copilot
    </strong>
    : Kích hoạt nhanh các tính năng AI, tối ưu hóa quy trình làm việc và cá nhân hóa trải nghiệm người dùng.
   </p>
  </li>
 </ul>
 <hr/>
 <h2 dir="ltr">
  <strong>
   Thiết Kế Nhỏ Gọn, Độ Bền Chuẩn Quân Đội
  </strong>
 </h2>
 <p dir="ltr">
  Với kích thước chỉ 130 x 130 x 34mm,
  <strong>
   ASUS NUC AI 350 (PN54)
  </strong>
  là một trong những Mini PC nhỏ gọn nhất trên thị trường, dễ dàng phù hợp với mọi không gian làm việc. Dù nhỏ gọn, sản phẩm vẫn đạt chuẩn độ bền quân đội MIL-STD-810H, vượt qua các bài kiểm tra khắc nghiệt về sốc, nhiệt độ cực đoan, cát bụi, và rung lắc. Thiết kế mô-đun không cần dụng cụ cho phép nâng cấp bộ nhớ và lưu trữ dễ dàng, đảm bảo khả năng mở rộng trong tương lai.
 </p>
 <p dir="ltr">
  <img data-thumb="original" original-height="746" original-width="1500" src="//bizweb.dktcdn.net/100/543/817/files/mini-pc-asus-nuc-ai-350.jpg?v=1763981435550"/>
 </p>
 <h3 dir="ltr">
  <strong>
   Đặc Điểm Thiết Kế
  </strong>
 </h3>
 <ul data-tight="true" dir="ltr">
  <li>
   <p dir="ltr">
    Kích Thước Siêu Nhỏ: Tiết kiệm không gian, phù hợp với văn phòng, cửa hàng bán lẻ, hoặc giải trí tại gia.
   </p>
  </li>
  <li>
   <p dir="ltr">
    Độ Bền MIL-STD-810H: Đảm bảo hoạt động ổn định trong các điều kiện môi trường khắc nghiệt.
   </p>
  </li>
  <li>
   <p dir="ltr">
    Nâng Cấp Dễ Dàng: Thiết kế mô-đun giúp thay thế hoặc nâng cấp RAM và SSD mà không cần dụng cụ chuyên dụng.
   </p>
  </li>
 </ul>
 <hr/>
 <h2 dir="ltr">
  <strong>
   Tính Bền Vững Và Tiết Kiệm Năng Lượng
  </strong>
 </h2>
 <p dir="ltr">
  ASUS cam kết xây dựng tương lai bền vững với ExpertCenter PN54. Sản phẩm sử dụng vật liệu thân thiện với môi trường và đạt tiêu chuẩn EPEAT Climate+, đồng thời cung cấp hiệu suất năng lượng vượt trội với mức tiết kiệm năng lượng lên đến 40%. Quy trình sản xuất của ASUS tuân thủ các tiêu chuẩn ESG cao, đảm bảo giảm thiểu tác động đến môi trường mà vẫn duy trì hiệu suất tối ưu.
 </p>
 <p dir="ltr">
  <img data-thumb="original" original-height="812" original-width="1973" src="//bizweb.dktcdn.net/100/543/817/files/asus-nuc-ai-350-pn54-bao-ve-moi-truong.jpg?v=1760325294990"/>
 </p>
 <h3 dir="ltr">
  Cam Kết Bền Vững
 </h3>
 <ul data-tight="true" dir="ltr">
  <li>
   <p dir="ltr">
    Vật Liệu Thân Thiện Môi Trường: Đáp ứng tiêu chuẩn EPEAT Climate+, giảm thiểu tác động đến môi trường.
   </p>
  </li>
  <li>
   <p dir="ltr">
    Tiết Kiệm Năng Lượng: Giảm 40% tiêu thụ năng lượng, lý tưởng cho các doanh nghiệp chú trọng đến hiệu quả năng lượng.
   </p>
  </li>
  <li>
   <p dir="ltr">
    Sản Xuất Bền Vững: Quy trình sản xuất tuân thủ các tiêu chuẩn ESG, góp phần xây dựng tương lai xanh.
   </p>
  </li>
 </ul>
 <hr/>
 <h2 dir="ltr">
  <strong>
   Ứng Dụng Đa Dạng Cho Mọi Nhu Cầu
  </strong>
 </h2>
 <p dir="ltr">
  ASUS ExpertCenter PN54 là giải pháp toàn diện cho nhiều lĩnh vực, từ văn phòng hiện đại, bán lẻ thông minh, đến giải trí tại gia. Với khả năng hỗ trợ AI cục bộ, sản phẩm đảm bảo bảo mật dữ liệu tối ưu, đặc biệt quan trọng đối với các doanh nghiệp xử lý thông tin nhạy cảm. PN54 còn lý tưởng cho các nhà sáng tạo nội dung, với khả năng xử lý các tác vụ như chỉnh sửa video 4K, tạo hình ảnh bằng AI, và quản lý dữ liệu lớn.
 </p>
 <p dir="ltr">
  <img data-thumb="original" original-height="357" original-width="1249" src="//bizweb.dktcdn.net/100/543/817/files/screenshot-2025-08-20-164533.jpg?v=1755683147185"/>
 </p>
 <h3 dir="ltr">
  Ứng Dụng Cụ Thể
 </h3>
 <ul data-tight="true" dir="ltr">
  <li>
   <p dir="ltr">
    Văn Phòng Hiện Đại: Hỗ trợ đa nhiệm, kết nối đa màn hình, và các công cụ AI để tăng năng suất.
   </p>
  </li>
  <li>
   <p dir="ltr">
    Bán Lẻ Thông Minh: Hỗ trợ biển báo kỹ thuật số, kết nối mạng tốc độ cao, và thiết kế nhỏ gọn cho không gian hạn chế.
   </p>
  </li>
  <li>
   <p dir="ltr">
    Giải Trí Tại Gia: Hỗ trợ hiển thị 4K và chơi game nhẹ, mang đến trải nghiệm giải trí đỉnh cao.
   </p>
  </li>
 </ul>
 <p dir="ltr">
  <img data-thumb="original" original-height="721" original-width="1643" src="//bizweb.dktcdn.net/100/543/817/files/asus-nuc-ai-350-pn54-ung-dung.jpg?v=1760325316050"/>
 </p>
 <hr/>
 <h2 dir="ltr">
  <strong>
   Thông Số Kỹ Thuật
  </strong>
 </h2>
 <ul data-tight="true" dir="ltr">
  <li>
   <p dir="ltr">
    Bộ Vi Xử Lý: AMD Ryzen™ AI 300 Series (tùy chọn Ryzen AI 5 340, Ryzen AI 5 350, Ryzen AI 7 350)
   </p>
  </li>
  <li>
   <p dir="ltr">
    Đồ Họa: AMD Radeon™ 800M (Radeon 860M với Ryzen AI 7 350)
   </p>
  </li>
  <li>
   <p dir="ltr">
    Bộ Nhớ: Hỗ trợ lên đến 128GB DDR5 RAM
   </p>
  </li>
  <li>
   <p dir="ltr">
    Lưu Trữ: Hỗ trợ lên đến 2TB M.2 NVMe SSD
   </p>
  </li>
  <li>
   <p dir="ltr">
    Kết Nối: Wi-Fi 6E, Bluetooth 5.2,LAN 2.5G, USB 4, sáu cổng USB, hai cổng DisplayPort
   </p>
  </li>
  <li>
   <p dir="ltr">
    Hệ Điều Hành: Windows 11
   </p>
  </li>
  <li>
   <p dir="ltr">
    Bảo Mật: Nhận diện dấu vân tay, TPM tùy chọn, phím Copilot
   </p>
  </li>
  <li>
   <p dir="ltr">
    Kích Thước: 130 x 130 x 34mm
   </p>
  </li>
  <li>
   <p dir="ltr">
    Độ Bền: Chuẩn quân đội MIL-STD-810H
   </p>
  </li>
  <li>
   <p dir="ltr">
    Tiết Kiệm Năng Lượng: Tiêu thụ năng lượng thấp hơn 40%, đạt chuẩn EPEAT Climate+
   </p>
  </li>
 </ul>
 <p dir="ltr">
  <img data-thumb="original" original-height="1149" original-width="1500" src="//bizweb.dktcdn.net/100/543/817/files/mini-pc-asus-nuc-ai-350-3.jpg?v=1763981447557"/>
 </p>
 <hr/>
 <h2 dir="ltr">
  <strong>
   Kết Luận
  </strong>
 </h2>
 <p dir="ltr">
  ASUS NUC AI 350 (PN54) là sự kết hợp hoàn hảo giữa hiệu suất mạnh mẽ, thiết kế nhỏ gọn, và công nghệ AI tiên tiến. Với bộ vi xử lý AMD Ryzen™ AI 300 Series, đồ họa Radeon™ 800M, và khả năng kết nối vượt trội, PN54 không chỉ đáp ứng nhu cầu hiện tại mà còn sẵn sàng cho tương lai. Độ bền chuẩn quân đội, bảo mật cao cấp, và cam kết bền vững khiến sản phẩm này trở thành lựa chọn hàng đầu cho các doanh nghiệp, nhà sáng tạo nội dung, và người dùng cá nhân. Hãy khám phá ASUS ExpertCenter PN54 ngay hôm nay để trải nghiệm công nghệ đỉnh cao trong tầm tay!
 </p>
 <p>
  <lite-youtube videoid="_er1aM1m2Ho" style="background-image: url('https://img.youtube.com/vi/_er1aM1m2Ho/maxresdefault.jpg'); border-radius: 8px;"></lite-youtube>
 </p>
</div>
                            <div class="desc-overlay"></div>
                        </div>
                        <div style="text-align: center; margin-top: 20px;">
                            <button class="btn-show-more" onclick="toggleDescription()" id="btn-show-desc">Xem thêm <i class="ph-bold ph-caret-down"></i></button>
                        </div>
                    </div>
                    
                    <!-- Right: Technical Specs -->
                    <div class="specs-column">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                            <h2 style="font-size: 1.2rem; font-weight: 700; color: #0f172a; display: flex; align-items: center; gap: 8px; margin: 0;">
                                <i class="ph-fill ph-cpu" style="color: var(--primary);"></i> Thông số kỹ thuật
                            </h2>
                            <button type="button" class="btn-nava-compare-trigger" onclick="openCompareDrawerDirect()" style="background: transparent; border: 1px solid var(--border-color); border-radius: 6px; padding: 6px 12px; font-weight: 700; font-size: 0.85rem; color: var(--text-dark); cursor: pointer; display: inline-flex; align-items: center; gap: 6px; transition: all 0.2s;" onmouseover="this.style.borderColor='var(--primary)'; this.style.color='var(--primary)';" onmouseout="this.style.borderColor='var(--border-color)'; this.style.color='var(--text-dark)';">
                                <i class="ph-bold ph-arrows-left-right"></i> So sánh
                            </button>
                        </div>
                        
                        <div class="specs-scroll-wrapper" style="position: relative;">
                            <div class="nava-spec-grid" data-lenis-prevent>
                                <div class="nava-spec-row">
                                    <div class="nava-spec-label">Thương hiệu</div>
                                    <div class="nava-spec-value">Asus</div>
                                </div>
                                <div class="nava-spec-row">
                                    <div class="nava-spec-label">Model</div>
                                    <div class="nava-spec-value">NUC AI 350 (PN54)</div>
                                </div>
                                <div class="nava-spec-row">
                                    <div class="nava-spec-label">Tình trạng</div>
                                    <div class="nava-spec-value">Mới 100%</div>
                                </div>
                                <div class="nava-spec-row">
                                    <div class="nava-spec-label">Kích thước</div>
                                    <div class="nava-spec-value">130x130x34mm</div>
                                </div>
                                <div class="nava-spec-row">
                                    <div class="nava-spec-label">CPU</div>
                                    <div class="nava-spec-value">AMD Ryzen AI 7 350 8C/16T max 5.0Ghz</div>
                                </div>
                                <div class="nava-spec-row">
                                    <div class="nava-spec-label">CPU Mark</div>
                                    <div class="nava-spec-value">30.000</div>
                                </div>
                                <div class="nava-spec-row">
                                    <div class="nava-spec-label">GPU</div>
                                    <div class="nava-spec-value">AMD Radeon™ 860M</div>
                                </div>
                                <div class="nava-spec-row">
                                    <div class="nava-spec-label">G3D Mark</div>
                                    <div class="nava-spec-value">8.500</div>
                                </div>
                                <div class="nava-spec-row">
                                    <div class="nava-spec-label">Ram</div>
                                    <div class="nava-spec-value">2x DDR5 5600 tối đa 128GB</div>
                                </div>
                                <div class="nava-spec-row">
                                    <div class="nava-spec-label">SSD</div>
                                    <div class="nava-spec-value">2x M.2 2280 NVMe</div>
                                </div>
                                <div class="nava-spec-row">
                                    <div class="nava-spec-label">Kết nối không dây</div>
                                    <div class="nava-spec-value">Wi-Fi 6E (Gig+) 2x2 + Bluetooth® 5.4</div>
                                </div>
                                <div class="nava-spec-row">
                                    <div class="nava-spec-label">Cổng IO</div>
                                    <div class="nava-spec-value" style="font-weight: 600; line-height: 1.6;">
                                        1x USB 4<br>
                                        1x USB 3.2 Gen2 Type A (10G)<br>
                                        1x USB 2.0 Type A (5G)<br>
                                        1x HDMI2.1(FRL6)<br>
                                        2x DisplayPort 1.4<br>
                                        1x 2.5G RJ45 LAN<br>
                                        1x DC in
                                    </div>
                                </div>
                                <div class="nava-spec-row">
                                    <div class="nava-spec-label">Power</div>
                                    <div class="nava-spec-value">DC 120W</div>
                                </div>
                                <div class="nava-spec-row">
                                    <div class="nava-spec-label">Tính năng đặc biệt</div>
                                    <div class="nava-spec-value">Vân tay, Copilot+, lên đến 66 TOPS</div>
                                </div>
                                <div class="nava-spec-row">
                                    <div class="nava-spec-label">OS</div>
                                    <div class="nava-spec-value">Win 11 Pro, Office 2021</div>
                                </div>
                                <div class="nava-spec-row">
                                    <div class="nava-spec-label">Bảo hành</div>
                                    <div class="nava-spec-value">36 tháng</div>
                                </div>
                            </div>
                            <div class="specs-fade-overlay"></div>
                            <div class="specs-scroll-arrow"><i class="ph-bold ph-mouse"></i></div>
                        </div>
                        

                    </div>
                </div>
            </div>
            
            <!-- Shopee Reviews Section -->
            <div id="danh-gia-shopee" style="margin-bottom: 50px; background: var(--bg-white, #ffffff); border-radius: 16px; border: 1px solid var(--border-color, #e2e8f0); padding: 32px; box-sizing: border-box; width: 100%;">
                <h2 style="font-size: 1.4rem; font-weight: 800; color: var(--text-dark, #0f172a); margin-top: 0; margin-bottom: 24px; display: flex; align-items: center; gap: 10px;">
                    <i class="ph-fill ph-chat-centered-text" style="color: var(--primary, #1e3a8a); font-size: 1.6rem;"></i> ĐÁNH GIÁ SẢN PHẨM (TỪ SHOPEE)
                </h2>
                
                <div class="shopee-rating-summary" id="shopeeRatingSummary" style="display: none;">
                    <!-- JS will populate rating summary here -->
                </div>
                <div class="shopee-comments-list" id="shopeeCommentsList">
                    <!-- JS will populate realtime reviews here -->
                    <div class="text-center" style="padding: 40px; color: var(--text-gray);">
                        <i class="ph ph-spinner ph-spin" style="font-size: 2rem; color: var(--primary, #1e3a8a);"></i>
                        <p>Đang tải đánh giá từ Shopee...</p>
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
                        background: #ffffff !important;
                        border-radius: 16px;
                        border: 1px solid var(--border-color) !important;
                        padding: 15px;
                        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                        position: relative;
                        display: flex;
                        flex-direction: column;
                        height: 100%;
                        cursor: pointer;
                        overflow: hidden;
                        box-shadow: none !important;
                    }
                    .product-card:hover {
                        transform: translateY(-4px);
                        border-color: var(--primary) !important;
                        box-shadow: none !important;
                    }
                    .card-glow { display: none !important; }
                    .product-card:hover .card-glow { display: none !important; }
                    
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
                        filter: none !important;
                    }
                    .product-card:hover .product-img {
                        transform: scale(1.05);
                        filter: none !important;
                    }
                    .card-content {
                        padding: 15px 0 0 0; flex: 1; display: flex; flex-direction: column; z-index: 2;
                    }
                    .card-specs {
                        display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 12px;
                    }
                    .spec-pill {
                        background: var(--bg-gray); color: var(--text-gray); border: 1px solid var(--border-color); padding: 4px 8px; border-radius: 6px; font-size: 0.7rem; font-weight: 600; display: inline-block; white-space: nowrap; box-shadow: none;
                    }
                    .spec-pill.secondary {
                        background: var(--bg-gray); color: var(--text-gray); border: 1px solid var(--border-color); box-shadow: none; font-weight: 600;
                    }
                    .card-title {
                        font-size: 1rem; line-height: 1.4; margin-bottom: 10px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; height: 2.8em; font-weight: 700; color: #0f172a; transition: color 0.2s;
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
                            <button class="compare-btn" data-name="ASUS NUC 14 Essential Int" title="Thêm vào so sánh" onclick="event.stopPropagation(); toggleCompare(this, 'ASUS NUC 14 Essential Int', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png', '4.490.000đ')"><i class="ph ph-arrows-left-right"></i></button>
                            <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" alt="ASUS NUC 14" class="product-img">
                        </div>
                        <div class="card-content">
                            <div class="card-specs">
                                <span class="spec-pill">CPU 6.000</span>                                <span class="spec-pill secondary">GPU 1.200</span>
                                <span class="spec-pill">WIFI 6E</span>
                                <span class="spec-pill secondary">4 USB 3.2</span>
                                <span class="spec-pill secondary">2 TYPE C</span>
                            </div>
                            <h2 class="card-title">ASUS NUC 14 Essential Intel</h2>
                            <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">4.490.000đ</span>
                                
                            </div>
                        </div>
                    </div>
                    
                    <!-- Product 2 -->
                    <div class="product-card" onclick="window.location.href='demo_product.html'">
                        <div class="card-glow"></div>
                        <div class="card-image-wrap">
                            <button class="compare-btn" data-name="AtomMan G7 PT Mini PC" title="Thêm vào so sánh" onclick="event.stopPropagation(); toggleCompare(this, 'AtomMan G7 PT Mini PC', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png', '34.490.000đ')"><i class="ph ph-arrows-left-right"></i></button>
                            <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" alt="AtomMan G7 PT" class="product-img">
                        </div>
                        <div class="card-content">
                            <div class="card-specs">
                                <span class="spec-pill">CPU 40.000</span>                                <span class="spec-pill secondary">GPU 17...</span>
                                <span class="spec-pill">4 FAN S...</span>
                                <span class="spec-pill secondary">WIFI 7</span>
                            </div>
                            <h2 class="card-title">AtomMan G7 PT Mini PC</h2>
                            <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">34.490.000đ</span>
                                
                            </div>
                        </div>
                    </div>
                    
                    <!-- Product 3 -->
                    <div class="product-card" onclick="window.location.href='demo_product.html'">
                        <div class="card-glow"></div>
                        <div class="card-image-wrap">
                            <button class="compare-btn" data-name="Mini PC GMK EVO X1 32G" title="Thêm vào so sánh" onclick="event.stopPropagation(); toggleCompare(this, 'Mini PC GMK EVO X1 32G', '//bizweb.dktcdn.net/thumb/large/100/543/817/products/mini-pc-gmk-evo-x1-ai.jpg', '31.190.000đ')"><i class="ph ph-arrows-left-right"></i></button>
                            <img src="//bizweb.dktcdn.net/thumb/large/100/543/817/products/mini-pc-gmk-evo-x1-ai.jpg" alt="Mini PC GMK EVO" class="product-img">
                        </div>
                        <div class="card-content">
                            <div class="card-specs">
                                <span class="spec-pill">CPU 38.500</span>                                <span class="spec-pill secondary">GPU ...</span>
                                <span class="spec-pill">2 NVME</span>
                                <span class="spec-pill secondary">USB4</span>
                            </div>
                            <h2 class="card-title">Mini PC GMK EVO X1 32G</h2>
                            <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">31.190.000đ</span>
                                
                            </div>
                        </div>
                    </div>
                    
                    <!-- Product 4 -->
                    <div class="product-card" onclick="window.location.href='demo_product.html'">
                        <div class="card-glow"></div>
                        <div class="card-image-wrap">
                            <button class="compare-btn" data-name="Tablet Minisforum V3 SE" title="Thêm vào so sánh" onclick="event.stopPropagation(); toggleCompare(this, 'Tablet Minisforum V3 SE', '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_2.png', '23.090.000đ')"><i class="ph ph-arrows-left-right"></i></button>
                            <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_2.png" alt="Tablet Minisforum" class="product-img">
                        </div>
                        <div class="card-content">
                            <div class="card-specs">
                                <span class="spec-pill">CPU 22.000</span>                                <span class="spec-pill secondary">CPU ...</span>
                                <span class="spec-pill">WIFI 6</span>
                                <span class="spec-pill secondary">2 USB4</span>
                            </div>
                            <h2 class="card-title">Tablet Minisforum V3 SE</h2>
                            <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-top: auto; gap: 8px;">
                                <span style="color: var(--text-dark); font-weight: 800; font-size: 1.15rem;">23.090.000đ</span>
                                
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
                            <div class="sticky-price-display" id="sticky-price">12.390.000đ</div>
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
            
            <!-- Bottom Sheet Overlay & Drawer for quick configuration -->
            <div id="nava-bs-overlay" onclick="closeBottomSheet()"></div>
            <div id="nava-bottom-sheet" data-lenis-prevent>
                <!-- Header: Thumbnail, Price, and Title -->
                <div class="bs-header">
                    <img class="bs-thumb" src="//bizweb.dktcdn.net/thumb/large/100/543/817/products/mini-pc-asus-nuc-ai-350-pn54-ryzen-ai-7-350-gaming.jpg?v=1763971973973" alt="ASUS NUC AI 350">
                    <div class="bs-header-info">
                        <div class="bs-price-val" id="bs-price">12.390.000đ</div>
                        <div style="font-size: 0.9rem; color: var(--text-gray, #64748b); margin-top: 4px; font-weight: 600;">ASUS NUC AI 350</div>
                    </div>
                    <button class="bs-close-btn" onclick="closeBottomSheet()"><i class="ph ph-x"></i></button>
                </div>
                
                <!-- Body: RAM and SSD selectors, Quantity selector -->
                <div class="bs-body">
                    <div class="bs-options-row">
                        <!-- RAM Selector -->
                        <div class="bs-option-col">
                            <span class="bs-option-label-v2" style="font-weight: 700; font-size: 0.85rem; color: var(--text-gray, #64748b); margin-bottom: 6px; display: block;">RAM DDR5</span>
                            <div class="nava-dropdown-wrapper" data-dropdown-type="ram" style="position: relative; width: 100%;">
                                <div class="nava-dropdown-display" style="width: 100%; border: 1px solid var(--border-color); border-radius: 8px; padding: 12px 15px; padding-right: 40px; background: var(--bg-gray); cursor: default; display: flex; justify-content: space-between; align-items: center; box-sizing: border-box; position: relative;">
                                    <span class="nava-dropdown-selected" style="font-weight: 700; font-size: 0.9rem; color: var(--text-dark);">NO RAM</span>
                                    <span class="nava-dropdown-selected-price" style="font-weight: 700; font-size: 0.9rem; color: var(--primary); margin-left: auto; margin-right: 5px;">+0đ</span>
                                    <i class="ph-bold ph-caret-down nava-dropdown-arrow" style="color: var(--text-gray); transition: transform 0.2s; position: absolute; right: 15px; top: 50%; transform: translateY(-50%);"></i>
                                </div>
                                <ul class="nava-dropdown-list">
                                    <li class="nava-dropdown-item active" onclick="selectVariantDropdown(this, 'ram', 0, 'NO RAM')" style="display: flex; justify-content: space-between; align-items: center; width: 100%; box-sizing: border-box;">
                                        <span>NO RAM</span>
                                        <span style="color: var(--primary); font-weight: 700;">+0đ</span>
                                    </li>
                                    <li class="nava-dropdown-item" onclick="selectVariantDropdown(this, 'ram', 1890000, '8GB - 4800')" style="display: flex; justify-content: space-between; align-items: center; width: 100%; box-sizing: border-box;">
                                        <span>8GB - 4800</span>
                                        <span style="color: var(--primary); font-weight: 700;">+1.890.000đ</span>
                                    </li>
                                    <li class="nava-dropdown-item" onclick="selectVariantDropdown(this, 'ram', 2090000, '8GB - 5600')" style="display: flex; justify-content: space-between; align-items: center; width: 100%; box-sizing: border-box;">
                                        <span>8GB - 5600</span>
                                        <span style="color: var(--primary); font-weight: 700;">+2.090.000đ</span>
                                    </li>
                                    <li class="nava-dropdown-item" onclick="selectVariantDropdown(this, 'ram', 3790000, '16GB - 4800')" style="display: flex; justify-content: space-between; align-items: center; width: 100%; box-sizing: border-box;">
                                        <span>16GB - 4800</span>
                                        <span style="color: var(--primary); font-weight: 700;">+3.790.000đ</span>
                                    </li>
                                    <li class="nava-dropdown-item" onclick="selectVariantDropdown(this, 'ram', 4190000, '16GB - 5600')" style="display: flex; justify-content: space-between; align-items: center; width: 100%; box-sizing: border-box;">
                                        <span>16GB - 5600</span>
                                        <span style="color: var(--primary); font-weight: 700;">+4.190.000đ</span>
                                    </li>
                                    <li class="nava-dropdown-item" onclick="selectVariantDropdown(this, 'ram', 6990000, '32GB - 4800')" style="display: flex; justify-content: space-between; align-items: center; width: 100%; box-sizing: border-box;">
                                        <span>32GB - 4800</span>
                                        <span style="color: var(--primary); font-weight: 700;">+6.990.000đ</span>
                                    </li>
                                </ul>
                            </div>
                        </div>
                        
                        <!-- SSD Selector -->
                        <div class="bs-option-col">
                            <span class="bs-option-label-v2" style="font-weight: 700; font-size: 0.85rem; color: var(--text-gray, #64748b); margin-bottom: 6px; display: block;">SSD NVMe</span>
                            <div class="nava-dropdown-wrapper" data-dropdown-type="ssd" style="position: relative; width: 100%;">
                                <div class="nava-dropdown-display" style="width: 100%; border: 1px solid var(--border-color); border-radius: 8px; padding: 12px 15px; padding-right: 40px; background: var(--bg-gray); cursor: default; display: flex; justify-content: space-between; align-items: center; box-sizing: border-box; position: relative;">
                                    <span class="nava-dropdown-selected" style="font-weight: 700; font-size: 0.9rem; color: var(--text-dark);">NO SSD</span>
                                    <span class="nava-dropdown-selected-price" style="font-weight: 700; font-size: 0.9rem; color: var(--primary); margin-left: auto; margin-right: 5px;">+0đ</span>
                                    <i class="ph-bold ph-caret-down nava-dropdown-arrow" style="color: var(--text-gray); transition: transform 0.2s; position: absolute; right: 15px; top: 50%; transform: translateY(-50%);"></i>
                                </div>
                                <ul class="nava-dropdown-list">
                                    <li class="nava-dropdown-item active" onclick="selectVariantDropdown(this, 'ssd', 0, 'NO SSD')" style="display: flex; justify-content: space-between; align-items: center; width: 100%; box-sizing: border-box;">
                                        <span>NO SSD</span>
                                        <span style="color: var(--primary); font-weight: 700;">+0đ</span>
                                    </li>
                                    <li class="nava-dropdown-item" onclick="selectVariantDropdown(this, 'ssd', 1190000, '256GB')" style="display: flex; justify-content: space-between; align-items: center; width: 100%; box-sizing: border-box;">
                                        <span>256GB</span>
                                        <span style="color: var(--primary); font-weight: 700;">+1.190.000đ</span>
                                    </li>
                                    <li class="nava-dropdown-item" onclick="selectVariantDropdown(this, 'ssd', 2290000, '500GB')" style="display: flex; justify-content: space-between; align-items: center; width: 100%; box-sizing: border-box;">
                                        <span>500GB</span>
                                        <span style="color: var(--primary); font-weight: 700;">+2.290.000đ</span>
                                    </li>
                                    <li class="nava-dropdown-item" onclick="selectVariantDropdown(this, 'ssd', 3990000, '1TB')" style="display: flex; justify-content: space-between; align-items: center; width: 100%; box-sizing: border-box;">
                                        <span>1TB</span>
                                        <span style="color: var(--primary); font-weight: 700;">+3.990.000đ</span>
                                    </li>
                                </ul>
                            </div>
                        </div>
                        
                        <!-- Qty Selector -->
                        <div class="bs-option-col bs-qty-col">
                            <span class="bs-option-label-v2" style="font-weight: 700; font-size: 0.85rem; color: var(--text-gray, #64748b); margin-bottom: 6px; display: block;"><span class="desktop-qty-label">Số lượng</span><span class="mobile-qty-label">SL</span></span>
                            <div class="qty-selector" style="display: inline-flex; align-items: center; border: 1px solid var(--border-color); border-radius: 8px; overflow: hidden; background: var(--bg-gray); height: 46px;">
                                <button type="button" class="qty-adjust" onclick="adjustQty(-1)" style="width: 36px; height: 100%; border: none; background: transparent; cursor: pointer; font-weight: bold; color: var(--text-dark); transition: 0.2s;" onmouseover="this.style.background='rgba(0,0,0,0.05)'" onmouseout="this.style.background='transparent'">-</button>
                                <input type="text" value="1" class="qty-val" id="qty-val-bs" readonly style="width: 40px; height: 100%; text-align: center; border: none; background: transparent; font-weight: 700; font-size: 0.95rem; color: var(--text-dark); outline: none;">
                                <button type="button" class="qty-adjust" onclick="adjustQty(1)" style="width: 36px; height: 100%; border: none; background: transparent; cursor: pointer; font-weight: bold; color: var(--text-dark); transition: 0.2s;" onmouseover="this.style.background='rgba(0,0,0,0.05)'" onmouseout="this.style.background='transparent'">+</button>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Actions row: Add to cart & Buy now -->
                    <div class="bs-actions-row" style="display: flex; gap: 15px; align-items: center; width: 100%; margin-top: 15px;">
                        <button type="button" class="btn-add-cart btn-add-cart-bs" onclick="triggerAddToCart(event)" style="flex: none !important; width: 60px; height: 50px; display: flex; align-items: center; justify-content: center;" title="Thêm vào giỏ">
                            <i class="ph ph-shopping-cart-simple" style="font-size: 1.4rem;"></i>
                        </button>
                        <button type="button" class="bs-buy-btn" onclick="triggerCheckout(event)" style="flex: 1; height: 50px; border-radius: 8px; border: none; background: linear-gradient(90deg, var(--primary), var(--secondary)); color: white; font-weight: 800; font-size: 1rem; cursor: pointer; text-transform: uppercase; transition: all 0.2s; box-shadow: 0 4px 15px rgba(0, 51, 102, 0.2);" onmouseover="this.style.transform='translateY(-1px)'; this.style.boxShadow='0 6px 20px rgba(0, 51, 102, 0.35)'" onmouseout="this.style.transform='none'; this.style.boxShadow='0 4px 15px rgba(0, 51, 102, 0.2)'">MUA NGAY</button>
                    </div>
                </div>
            </div>
            
            <script>
                function toggleDescription() {
                    const wrapper = document.getElementById('desc-wrapper');
                    const btn = document.getElementById('btn-show-desc');
                    if (wrapper.classList.contains('expanded')) {
                        wrapper.classList.remove('expanded');
                        btn.innerHTML = 'Xem thêm <i class="ph-bold ph-caret-down"></i>';
                        wrapper.scrollIntoView({ behavior: 'smooth' });
                    } else {
                        wrapper.classList.add('expanded');
                        btn.innerHTML = 'Thu gọn <i class="ph-bold ph-caret-up"></i>';
                    }
                }
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
                    
                    const container = document.getElementById('thumbnail-list');
                    if (container) {
                        const containerWidth = container.clientWidth;
                        const elementLeft = element.offsetLeft;
                        const elementWidth = element.clientWidth;
                        const targetScrollLeft = elementLeft - (containerWidth / 2) + (elementWidth / 2);
                        container.scrollTo({
                            left: targetScrollLeft,
                            behavior: 'smooth'
                        });
                    }
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
                let activeRamName = 'NO RAM';
                let activeSsdName = 'NO SSD';
                let warnedBarebone = false;
                let warnedBareboneCart = false;
                let currentPrice = basePrice;

                function animatePrice(elementId, startValue, endValue, duration = 400) {
                    const obj = document.getElementById(elementId);
                    if (!obj) return;
                    
                    const startTime = performance.now();
                    
                    function update(currentTime) {
                        const elapsedTime = currentTime - startTime;
                        if (elapsedTime >= duration) {
                            obj.innerHTML = endValue.toLocaleString('vi-VN') + 'đ';
                            return;
                        }
                        
                        // Ease out quad
                        const progress = elapsedTime / duration;
                        const easeProgress = progress * (2 - progress);
                        
                        const currentValue = Math.round(startValue + (endValue - startValue) * easeProgress);
                        obj.innerHTML = currentValue.toLocaleString('vi-VN') + 'đ';
                        
                        requestAnimationFrame(update);
                    }
                    
                    requestAnimationFrame(update);
                }
                
                // Bottom Sheet State
                let isBsOpen = false;
                
                window.openBottomSheet = function() {
                    if (window.innerWidth >= 992) {
                        return; // Don't show bottom-sheet modal on PC/desktop
                    }
                    const overlay = document.getElementById('nava-bs-overlay');
                    const bs = document.getElementById('nava-bottom-sheet');
                    const stickyBar = document.getElementById('sticky-cart-bar');
                    
                    if (overlay && bs) {
                        isBsOpen = true;
                        if (stickyBar) {
                            stickyBar.style.setProperty('transform', 'translateY(120%)', 'important');
                        }
                        overlay.style.display = 'block';
                        bs.style.display = 'flex';
                        void overlay.offsetWidth;
                        void bs.offsetWidth;
                        overlay.style.opacity = '1';
                        bs.classList.add('open');
                        document.body.style.overflow = 'hidden';
                        
                        // Automatically open/expand the dropdown lists on mobile bottom sheet
                        setTimeout(() => {
                            const bsDropdowns = bs.querySelectorAll('.nava-dropdown-wrapper, .nava-custom-select-wrapper, .custom-select-wrapper');
                            bsDropdowns.forEach(w => {
                                w.classList.add('active');
                            });
                        }, 100);

                        // Hide compare bar when bottom sheet is open
                        if (typeof updateCompareBar === 'function') {
                            updateCompareBar();
                        }
                    }
                };
                
                window.closeBottomSheet = function() {
                    const overlay = document.getElementById('nava-bs-overlay');
                    const bs = document.getElementById('nava-bottom-sheet');
                    
                    if (overlay && bs) {
                        isBsOpen = false;
                        overlay.style.opacity = '0';
                        bs.classList.remove('open');
                        setTimeout(() => {
                            overlay.style.display = 'none';
                            bs.style.display = 'none';
                            document.body.style.overflow = '';
                            toggleStickyBar();
                            
                            // Restore compare bar visibility
                            if (typeof updateCompareBar === 'function') {
                                updateCompareBar();
                            }
                        }, 300);
                    }
                };

                window.openReviewImage = function(src) {
                    let rLightbox = document.getElementById('review-lightbox');
                    if (!rLightbox) {
                        rLightbox = document.createElement('div');
                        rLightbox.id = 'review-lightbox';
                        rLightbox.innerHTML = `
                            <div style="position: fixed; inset: 0; background: rgba(0,0,0,0.85); z-index: 2147483647; display: flex; align-items: center; justify-content: center; backdrop-filter: blur(8px); opacity: 0; transition: opacity 0.25s;" onclick="this.parentNode.style.display='none'; document.body.style.overflow=''">
                                <button type="button" style="position: absolute; top: 20px; right: 20px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: white; width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; font-size: 1.5rem;"><i class="ph ph-x"></i></button>
                                <img id="review-lightbox-img" src="" style="max-width: 90%; max-height: 90vh; object-fit: contain; border-radius: 8px; border: 2px solid rgba(255,255,255,0.1);">
                            </div>
                        `;
                        document.body.appendChild(rLightbox);
                    }
                    rLightbox.querySelector('#review-lightbox-img').src = src;
                    rLightbox.style.display = 'block';
                    setTimeout(() => {
                        rLightbox.querySelector('div').style.opacity = '1';
                    }, 50);
                    document.body.style.overflow = 'hidden';
                };

                function selectVariantDropdown(element, type, price, name) {
                    // Sync all dropdowns of this type (main page and bottom sheet)
                    const wrappers = document.querySelectorAll(`.nava-dropdown-wrapper[data-dropdown-type="${type}"]`);
                    wrappers.forEach(wrapper => {
                        const displayEl = wrapper.querySelector('.nava-dropdown-selected');
                        if (displayEl) {
                            displayEl.innerText = name;
                        }
                        const displayPriceEl = wrapper.querySelector('.nava-dropdown-selected-price');
                        if (displayPriceEl) {
                            displayPriceEl.innerText = price > 0 ? '+' + price.toLocaleString('vi-VN') + 'đ' : '+0đ';
                        }
                        
                        const items = wrapper.querySelectorAll('.nava-dropdown-item');
                        items.forEach(item => {
                            const itemSpan = item.querySelector('span');
                            const itemName = itemSpan ? itemSpan.innerText : item.innerText;
                            if (itemName.trim() === name.trim()) {
                                item.classList.add('active');
                            } else {
                                item.classList.remove('active');
                            }
                        });
                        
                        // Close dropdown
                        wrapper.classList.remove('active');
                    });
                    
                    if (type === 'ram') { 
                        activeRamPrice = price; 
                        activeRamName = name; 
                    }
                    if (type === 'ssd') { 
                        activeSsdPrice = price; 
                        activeSsdName = name; 
                    }
                    warnedBarebone = false;
                    warnedBareboneCart = false;
                    
                    const total = basePrice + activeRamPrice + activeSsdPrice;
                    
                    if (total !== currentPrice) {
                        animatePrice('main-price', currentPrice, total, 400);
                        animatePrice('sticky-price', currentPrice, total, 400);
                        animatePrice('bs-price', currentPrice, total, 400);
                        currentPrice = total;
                    }
                    
                    const stickyTitle = document.querySelector('.sticky-title');
                    if(stickyTitle) {
                        let opts = [];
                        if(activeRamName && activeRamName !== 'NO RAM') opts.push(activeRamName);
                        if(activeSsdName && activeSsdName !== 'NO SSD') opts.push(activeSsdName);
                        let optString = opts.length > 0 ? ` - ${opts.join(', ')}` : '';
                        stickyTitle.innerHTML = 'ASUS NUC AI 350' + optString;
                    }

                    if (typeof checkRAMSSDPrompt === 'function') {
                        checkRAMSSDPrompt();
                    }
                }

                function checkRAMSSDPrompt() {
                    let hasRam = true;
                    let hasSsd = true;
                    
                    let isDefaultRam = (activeRamName === 'NO RAM' || activeRamName.toUpperCase().includes('TRỐNG') || activeRamName.toUpperCase().includes('0GB'));
                    let isDefaultSsd = (activeSsdName === 'NO SSD' || activeSsdName.toUpperCase().includes('TRỐNG') || activeSsdName.toUpperCase().includes('0GB'));
                    
                    if (isDefaultRam || isDefaultSsd) {
                        showNudgeBanner();
                    } else {
                        hideNudgeBanner();
                    }
                }
                
                function showNudgeBanner() {
                    let banner = document.getElementById('ram-ssd-nudge-banner');
                    let isAlreadyVisible = false;
                    if (banner && banner.style.opacity === '1') {
                        isAlreadyVisible = true;
                    }
                    
                    if (!banner) {
                        if (!document.getElementById('nudge-banner-style')) {
                            const style = document.createElement('style');
                            style.id = 'nudge-banner-style';
                            style.innerHTML = `
                                @keyframes nudge-shake {
                                    0%, 100% { transform: translateX(-50%) translateY(0); }
                                    15%, 45%, 75% { transform: translateX(-52%) translateY(-1px); }
                                    30%, 60%, 90% { transform: translateX(-48%) translateY(1px); }
                                }
                                .nudge-shake-active {
                                    animation: nudge-shake 0.7s ease-in-out 3;
                                }
                            `;
                            document.head.appendChild(style);
                        }
                        
                        banner = document.createElement('div');
                        banner.id = 'ram-ssd-nudge-banner';
                        banner.style.cssText = `
                            position: fixed; bottom: 85px; left: 50%; 
                            transform: translateX(-50%) translateY(120px); 
                            width: calc(100% - 32px); max-width: 480px; 
                            background: rgba(255, 255, 255, 0.95); 
                            backdrop-filter: blur(12px); 
                            border: 1.5px solid rgba(239, 68, 68, 0.35); 
                            border-radius: 16px; padding: 14px 20px; 
                            box-shadow: 0 10px 35px rgba(239, 68, 68, 0.15), 0 5px 15px rgba(0,0,0,0.08); 
                            z-index: 99999; display: flex; align-items: center; gap: 12px; 
                            transition: transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275), opacity 0.3s; 
                            opacity: 0; box-sizing: border-box; font-family: inherit;
                        `;
                        banner.innerHTML = `
                            <div style="width: 38px; height: 38px; border-radius: 50%; background: rgba(239, 68, 68, 0.1); color: #ef4444; display: flex; align-items: center; justify-content: center; flex-shrink: 0;"><i class="ph-fill ph-warning-octagon" style="font-size: 1.4rem;"></i></div>
                            <div style="flex: 1; text-align: left;">
                                <div style="font-size: 0.88rem; font-weight: 800; color: #ef4444; margin-bottom: 2px;">Chưa chọn cấu hình RAM & SSD</div>
                                <div style="font-size: 0.78rem; font-weight: 600; color: #64748b;">Vui lòng chọn cấu hình ở trên để nhận báo giá & mua hàng!</div>
                            </div>
                            <button id="nudge-banner-btn" style="background: var(--primary, #003366); border: none; border-radius: 8px; color: white; padding: 8px 14px; font-weight: 700; font-size: 0.78rem; cursor: pointer; white-space: nowrap; transition: 0.2s;">Chọn ngay</button>
                        `;
                        document.body.appendChild(banner);
                        
                        banner.querySelector('#nudge-banner-btn').addEventListener('click', function() {
                            const selectorBlock = document.querySelector('.product-control, [data-dropdown-type="ram"], .box-variant');
                            if (selectorBlock) {
                                selectorBlock.scrollIntoView({ behavior: 'smooth', block: 'center' });
                                const displays = document.querySelectorAll('.nava-dropdown-display, .swatch');
                                displays.forEach(d => {
                                    d.style.transition = 'all 0.3s';
                                    d.style.borderColor = '#ef4444';
                                    d.style.boxShadow = '0 0 10px rgba(239,68,68,0.2)';
                                    setTimeout(() => {
                                        d.style.borderColor = '';
                                        d.style.boxShadow = '';
                                    }, 1500);
                                });
                            }
                        });
                    }
                    
                    setTimeout(() => {
                        banner.style.transform = 'translateX(-50%) translateY(0)';
                        banner.style.opacity = '1';
                        if (!isAlreadyVisible) {
                            banner.classList.add('nudge-shake-active');
                            setTimeout(() => {
                                banner.classList.remove('nudge-shake-active');
                            }, 2200);
                        }
                    }, 100);
                }
                
                function hideNudgeBanner() {
                    const banner = document.getElementById('ram-ssd-nudge-banner');
                    if (banner) {
                        banner.style.transform = 'translateX(-50%) translateY(120px)';
                        banner.style.opacity = '0';
                    }
                }

                window.adjustQty = function(amount) {
                    const qtyInputMain = document.getElementById('qty-val-main');
                    const qtyInputBs = document.getElementById('qty-val-bs');
                    
                    let currentVal = 1;
                    if (qtyInputMain) {
                        currentVal = parseInt(qtyInputMain.value) || 1;
                    } else if (qtyInputBs) {
                        currentVal = parseInt(qtyInputBs.value) || 1;
                    }
                    
                    let newVal = currentVal + amount;
                    if (newVal < 1) newVal = 1;
                    
                    if (qtyInputMain) qtyInputMain.value = newVal;
                    if (qtyInputBs) qtyInputBs.value = newVal;
                };

                let isStickyBarTicking = false;
                let cachedStickyBar = null;
                let cachedWrappers = null;

                function toggleStickyBar(e) {
                    if (!isStickyBarTicking) {
                        window.requestAnimationFrame(() => {
                            if (!cachedStickyBar) {
                                cachedStickyBar = document.getElementById('sticky-cart-bar');
                            }
                            if (!cachedStickyBar) {
                                isStickyBarTicking = false;
                                return;
                            }
                            
                            const threshold = window.innerWidth <= 768 ? 200 : 600;
                            let scrollY = window.scrollY || document.documentElement.scrollTop || document.body.scrollTop || 0;
                            
                            if (scrollY === 0) {
                                if (!cachedWrappers) {
                                    cachedWrappers = document.querySelectorAll('.bodywrap, .wrapper, #wrapper, .page-body, main, #main, #nava-master-wrapper');
                                }
                                for (let i = 0; i < cachedWrappers.length; i++) {
                                    if (cachedWrappers[i].scrollTop > scrollY) {
                                        scrollY = cachedWrappers[i].scrollTop;
                                    }
                                }
                            }
                            
                            if (e && e.target && e.target.scrollTop > scrollY) {
                                if (e.target.clientHeight && e.target.clientHeight > window.innerHeight * 0.5) {
                                    scrollY = e.target.scrollTop;
                                }
                            }
                            
                            if (scrollY > threshold && !isBsOpen) {
                                cachedStickyBar.style.setProperty('transform', 'translateY(0)', 'important');
                                cachedStickyBar.style.setProperty('display', 'block', 'important');
                            } else {
                                cachedStickyBar.style.setProperty('transform', 'translateY(120%)', 'important');
                            }
                            isStickyBarTicking = false;
                        });
                        isStickyBarTicking = true;
                    }
                }

                function initProductPage() {
                    const scrollTarget = document.getElementById('nava-master-wrapper') || document.body;

                    const stickyBar = document.getElementById('sticky-cart-bar');
                    if (stickyBar) {
                        stickyBar.style.setProperty('z-index', '1000', 'important');
                        if (stickyBar.parentNode !== scrollTarget) {
                            scrollTarget.appendChild(stickyBar);
                        }
                    }
                    
                    const bsOverlay = document.getElementById('nava-bs-overlay');
                    const bsDrawer = document.getElementById('nava-bottom-sheet');
                    if (bsOverlay && bsOverlay.parentNode !== scrollTarget) {
                        scrollTarget.appendChild(bsOverlay);
                    }
                    if (bsDrawer && bsDrawer.parentNode !== scrollTarget) {
                        scrollTarget.appendChild(bsDrawer);
                    }
                    
                    toggleStickyBar(); // Check immediately on load
                    
                    // Call checkRAMSSDPrompt on load
                    setTimeout(checkRAMSSDPrompt, 100);
                    
                    document.querySelectorAll('.nava-dropdown-display').forEach(display => {
                        display.addEventListener('click', function(e) {
                            e.preventDefault();
                            e.stopPropagation();
                        });
                    });
                    
                    document.querySelectorAll('.nava-dropdown-wrapper').forEach(wrapper => {
                        wrapper.addEventListener('mouseenter', function() {
                            wrapper.classList.add('active');
                        });
                        wrapper.addEventListener('mouseleave', function() {
                            wrapper.classList.remove('active');
                        });
                    });

                    const triggerCartOpen = (e) => {
                        if (e) e.preventDefault();
                        const headerCartBtn = document.getElementById('header-cart-btn');
                        if (headerCartBtn) {
                            headerCartBtn.click();
                        }
                    };

                    const btnCartIcon = document.getElementById('btn-cart-icon');
                    if (btnCartIcon) {
                        btnCartIcon.addEventListener('click', triggerCartOpen);
                    }

                    document.querySelectorAll('.btn-add-cart-sticky').forEach(btn => {
                        btn.addEventListener('click', triggerCartOpen);
                    });

                    window.triggerAddToCart = (e) => {
if (e) e.preventDefault();

// 1. Check for contact price (if price is 0đ/Liên hệ, redirect directly)
const total = basePrice + activeRamPrice + activeSsdPrice;
if (total === 0) {
window.location.href = 'tel:0972178527';
return;
}

// 2. Check for configuration warning
let isDefaultRam = (activeRamName === 'NO RAM' || activeRamName.toUpperCase().includes('TRỐNG') || activeRamName.toUpperCase().includes('0GB'));
let isDefaultSsd = (activeSsdName === 'NO SSD' || activeSsdName.toUpperCase().includes('TRỐNG') || activeSsdName.toUpperCase().includes('0GB'));

if (isDefaultRam || isDefaultSsd) {
if (window.innerWidth >= 992) {
// On PC/desktop, scroll to options
const selectorBlock = document.querySelector('.product-control, [data-dropdown-type="ram"], .box-variant');
if (selectorBlock) {
selectorBlock.scrollIntoView({ behavior: 'smooth', block: 'center' });
const displays = document.querySelectorAll('.nava-dropdown-display, .swatch');
displays.forEach(d => {
d.style.transition = 'all 0.3s';
d.style.borderColor = '#ef4444';
d.style.boxShadow = '0 0 10px rgba(239,68,68,0.2)';
setTimeout(() => {
d.style.borderColor = '';
d.style.boxShadow = '';
}, 1500);
});
}
} else {
// On mobile, open bottom sheet
openBottomSheet();
const bs = document.getElementById('nava-bottom-sheet');
if (bs) {
bs.classList.remove('bs-shake-active');
void bs.offsetWidth; // Reflow
bs.classList.add('bs-shake-active');
}
}
return;
}

closeBottomSheet();
triggerCartOpen(e);
};

window.triggerCheckout = (e) => {
if (e) e.preventDefault();

// 1. Check for contact price (if price is 0đ/Liên hệ, redirect directly)
const total = basePrice + activeRamPrice + activeSsdPrice;
if (total === 0) {
window.location.href = 'tel:0972178527';
return;
}

// 2. Check for configuration warning
let isDefaultRam = (activeRamName === 'NO RAM' || activeRamName.toUpperCase().includes('TRỐNG') || activeRamName.toUpperCase().includes('0GB'));
let isDefaultSsd = (activeSsdName === 'NO SSD' || activeSsdName.toUpperCase().includes('TRỐNG') || activeSsdName.toUpperCase().includes('0GB'));

if (isDefaultRam || isDefaultSsd) {
if (window.innerWidth >= 992) {
// On PC/desktop, scroll to options
const selectorBlock = document.querySelector('.product-control, [data-dropdown-type="ram"], .box-variant');
if (selectorBlock) {
selectorBlock.scrollIntoView({ behavior: 'smooth', block: 'center' });
const displays = document.querySelectorAll('.nava-dropdown-display, .swatch');
displays.forEach(d => {
d.style.transition = 'all 0.3s';
d.style.borderColor = '#ef4444';
d.style.boxShadow = '0 0 10px rgba(239,68,68,0.2)';
setTimeout(() => {
d.style.borderColor = '';
d.style.boxShadow = '';
}, 1500);
});
}
} else {
// On mobile, open bottom sheet
openBottomSheet();
const bs = document.getElementById('nava-bottom-sheet');
if (bs) {
bs.classList.remove('bs-shake-active');
void bs.offsetWidth; // Reflow
bs.classList.add('bs-shake-active');
}
}
return;
}

window.location.href = 'demo_checkout.html';
};

                    const btnBuyNowMain = document.getElementById('btn-buy-now-main');
                    if (btnBuyNowMain) {
                        btnBuyNowMain.addEventListener('click', triggerCheckout);
                    }

                    document.querySelectorAll('.btn-buy-now-sticky').forEach(btn => {
                        btn.addEventListener('click', triggerCheckout);
                    });
                    
                    document.addEventListener('click', function() {
                        document.querySelectorAll('.nava-dropdown-wrapper').forEach(w => w.classList.remove('active'));
                    });

                    const ratingBtn = document.getElementById('rating-scroll-btn');
                    if (ratingBtn) {
                        ratingBtn.addEventListener('click', function(e) {
                            e.preventDefault();
                            const dest = document.getElementById('danh-gia-shopee');
                            if (dest) {
                                dest.scrollIntoView({ behavior: 'smooth', block: 'start' });
                            }
                        });
                    }

                    const scrollContainer = document.getElementById('nava-master-wrapper') || window;
                    scrollContainer.addEventListener('scroll', toggleStickyBar, { passive: true });
                    window.addEventListener('scroll', toggleStickyBar, true);
                }

                if (document.readyState === 'loading') {
                    document.addEventListener('DOMContentLoaded', initProductPage);
                } else {
                    initProductPage();
                }
                
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
                
                window.openLightbox = function(e) {
                    if (e && e.stopPropagation) e.stopPropagation();
                    let lightbox = document.getElementById('nava-lightbox');
                    if (!lightbox) {
                        lightbox = document.createElement('div');
                        lightbox.id = 'nava-lightbox';
                        lightbox.innerHTML = `
                            <div style="position: fixed; inset: 0; background: rgba(0,0,0,0.9); z-index: 2147483647; display: flex; align-items: center; justify-content: center; backdrop-filter: blur(8px); opacity: 0; transition: opacity 0.3s;">
                                <button type="button" onclick="window.closeLightbox()" style="position: absolute; top: 20px; right: 20px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: white; width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; font-size: 1.5rem; transition: 0.2s; z-index: 2;" onmouseover="this.style.background='rgba(255,255,255,0.2)'" onmouseout="this.style.background='rgba(255,255,255,0.1)'"><i class="ph ph-x"></i></button>
                                <button type="button" onclick="if(event) event.stopPropagation(); window.navigateLightbox(-1)" style="position: absolute; left: 20px; top: 50%; transform: translateY(-50%); background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: white; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; font-size: 1.5rem; transition: 0.2s; z-index: 2;" onmouseover="this.style.background='rgba(255,255,255,0.2)'" onmouseout="this.style.background='rgba(255,255,255,0.1)'"><i class="ph-bold ph-caret-left"></i></button>
                                <img id="lightbox-img" src="" style="max-width: 90%; max-height: 90vh; object-fit: contain; transition: 0.3s; transform: scale(0.95); opacity: 0; position: relative; z-index: 1;" onclick="if(event) event.stopPropagation();">
                                <button type="button" onclick="if(event) event.stopPropagation(); window.navigateLightbox(1)" style="position: absolute; right: 20px; top: 50%; transform: translateY(-50%); background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: white; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; font-size: 1.5rem; transition: 0.2s; z-index: 2;" onmouseover="this.style.background='rgba(255,255,255,0.2)'" onmouseout="this.style.background='rgba(255,255,255,0.1)'"><i class="ph-bold ph-caret-right"></i></button>
                                <div id="lightbox-counter" style="position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); color: rgba(255,255,255,0.6); font-weight: 600; letter-spacing: 2px; z-index: 2;"></div>
                            </div>
                        `;
                        lightbox.querySelector('div').onclick = window.closeLightbox; // close when clicking background
                        document.body.appendChild(lightbox);
                    }
                    
                    const mainObj = document.getElementById('main-product-img');
                    if (mainObj) {
                        const currentSrc = mainObj.src || '';
                        currentLightboxIndex = galleryImages.findIndex(src => currentSrc.includes(src.split('?')[0]));
                        if(currentLightboxIndex === -1) currentLightboxIndex = 0;
                    }
                    
                    lightbox.style.display = 'block';
                    const lightboxDiv = lightbox.querySelector('div');
                    if (lightboxDiv) {
                        void lightboxDiv.offsetWidth; // trigger reflow
                        lightboxDiv.style.opacity = '1';
                    }
                    
                    window.updateLightboxImage();
                    document.body.style.overflow = 'hidden';
                }
                
                window.closeLightbox = function() {
                    const lightbox = document.getElementById('nava-lightbox');
                    if (!lightbox) return;
                    const lightboxDiv = lightbox.querySelector('div');
                    if (lightboxDiv) lightboxDiv.style.opacity = '0';
                    setTimeout(() => {
                        lightbox.style.display = 'none';
                        document.body.style.overflow = '';
                    }, 300);
                }
                
                window.navigateLightbox = function(dir) {
                    currentLightboxIndex += dir;
                    if(currentLightboxIndex < 0) currentLightboxIndex = galleryImages.length - 1;
                    if(currentLightboxIndex >= galleryImages.length) currentLightboxIndex = 0;
                    window.updateLightboxImage();
                }
                
                window.updateLightboxImage = function() {
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
    full_html = clean_liquid_tags(header_part + product_html + local_footer_part, 'product')
    
    # Inject sticky compare bar HTML from post_build.py
    try:
        with open("post_build.py", "r", encoding="utf-8") as f:
            pb_content = f.read()
            start_pos = pb_content.find('sticky_html = """')
            end_idx = pb_content.find('"""\n\nfile_path')
            if start_pos != -1 and end_idx != -1:
                start_idx = start_pos + len('sticky_html = """')
                sticky_html = pb_content[start_idx:end_idx]
                if "<!-- Sticky Compare Bar -->" not in full_html:
                    if "</body>" in full_html:
                        full_html = full_html.replace("</body>", sticky_html + "\n</body>")
                    else:
                        full_html += sticky_html
    except Exception as e:
        print("Failed to inject sticky compare bar:", e)

    full_html = inject_seo_metadata(
        full_html,
        title="ASUS NUC AI 350 (ExpertCenter PN54) Mini PC Ryzen AI 7 350 - Nava Store",
        description="ASUS NUC AI 350 (ExpertCenter PN54) Mini PC Ryzen AI 7 350 chính hãng, hiệu năng AI vượt trội với AMD Ryzen AI, card Radeon 860M, bảo hành 36 tháng.",
        keywords="ASUS NUC AI 350, ExpertCenter PN54, Mini PC Ryzen AI 7 350, Nava Store"
    )
    with open(os.path.join(base_dir, "demo_product.html"), "w", encoding="utf-8") as f:
        f.write(full_html)

def build_auth_pages(base_dir):
    # CSS & Boilerplate for Glassmorphism Fullscreen Auth Pages
    auth_css = """
        <style>
            :root {
                --primary: #003366;
                --secondary: #004c99;
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
                scrollbar-width: none;
            }
            .glass-card::-webkit-scrollbar {
                display: none;
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
                font-weight: 850;
                color: var(--text-dark);
                margin: 0 0 5px 0;
                letter-spacing: -0.5px;
            }
            .auth-desc {
                color: var(--text-gray);
                font-size: 0.92rem;
                margin: 0 0 25px 0;
            }
            .form-group-nava {
                position: relative;
                margin-bottom: 18px;
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
                padding: 14px 16px 14px 44px;
                border: 1px solid var(--border-color);
                border-radius: var(--radius-md);
                background: var(--bg-gray);
                font-family: inherit;
                font-size: 0.95rem;
                color: var(--text-dark);
                transition: all 0.3s;
                box-sizing: border-box;
                outline: none;
            }
            .input-nava:focus {
                border-color: var(--primary);
                background: white;
                box-shadow: 0 0 0 4px rgba(0, 51, 102, 0.1);
            }
            .btn-nava {
                width: 100%;
                padding: 14px;
                border-radius: var(--radius-md);
                font-weight: 700;
                font-size: 1rem;
                cursor: pointer;
                transition: all 0.3s;
                box-sizing: border-box;
                border: 1px solid var(--border-color);
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
            }
            .btn-primary-nava {
                background: linear-gradient(90deg, var(--primary), var(--secondary));
                color: white;
                border: none;
                box-shadow: 0 10px 20px rgba(0, 51, 102, 0.2);
            }
            .btn-primary-nava:hover {
                transform: translateY(-2px);
                box-shadow: 0 15px 25px rgba(0, 51, 102, 0.3);
            }
            .link-nava {
                color: var(--primary);
                font-weight: 700;
                text-decoration: none;
                font-size: 0.95rem;
                transition: color 0.2s;
            }
            .link-nava:hover {
                color: var(--secondary);
                text-decoration: underline;
            }
            .social-divider {
                display: flex;
                align-items: center;
                text-align: center;
                margin: 25px 0 20px;
                color: var(--text-gray);
                font-size: 0.75rem;
                font-weight: 700;
                letter-spacing: 1px;
            }
            .social-divider::before,
            .social-divider::after {
                content: '';
                flex: 1;
                border-bottom: 1px solid var(--border-color);
            }
            .social-divider::before { margin-right: 10px; }
            .social-divider::after { margin-left: 10px; }
            
            .social-login-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 12px;
            }
            .btn-social {
                background: white;
                color: var(--text-dark);
                font-size: 0.95rem;
                padding: 10px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
                transition: all 0.2s;
            }
            .btn-social:hover {
                background: var(--bg-gray);
                border-color: #cbd5e1;
                box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
            }
            @media (max-width: 480px) {
                .glass-card { padding: 25px 20px !important; border-radius: var(--radius-md) !important; }
                .auth-title { font-size: 1.5rem !important; }
                .input-nava { padding: 12px 14px 12px 40px !important; font-size: 0.9rem !important; }
                .btn-nava { padding: 12px !important; font-size: 0.95rem !important; }
                .btn-social { padding: 8px !important; font-size: 0.85rem !important; }
                .social-divider { margin: 20px 0 15px !important; }
            }
        </style>
    """

    header_wrapper = f"""<!DOCTYPE html>
    <html lang="vi">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Tài Khoản - Nava Store</title>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
            <script src="https://unpkg.com/@phosphor-icons/web"></script>
            {auth_css}
        </head>
        <body>
    """
    
    footer_wrapper = """
        </body>
    </html>
    """

    # 1. Login HTML (with Recovery Form built-in)
    login_html = header_wrapper + """
        <div class="auth-page-wrapper" id="login-container">
            <!-- Normal Login Card -->
            <div class="glass-card normal-login-box">
                <a href="demo_collection.html" class="link-nava" style="position: absolute; top: 25px; left: 25px; display: inline-flex; align-items: center; gap: 5px; font-size: 0.85rem;"><i class="ph-bold ph-arrow-left"></i> Quay lại</a>
                <div style="text-align: center; margin-top: 10px;">
                    <img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/logo.png?1775454528082" alt="Nava Store" style="height: 45px; margin-bottom: 15px;">
                    <h1 class="auth-title">Đăng Nhập</h1>
                    <p class="auth-desc">Chào mừng bạn quay lại với Nava Store</p>
                </div>
                
                <form method="post" action="/account/login" id="customer_login" accept-charset="UTF-8">
                    <input name="FormType" type="hidden" value="customer_login"/>
                    <input name="utf8" type="hidden" value="true"/>
                    
                    <div class="form-group-nava">
                        <i class="ph-bold ph-envelope"></i>
                        <input type="email" placeholder="Nhập địa chỉ Email" class="input-nava" pattern="[a-z0-9._%%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$" name="email" id="customer_email" required>
                    </div>
                    
                    <div class="form-group-nava" style="position: relative;">
                        <i class="ph-bold ph-lock"></i>
                        <input type="password" placeholder="Mật khẩu" class="input-nava" name="password" id="customer_password" required style="padding-right: 40px;">
                        <i class="ph ph-eye-slash" style="position: absolute; right: 15px; left: auto; top: 50%; transform: translateY(-50%); cursor: pointer; color: var(--text-gray); font-size: 1.1rem; z-index: 5;" onclick="togglePasswordVisibility('customer_password', this)"></i>
                    </div>
                    
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
                        <a href="#" onclick="toggleRecover(); return false;" class="link-nava" style="font-size: 0.88rem; font-weight: 500;">Quên mật khẩu?</a>
                    </div>
                    
                    <button type="submit" class="btn-nava btn-primary-nava" style="margin-top: 5px;">Đăng Nhập</button>
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
                
                <p style="text-align: center; margin-top: 25px; color: var(--text-gray); font-size: 0.95rem;">
                    Chưa có tài khoản? <a href="demo_register.html" class="link-nava">Đăng ký ngay</a>
                </p>
            </div>
            
            <!-- Recovery Card -->
            <style>
                .recover-login-box { display: none; }
                .show-recover .normal-login-box { display: none; }
                .show-recover .recover-login-box { display: block; }
            </style>
            
            <div class="glass-card recover-login-box">
                <div style="text-align: center;">
                    <img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/logo.png?1775454528082" alt="Nava Store" style="height: 45px; margin-bottom: 15px;">
                    <h1 class="auth-title">Khôi Phục Mật Khẩu</h1>
                    <p class="auth-desc">Nhập email của bạn để nhận liên kết khôi phục</p>
                </div>
                
                <form method="post" action="/account/recover" id="recover_customer_password" accept-charset="UTF-8">
                    <input name="FormType" type="hidden" value="recover_customer_password"/>
                    <input name="utf8" type="hidden" value="true"/>
                    
                    <div class="form-group-nava">
                        <i class="ph-bold ph-envelope"></i>
                        <input type="email" class="input-nava" placeholder="Nhập Email của bạn" pattern="[a-z0-9._%%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$" name="email" id="customer_email1" required>
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
            
            function togglePasswordVisibility(inputId, icon) {
                const input = document.getElementById(inputId);
                if (!input) return;
                if (input.type === 'password') {
                    input.type = 'text';
                    icon.className = 'ph ph-eye';
                } else {
                    input.type = 'password';
                    icon.className = 'ph ph-eye-slash';
                }
            }
        </script>
    """ + footer_wrapper
    
    with open(os.path.join(base_dir, "demo_login.html"), "w", encoding="utf-8") as f:
        f.write(login_html)

    # 2. Register HTML
    register_html = header_wrapper + """
        <div class="auth-page-wrapper" id="register-container">
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
                        <input type="tel" placeholder="Số điện thoại" class="input-nava" pattern="\\d+" name="Phone" required>
                    </div>
                    
                    <div class="form-group-nava">
                        <i class="ph-bold ph-envelope"></i>
                        <input type="email" placeholder="E-mail" class="input-nava" pattern="[a-z0-9._%%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$" name="email" required>
                    </div>
                    
                    <div class="form-group-nava" style="position: relative;">
                        <i class="ph-bold ph-lock"></i>
                        <input type="password" placeholder="Mật khẩu" class="input-nava" name="password" id="register_password" required style="padding-right: 40px;">
                        <i class="ph ph-eye-slash" style="position: absolute; right: 15px; left: auto; top: 50%; transform: translateY(-50%); cursor: pointer; color: var(--text-gray); font-size: 1.1rem; z-index: 5;" onclick="togglePasswordVisibility('register_password', this)"></i>
                    </div>
                    
                    <button type="submit" class="btn-nava btn-primary-nava" style="margin-top: 5px;">Đăng Ký Tài Khoản</button>
                    
                    <p style="text-align: center; margin-top: 15px; color: var(--text-gray); font-size: 0.8rem; line-height: 1.4;">
                        Bằng việc đăng ký, bạn đồng ý với <a href="demo_policy.html#terms" class="link-nava" style="font-size: 0.8rem;">Điều khoản dịch vụ</a> và <a href="demo_policy.html#privacy" class="link-nava" style="font-size: 0.8rem;">Chính sách bảo mật</a> của Nava Store
                    </p>
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
        
        <script>
            function togglePasswordVisibility(inputId, icon) {
                const input = document.getElementById(inputId);
                if (!input) return;
                if (input.type === 'password') {
                    input.type = 'text';
                    icon.className = 'ph ph-eye';
                } else {
                    input.type = 'password';
                    icon.className = 'ph ph-eye-slash';
                }
            }
        </script>
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
            .compare-page { padding: 20px 15px; max-width: 1200px; margin: 10px auto; }
            .compare-hero { text-align: center; margin-bottom: 40px; }
            .compare-hero h1 { font-size: 2.5rem; font-weight: 800; color: var(--text-dark); margin-bottom: 10px; background: linear-gradient(135deg, var(--primary), var(--secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
            .compare-hero p { color: var(--text-gray); font-size: 1.1rem; }
            
            .compare-grid-scroll-wrapper { width: 100%; }
            .compare-grid { display: grid; grid-template-columns: 250px 1fr 1fr 1fr; background: var(--bg-white); border-radius: var(--radius-lg); overflow: hidden; box-shadow: var(--shadow-sm); border: 1px solid var(--border-color); }
            
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
                .compare-grid-scroll-wrapper {
                    overflow-x: auto;
                    width: 100%;
                    -webkit-overflow-scrolling: touch;
                    scrollbar-width: none;
                    border-radius: var(--radius-lg);
                    border: 1px solid var(--border-color);
                }
                .compare-grid-scroll-wrapper::-webkit-scrollbar {
                    display: none;
                }
                .compare-grid {
                    grid-template-columns: 120px 180px 180px 180px !important;
                    width: max-content;
                    border: none !important;
                    border-radius: 0 !important;
                }
                .compare-label { font-size: 0.75rem; padding: 10px; }
                .compare-cell { font-size: 0.8rem; padding: 10px; }
                .compare-prod-img { width: 80px; height: 80px; }
                .compare-prod-title { font-size: 0.9rem !important; }
                .compare-prod-price { font-size: 1.05rem !important; }
                .col-3-compare { display: flex !important; }
            }

            /* Dark Mode Styling Overrides */
            [data-theme="dark"] .compare-grid {
                background: #1e293b;
                border-color: #334155;
            }
            [data-theme="dark"] .compare-cell-header {
                background: #0f172a !important;
                border-color: #334155 !important;
            }
            [data-theme="dark"] .compare-cell-header.empty {
                background: #1e293b !important;
                border-color: #334155 !important;
            }
            [data-theme="dark"] .compare-cell {
                border-color: #334155 !important;
                color: #e2e8f0 !important;
            }
            [data-theme="dark"] .compare-label {
                background: #0f172a !important;
                color: #94a3b8 !important;
            }
            [data-theme="dark"] .highlight-cell {
                background: rgba(16, 185, 129, 0.15) !important;
                color: #34d399 !important;
            }
            [data-theme="dark"] .compare-row:hover .compare-cell {
                background: rgba(255, 255, 255, 0.02) !important;
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
            </div>
            
            <div class="compare-grid-scroll-wrapper">
            <div class="compare-grid">
                <!-- Header -->
                <div class="compare-row-header">
                    <div class="compare-cell-header empty">
                        <button class="btn-pill" style="border: 2px dashed var(--border-color); background: transparent; color: var(--text-gray); border-radius: var(--radius-md); padding: 10px 15px; display: flex; align-items: center; gap: 5px; font-weight: 600; cursor: pointer;"><i class="ph-bold ph-plus"></i> Thêm SP</button>
                    </div>
                    <div class="compare-cell-header">
                        <button class="remove-btn" title="Xóa khỏi so sánh"><i class="ph-bold ph-x"></i></button>
                        <img src="//bizweb.dktcdn.net/thumb/large/100/543/817/products/mini-pc-asus-nuc-ai-350-pn54-ryzen-ai-7-350-gaming.jpg?v=1763971973973" alt="ASUS NUC" class="compare-prod-img">
                        <div class="compare-prod-title">ASUS NUC AI 350 (PN54)</div>
                        <div class="compare-prod-price">12.390.000đ</div>
                        <button class="btn-pill" style="width: 100%; border-radius: var(--radius-md); padding: 12px; font-weight: bold; background: rgba(14, 165, 233, 0.1); color: var(--primary); border: 2px solid var(--primary); cursor: pointer;">Mua ngay</button>
                    </div>
                    <div class="compare-cell-header">
                        <button class="remove-btn" title="Xóa khỏi so sánh"><i class="ph-bold ph-x"></i></button>
                        <img src="//bizweb.dktcdn.net/thumb/large/100/543/817/products/mini-pc-minisforum-um890-pro-ai-r9-8945hs-gaming-do-hoa.jpg?v=1761015394420" alt="UM890 PRO" class="compare-prod-img">
                        <div class="compare-prod-title">MINISFORUM UM890 Pro</div>
                        <div class="compare-prod-price">14.990.000đ</div>
                        <button class="btn-pill" style="width: 100%; border-radius: var(--radius-md); padding: 12px; font-weight: bold; background: rgba(14, 165, 233, 0.1); color: var(--primary); border: 2px solid var(--primary); cursor: pointer;">Mua ngay</button>
                    </div>
                    <div class="compare-cell-header col-3-compare">
                        <button class="remove-btn" title="Xóa khỏi so sánh"><i class="ph-bold ph-x"></i></button>
                        <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_1.png" alt="Beelink SER8" class="compare-prod-img">
                        <div class="compare-prod-title">BEELINK SER8 AI</div>
                        <div class="compare-prod-price">15.490.000đ</div>
                        <button class="btn-pill" style="width: 100%; border-radius: var(--radius-md); padding: 12px; font-weight: bold; background: rgba(14, 165, 233, 0.1); color: var(--primary); border: 2px solid var(--primary); cursor: pointer;">Mua ngay</button>
                    </div>
                </div>
                
                <!-- Specs -->
                <div class="compare-row">
                    <div class="compare-cell compare-label">Thương hiệu</div>
                    <div class="compare-cell">Asus</div>
                    <div class="compare-cell">Minisforum</div>
                    <div class="compare-cell col-3-compare">Beelink</div>
                </div>
                
                <div class="compare-row">
                    <div class="compare-cell compare-label">Model</div>
                    <div class="compare-cell">NUC AI 350 (PN54)</div>
                    <div class="compare-cell">UM890 Pro</div>
                    <div class="compare-cell col-3-compare">SER8 AI</div>
                </div>
                
                <div class="compare-row">
                    <div class="compare-cell compare-label">Tình trạng</div>
                    <div class="compare-cell">Mới 100%</div>
                    <div class="compare-cell">Mới 100%</div>
                    <div class="compare-cell col-3-compare">Mới 100%</div>
                </div>
                
                <div class="compare-row">
                    <div class="compare-cell compare-label">Kích thước</div>
                    <div class="compare-cell highlight-cell">130x130x34mm (Cực mỏng)</div>
                    <div class="compare-cell">130x127x60mm</div>
                    <div class="compare-cell col-3-compare">135x135x48mm</div>
                </div>
                
                <div class="compare-row">
                    <div class="compare-cell compare-label">Vi xử lý (CPU)</div>
                    <div class="compare-cell">AMD Ryzen AI 7 350 (8C/16T, max 5.0Ghz)</div>
                    <div class="compare-cell highlight-cell">AMD Ryzen 9 8945HS (8C/16T, max 5.2Ghz)</div>
                    <div class="compare-cell col-3-compare">AMD Ryzen 7 8845HS (8C/16T, max 5.1Ghz)</div>
                </div>
                
                <div class="compare-row">
                    <div class="compare-cell compare-label">CPU Mark (Hiệu năng)</div>
                    <div class="compare-cell highlight-cell">~30.000 điểm</div>
                    <div class="compare-cell">~29.500 điểm</div>
                    <div class="compare-cell col-3-compare">~29.000 điểm</div>
                </div>
                
                <div class="compare-row">
                    <div class="compare-cell compare-label">Đồ họa (GPU)</div>
                    <div class="compare-cell highlight-cell">AMD Radeon™ 860M</div>
                    <div class="compare-cell">AMD Radeon™ 780M</div>
                    <div class="compare-cell col-3-compare">AMD Radeon™ 780M</div>
                </div>
 
                <div class="compare-row">
                    <div class="compare-cell compare-label">G3D Mark (Đồ họa)</div>
                    <div class="compare-cell highlight-cell">~8.500 điểm</div>
                    <div class="compare-cell">~7.200 điểm</div>
                    <div class="compare-cell col-3-compare">~7.200 điểm</div>
                </div>
 
                <div class="compare-row">
                    <div class="compare-cell compare-label">Xử lý AI (NPU)</div>
                    <div class="compare-cell highlight-cell">Lên đến 50 TOPS NPU (Tổng 66 TOPS)</div>
                    <div class="compare-cell">Lên đến 16 TOPS NPU (Tổng 39 TOPS)</div>
                    <div class="compare-cell col-3-compare">Lên đến 16 TOPS NPU (Tổng 38 TOPS)</div>
                </div>
 
                <div class="compare-row">
                    <div class="compare-cell compare-label">Hỗ trợ RAM</div>
                    <div class="compare-cell highlight-cell">2x DDR5 5600 tối đa 128GB</div>
                    <div class="compare-cell">2x DDR5 5600 tối đa 96GB</div>
                    <div class="compare-cell col-3-compare">2x DDR5 5600 tối đa 64GB</div>
                </div>
 
                <div class="compare-row">
                    <div class="compare-cell compare-label">Lưu trữ (SSD)</div>
                    <div class="compare-cell">2x M.2 2280 NVMe PCIe 4.0</div>
                    <div class="compare-cell">2x M.2 2280 NVMe PCIe 4.0</div>
                    <div class="compare-cell col-3-compare">2x M.2 2280 NVMe PCIe 4.0</div>
                </div>
 
                <div class="compare-row">
                    <div class="compare-cell compare-label">Kết nối không dây</div>
                    <div class="compare-cell highlight-cell">Wi-Fi 6E (Gig+) 2x2 + Bluetooth® 5.4</div>
                    <div class="compare-cell">Wi-Fi 6E + Bluetooth® 5.3</div>
                    <div class="compare-cell col-3-compare">Wi-Fi 6 + Bluetooth® 5.2</div>
                </div>
 
                <div class="compare-row">
                    <div class="compare-cell compare-label">Cổng kết nối (IO)</div>
                    <div class="compare-cell">1x USB4, 1x USB 3.2 Gen2 A, 1x USB 2.0, 1x HDMI 2.1, 2x DP 1.4, 1x 2.5G LAN</div>
                    <div class="compare-cell highlight-cell">2x USB4, 4x USB 3.2 Gen2 A, 1x HDMI 2.1, 1x DP 1.4, 2x 2.5G LAN, 1x OCuLink</div>
                    <div class="compare-cell col-3-compare">1x USB4, 3x USB 3.2, 1x Type-C, 1x HDMI, 1x DP, 1x 2.5G LAN</div>
                </div>
 
                <div class="compare-row">
                    <div class="compare-cell compare-label">Tính năng đặc biệt</div>
                    <div class="compare-cell">Vân tay, phím Copilot+, hỗ trợ Copilot+ PC</div>
                    <div class="compare-cell highlight-cell">Cổng OCuLink chuyên dụng gắn eGPU, tản nhiệt kim loại lỏng</div>
                    <div class="compare-cell col-3-compare">Thân máy nhôm nguyên khối, tản nhiệt buồng hơi</div>
                </div>
 
                <div class="compare-row">
                    <div class="compare-cell compare-label">Hệ điều hành</div>
                    <div class="compare-cell highlight-cell">Win 11 Pro + Office 2021 bản quyền</div>
                    <div class="compare-cell">Win 11 Pro bản quyền</div>
                    <div class="compare-cell col-3-compare">Win 11 Pro bản quyền</div>
                </div>
 
                <div class="compare-row">
                    <div class="compare-cell compare-label">Nguồn cấp điện</div>
                    <div class="compare-cell">Adapter DC 120W</div>
                    <div class="compare-cell highlight-cell">Adapter GaN 120W (Cực kỳ nhỏ gọn)</div>
                    <div class="compare-cell col-3-compare">Adapter DC 120W</div>
                </div>
 
                <div class="compare-row">
                    <div class="compare-cell compare-label">Bảo hành</div>
                    <div class="compare-cell highlight-cell"><i class="ph-fill ph-shield-check" style="margin-right: 5px;"></i> 36 tháng chính hãng ASUS Việt Nam</div>
                    <div class="compare-cell">12 tháng cửa hàng (hỗ trợ gửi hãng 6 tháng đầu)</div>
                    <div class="compare-cell col-3-compare">12 tháng cửa hàng</div>
                </div>
            </div>
            </div>
            
            <!-- Recently Viewed Section -->
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@8/swiper-bundle.min.css" />
            <script src="https://cdn.jsdelivr.net/npm/swiper@8/swiper-bundle.min.js"></script>
            <div class="template-product mt-5" style="width: 100%; margin-top: 50px;">
                <div class="box_product_1 rounded-10 bg-white py-3 px-2 p-lg-3" style="border: 1px solid var(--border-color); border-radius: var(--radius-lg); padding: 25px; box-shadow: var(--shadow-sm);">
                    <div class="t1 align-items-center d-flex justify-content-between mb-3">
                        <h3 class="special-content_title font-weight-bold position-relative m-0" style="font-size: 1.3rem; font-weight: 800; color: var(--text-dark); margin: 0; display: flex; align-items: center; gap: 10px;">
                            <i class="ph-fill ph-clock-counter-clockwise" style="color: var(--primary); font-size: 1.5rem;"></i>
                            <span class="position-relative">Sản phẩm đã xem</span>
                        </h3>
                    </div>
                    <div class="swiper js-recent-slider p-2 pb-3 pb-lg-2" style="position: relative; overflow: hidden; list-style: none; padding: 0; z-index: 1;">
                        <div class="swiper-wrapper js-recent-container" id="recent-products-wrapper">
                            <!-- Dynamic cards -->
                        </div>
                        <!-- Navigation -->
                        <div class="swiper-button-prev recent-prev" style="color: var(--primary); width: 35px; height: 35px; background: white; border-radius: 50%; box-shadow: 0 4px 10px rgba(0,0,0,0.1); border: 1px solid var(--border-color); --swiper-navigation-size: 14px;"></div>
                        <div class="swiper-button-next recent-next" style="color: var(--primary); width: 35px; height: 35px; background: white; border-radius: 50%; box-shadow: 0 4px 10px rgba(0,0,0,0.1); border: 1px solid var(--border-color); --swiper-navigation-size: 14px;"></div>
                    </div>
                </div>
            </div>
            
            <script>
                document.addEventListener('DOMContentLoaded', function() {
                    const container = document.getElementById('recent-products-wrapper');
                    if (container) {
                        let items = [];
                        try {
                            items = JSON.parse(localStorage.getItem('mewRecent')) || [];
                        } catch(e) {}
                        
                        if (items.length === 0) {
                            items = [
                                {
                                    name: 'ASUS NUC AI 350 (PN54)',
                                    img: '//bizweb.dktcdn.net/thumb/large/100/543/817/products/mini-pc-asus-nuc-ai-350-pn54-ryzen-ai-7-350-gaming.jpg?v=1763971973973',
                                    price: '12.390.000đ',
                                    url: 'demo_product.html'
                                },
                                {
                                    name: 'MINISFORUM UM890 Pro',
                                    img: '//bizweb.dktcdn.net/thumb/large/100/543/817/products/mini-pc-minisforum-um890-pro-ai-r9-8945hs-gaming-do-hoa.jpg?v=1761015394420',
                                    price: '14.990.000đ',
                                    url: 'demo_product.html'
                                },
                                {
                                    name: 'GMKTEC NucBox K6 (Ryzen 7 7840HS)',
                                    img: 'https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_1.png',
                                    price: '14.200.000đ',
                                    url: 'demo_product.html'
                                }
                            ];
                        }
                        
                        let html = '';
                        items.forEach(item => {
                            const name = item.name || item.title || item;
                            const img = item.img || item.image || '//bizweb.dktcdn.net/thumb/large/100/543/817/products/mini-pc-asus-nuc-ai-350-pn54-ryzen-ai-7-350-gaming.jpg?v=1763971973973';
                            const price = item.price || 'Liên hệ';
                            const url = item.url || 'demo_product.html';
                            
                            html += `
                                <div class="swiper-slide" style="height: auto;">
                                    <div class="product-card" style="border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 15px; background: white; text-align: center; height: 100%; display: flex; flex-direction: column; justify-content: space-between; transition: 0.3s; box-sizing: border-box;" onmouseover="this.style.borderColor='var(--primary)'; this.style.boxShadow='0 8px 20px rgba(0,0,0,0.05)'" onmouseout="this.style.borderColor='var(--border-color)'; this.style.boxShadow='none'">
                                        <a href="${url}" style="text-decoration: none; display: block; margin-bottom: 10px;">
                                            <img src="${img}" style="width: 100px; height: 100px; object-fit: contain; margin: 0 auto;">
                                        </a>
                                        <a href="${url}" style="text-decoration: none; color: var(--text-dark); font-weight: 700; font-size: 0.9rem; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; height: 2.7em; margin-bottom: 8px; line-height: 1.35;">${name}</a>
                                        <div style="color: var(--primary); font-weight: 800; font-size: 1rem; margin-bottom: 10px;">${price}</div>
                                        <a href="${url}" class="btn-pill btn-blue" style="padding: 6px 12px; font-size: 0.8rem; border-radius: 6px; text-decoration: none; font-weight: 700; display: inline-block; box-shadow: none !important;">Xem chi tiết</a>
                                    </div>
                                </div>
                            `;
                        });
                    }
                    updateRecentNavVisibility();
                    swiperRecent.on('resize', updateRecentNavVisibility);
                    swiperRecent.on('update', updateRecentNavVisibility);
                }
            });
        </script>
    </div>
    """
    full_html = clean_liquid_tags(header_part + compare_html + local_footer_part, 'compare')
    full_html = inject_seo_metadata(
        full_html,
        title="So Sánh Sản Phẩm - Nava Store",
        description="So sánh các sản phẩm Mini PC, eGPU để lựa chọn sản phẩm phù hợp nhất với nhu cầu của bạn.",
        keywords="so sanh san pham, mini pc, egpu, nava store"
    )
    with open(os.path.join(base_dir, "demo_compare.html"), "w", encoding="utf-8") as f:
        f.write(full_html)

def build_cart_page(base_dir, header_part, footer_part):
    sticky_stuff = ""
    with open(os.path.join(base_dir, "index.bwt"), "r", encoding="utf-8") as f:
        idx_content = f.read()
        if "<!-- Mobile Sidebar Drawer -->" in idx_content:
            sticky_stuff = idx_content[idx_content.find("<!-- Mobile Sidebar Drawer -->"):]
            if "<!-- /MASTER SAPO ESCAPE WRAPPER -->" in sticky_stuff:
                sticky_stuff = sticky_stuff.split("<!-- /MASTER SAPO ESCAPE WRAPPER -->")[0]
                
    local_footer_part = sticky_stuff + '<script src="assets/main.js" defer></script>\n' + footer_part

    cart_html = """
        <style>
            .nava-cart-page { padding: 0; max-width: 1200px; margin: 20px auto 60px; }
            .cart-title { font-size: 2.2rem; font-weight: 900; color: var(--text-dark); margin-bottom: 30px; display: flex; align-items: center; gap: 10px; }
            .cart-title i { color: var(--primary); }
            
            .cart-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 30px; }
            
            .cart-items-container { background: transparent !important; border: none !important; box-shadow: none !important; padding: 0 !important; }
            
            /* Override Sapo BWT cart basket item styles */
            .cart-item { 
                display: flex !important; gap: 20px; align-items: center; padding: 20px !important; margin-bottom: 20px; 
                background: var(--bg-white) !important; border: 1px solid var(--border-color) !important; border-radius: 16px !important; 
                box-shadow: 0 4px 10px rgba(0,0,0,0.03) !important; transition: all 0.3s ease !important; position: relative;
            }
            .cart-item:hover {
                border-color: var(--primary) !important;
                box-shadow: 0 10px 25px rgba(0, 51, 102, 0.08) !important;
                transform: translateY(-2px);
            }
            .cart-item:last-child { margin-bottom: 0; }
            
            .cart-item-img { 
                width: 100px !important; height: 100px !important; max-width: 100px !important; max-height: 100px !important; 
                object-fit: contain; border-radius: 12px; background: var(--bg-gray); padding: 10px; 
                border: 1px solid var(--border-color); position: static !important; display: block !important; flex-shrink: 0;
            }
            
            .cart-item-details { 
                flex: 1 !important; max-width: none !important; display: flex; flex-direction: column; padding: 0 !important; margin: 0 20px !important; 
            }
            
            .cart-item-title { 
                font-size: 1.05rem; font-weight: 700; color: var(--text-dark); margin-bottom: 5px; line-height: 1.4; text-decoration: none; display: block;
            }
            .cart-item-title:hover { color: var(--primary); }
            .cart-item-variant { font-size: 0.85rem; color: var(--text-gray); margin-top: 4px; display: block; }
            
            .cart-item-price { 
                font-size: 1.15rem; font-weight: 800; color: var(--primary); text-align: left !important; margin: 5px 0 0 0 !important;
            }
            
            .qty-spinner { 
                display: inline-flex !important; align-items: center; border: 1px solid var(--border-color); 
                border-radius: 20px; overflow: hidden; background: var(--bg-gray); height: 36px; width: fit-content; flex-shrink: 0;
            }
            .qty-btn { 
                width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; 
                background: transparent; border: none; cursor: pointer; color: var(--text-dark); transition: 0.2s; font-weight: 600;
            }
            .qty-btn:hover { background: rgba(0, 51, 102, 0.1); color: var(--primary); }
            .qty-input { 
                width: 40px; height: 36px; text-align: center; border: none; background: transparent; 
                font-weight: 700; font-size: 0.95rem; color: var(--text-dark); outline: none; 
            }
            
            .cart-item-remove { 
                background: #fee2e2 !important; color: #ef4444 !important; border: none !important; cursor: pointer; 
                display: inline-flex !important; align-items: center; justify-content: center; transition: 0.2s; 
                font-size: 0.85rem !important; font-weight: 700; padding: 0 16px !important; height: 36px; width: auto !important;
                border-radius: 18px !important; margin-left: 20px !important; flex-shrink: 0;
            }
            .cart-item-remove:hover { background: #ef4444 !important; color: white !important; transform: none !important; }
     
            .cart-summary { background: var(--bg-white); border-radius: var(--radius-lg); padding: 25px; box-shadow: var(--shadow-sm); border: 1px solid var(--border-color); height: fit-content; position: sticky; top: 120px; }
            .summary-title { font-size: 1.2rem; font-weight: 800; color: var(--text-dark); margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px solid var(--border-color); }
            
            .summary-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; font-size: 0.95rem; color: var(--text-gray); font-weight: 500; gap: 15px; }
            .summary-row span:first-child { white-space: nowrap; }
            .summary-total { display: flex; justify-content: space-between; align-items: center; margin-top: 20px; padding-top: 20px; border-top: 2px dashed var(--border-color); font-size: 1.2rem; font-weight: 900; color: var(--text-dark); gap: 15px; }
            .summary-total-label { white-space: nowrap; }
            .summary-total-price { color: var(--primary); font-size: 1.5rem; white-space: nowrap; }
            
            .btn-checkout-nava { display: flex; align-items: center; justify-content: center; gap: 8px; width: 100%; padding: 15px; background: linear-gradient(90deg, var(--primary), var(--primary-light)); color: white !important; text-align: center; border-radius: var(--radius-md); font-weight: 800; font-size: 1.1rem; text-decoration: none; text-transform: uppercase; letter-spacing: 1px; transition: all 0.3s; margin-top: 20px; box-shadow: 0 10px 20px rgba(0, 51, 102, 0.2); border: none; cursor: pointer; }
            .btn-checkout-nava:hover { transform: translateY(-3px); box-shadow: 0 15px 25px rgba(0, 51, 102, 0.3); color: white !important; }
            
            @media (max-width: 991px) {
                .cart-grid { grid-template-columns: 1fr; }
                .cart-summary { position: static; }
                .nava-cart-page { margin-top: 20px; }
            }
            @media (max-width: 575px) {
                .nava-cart-page { margin-top: 15px !important; padding-bottom: 80px !important; }
                .cart-title { font-size: 1.25rem !important; margin-bottom: 20px !important; gap: 8px !important; line-height: 1.3; }
                .cart-title i { font-size: 1.5rem !important; }
                
                .cart-items-container { padding: 0 !important; }
                .cart-item { 
                    display: grid !important; grid-template-columns: 80px 1fr !important; gap: 10px 15px !important; 
                    align-items: flex-start !important; padding: 15px !important; margin-bottom: 15px;
                }
                .cart-item-img { 
                    width: 80px !important; height: 80px !important; max-width: 80px !important; max-height: 80px !important;
                    display: block !important; position: static !important; grid-row: span 2;
                }
                
                .cart-item-price { font-size: 1.05rem !important; margin: 3px 0 6px 0 !important; }
                .cart-item-variant { font-size: 0.75rem !important; margin-bottom: 0 !important; }
                .cart-item-title { font-size: 0.92rem !important; line-height: 1.3; font-weight: 700 !important; }
                
                .qty-spinner { height: 32px !important; border-radius: 6px !important; }
                .qty-btn { width: 30px !important; height: 30px !important; font-size: 0.85rem !important; }
                .qty-input { width: 30px !important; height: 30px !important; font-size: 0.85rem !important; }
                
                .cart-item-remove { 
                    position: static !important; width: auto !important; height: 32px !important; padding: 0 12px !important;
                    border-radius: 16px !important; margin: 0 !important; font-size: 0.78rem !important; display: inline-flex !important;
                    align-items: center; justify-content: center;
                }
                
                /* Action wrapper for mobile */
                .cart-item-actions {
                    grid-column: 2; display: flex !important; align-items: center; justify-content: space-between; margin-top: 5px; gap: 10px; width: 100%; box-sizing: border-box;
                }
                .cart-item-actions .cart-item-remove { margin-left: 0 !important; }
     
                .cart-summary { padding: 15px !important; }
                .summary-title { font-size: 1.05rem !important; margin-bottom: 15px !important; padding-bottom: 10px !important; }
                .summary-row { font-size: 0.85rem !important; margin-bottom: 12px !important; }
                .summary-total { margin-top: 15px !important; padding-top: 15px !important; }
                .summary-total-label { font-size: 1.05rem !important; }
                .summary-total-price { font-size: 1.25rem !important; }
                .btn-checkout-nava { padding: 12px !important; font-size: 0.95rem !important; margin-top: 15px !important; }
                
                /* Ticket badges */
                .ticket-badge { padding: 3px 8px !important; font-size: 0.75rem !important; margin-right: 4px !important; }
                .ticket-badge::before { left: -3.5px !important; width: 4px !important; height: 6px !important; }
                .ticket-badge::after { right: -3.5px !important; width: 4px !important; height: 6px !important; }
 
                /* Voucher section mobile */
                .shopee-voucher-container { padding: 10px !important; margin: 15px 0 !important; }
                .voucher-header { margin-bottom: 8px !important; gap: 8px !important; }
                .voucher-tag { font-size: 0.65rem !important; padding: 3px 6px !important; }
                .voucher-title { font-size: 0.8rem !important; }
                .voucher-ticket::before { right: 53px !important; }
                .voucher-ticket::after { right: 53px !important; }
                .voucher-left { padding: 10px !important; }
                .voucher-right { width: 60px !important; }
                .voucher-desc { font-size: 0.78rem !important; }
                .voucher-subtext { font-size: 0.72rem !important; }
                .kol-input-box { margin-top: 10px !important; gap: 6px !important; }
                .kol-input { padding: 8px 10px !important; font-size: 0.82rem !important; }
                .kol-btn { padding: 8px 14px !important; font-size: 0.82rem !important; }
            }
        </style>
        
        <div class="nava-cart-page">
            <div class="breadcrumb" style="background: transparent; padding: 0; margin-bottom: 20px;">
                <a href="/" style="color: var(--text-gray); text-decoration: none;"><i class="ph ph-house"></i> Trang chủ</a> 
                <span style="margin: 0 10px; color: var(--text-gray);">/</span> 
                <span style="color: var(--primary); font-weight: bold;">Giỏ hàng</span>
            </div>th: 100%; }
                .cart-item-title { font-size: 0.92rem !important; line-height: 1.3; font-weight: 700 !important; }
                .cart-item-variant { font-size: 0.75rem !important; margin-bottom: 6px !important; }
                .cart-item-price { font-size: 1.05rem !important; }
                
                .cart-item-actions { grid-column: 2; display: flex !important; align-items: center; justify-content: space-between; margin-top: 5px; gap: 10px; width: 100%; box-sizing: border-box; }
                .qty-spinner { height: 32px !important; border-radius: 6px !important; display: inline-flex !important; align-items: center !important; overflow: hidden !important; }
                .qty-btn { width: 30px !important; height: 30px !important; font-size: 0.85rem !important; padding: 0 !important; margin: 0 !important; display: flex !important; align-items: center !important; justify-content: center !important; }
                .qty-input { width: 30px !important; height: 30px !important; font-size: 0.85rem !important; padding: 0 !important; margin: 0 !important; text-align: center !important; }
                .cart-item-remove { width: 32px !important; height: 32px !important; display: flex !important; align-items: center !important; justify-content: center !important; padding: 0 !important; }
                .cart-item-remove i { font-size: 1rem !important; }

                /* Order Summary mobile optimizations */
                .cart-summary { padding: 15px !important; }
                .summary-title { font-size: 1.05rem !important; margin-bottom: 15px !important; padding-bottom: 10px !important; }
                .summary-row { font-size: 0.85rem !important; margin-bottom: 12px !important; }
                .summary-total { margin-top: 15px !important; padding-top: 15px !important; }
                .summary-total-label { font-size: 1.05rem !important; }
                .summary-total-price { font-size: 1.25rem !important; }
                .btn-checkout-nava { padding: 12px !important; font-size: 0.95rem !important; margin-top: 15px !important; }
                
                /* Badges on mobile */
                .ticket-badge { padding: 3px 8px !important; font-size: 0.75rem !important; margin-right: 4px !important; }
                .ticket-badge::before { left: -3.5px !important; width: 4px !important; height: 6px !important; }
                .ticket-badge::after { right: -3.5px !important; width: 4px !important; height: 6px !important; }

                /* Voucher section mobile */
                .shopee-voucher-container { padding: 10px !important; margin: 15px 0 !important; }
                .voucher-header { margin-bottom: 8px !important; gap: 8px !important; }
                .voucher-tag { font-size: 0.65rem !important; padding: 3px 6px !important; }
                .voucher-title { font-size: 0.8rem !important; }
                .voucher-ticket::before { right: 53px !important; }
                .voucher-ticket::after { right: 53px !important; }
                .voucher-left { padding: 10px !important; }
                .voucher-right { width: 60px !important; }
                .voucher-desc { font-size: 0.78rem !important; }
                .voucher-subtext { font-size: 0.72rem !important; }
                .kol-input-box { margin-top: 10px !important; gap: 6px !important; }
                .kol-input { padding: 8px 10px !important; font-size: 0.82rem !important; }
                .kol-btn { padding: 8px 14px !important; font-size: 0.82rem !important; }
            }
        </style>
        
        <div class="nava-cart-page">
            <div class="breadcrumb" style="background: transparent; padding: 0; margin-bottom: 20px;">
                <a href="/" style="color: var(--text-gray); text-decoration: none;"><i class="ph ph-house"></i> Trang chủ</a> 
                <span style="margin: 0 10px; color: var(--text-gray);">/</span> 
                <span style="color: var(--primary); font-weight: bold;">Giỏ hàng</span>
            </div>
            
            <h1 class="cart-title"><i class="ph-fill ph-shopping-cart"></i> <span>Giỏ hàng của bạn (<span id="cart-qty-title">2</span> sản phẩm)</span></h1>
            
            <div class="cart-grid">
                <!-- Left: Cart Items -->
                <div class="cart-items-container">
                    <!-- Item 1 -->
                    <div class="cart-item" data-price="4490000" id="cart-item-1">
                        <img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" alt="ASUS NUC 14" class="cart-item-img">
                        <div class="cart-item-details">
                            <a href="demo_product.html" class="cart-item-title">ASUS NUC 14 Essential</a>
                            <div class="cart-item-variant">Core i3 / 8GB / 256GB</div>
                            <div class="cart-item-price">4.490.000đ</div>
                        </div>
                        <div class="cart-item-actions">
                            <div class="qty-spinner">
                                <button class="qty-btn" onclick="changeQty(this, -1)"><i class="ph-bold ph-minus"></i></button>
                                <input type="text" value="1" class="qty-input" readonly>
                                <button class="qty-btn" onclick="changeQty(this, 1)"><i class="ph-bold ph-plus"></i></button>
                            </div>
                            <button class="cart-item-remove" onclick="removeCartItem(this)" title="Xóa sản phẩm"><i class="ph-bold ph-trash"></i></button>
                        </div>
                    </div>
                    
                    <!-- Item 2 -->
                    <div class="cart-item" data-price="31190000" id="cart-item-2">
                        <img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_1.png" alt="GMK EVO X1" class="cart-item-img">
                        <div class="cart-item-details">
                            <a href="demo_product.html" class="cart-item-title">GMK EVO X1 32G</a>
                            <div class="cart-item-variant">Ryzen AI 9 HX370 / 32GB / 1TB</div>
                            <div class="cart-item-price">31.190.000đ</div>
                        </div>
                        <div class="cart-item-actions">
                            <div class="qty-spinner">
                                <button class="qty-btn" onclick="changeQty(this, -1)"><i class="ph-bold ph-minus"></i></button>
                                <input type="text" value="1" class="qty-input" readonly>
                                <button class="qty-btn" onclick="changeQty(this, 1)"><i class="ph-bold ph-plus"></i></button>
                            </div>
                            <button class="cart-item-remove" onclick="removeCartItem(this)" title="Xóa sản phẩm"><i class="ph-bold ph-trash"></i></button>
                        </div>
                    </div>
                    
                    <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid var(--border-color); display: flex; justify-content: space-between; align-items: center;">
                        <a href="demo_collection.html" style="color: var(--primary); text-decoration: none; font-weight: 600; display: inline-flex; align-items: center; gap: 5px;"><i class="ph-bold ph-arrow-left"></i> Tiếp tục mua sắm</a>
                    </div>
                </div>
                
                <!-- Right: Summary -->
                <div class="cart-summary">
                    <h2 class="summary-title">Tóm Tắt Đơn Hàng</h2>
                    
                    <div class="summary-row" style="align-items: center;">
                        <span id="summary-qty-label">Tạm tính (2 sản phẩm)</span>
                        <span id="summary-subtotal-val" style="font-weight: 700; color: var(--text-dark);">35.680.000đ</span>
                    </div>
                    
                    <div class="summary-row" style="align-items: center;">
                        <span>Phí vận chuyển</span>
                        <span class="ticket-badge ticket-green">Miễn phí</span>
                    </div>
                    
                    <div class="summary-row" id="summary-discount-row" style="align-items: center;">
                        <span>Giảm giá (Voucher)</span>
                        <span id="summary-discount-value" class="ticket-badge ticket-blue">-356.800đ</span>
                    </div>
                    
                    <!-- NAVA Voucher Section (Shopee Style) -->
                    <style>
                        /* Ticket Badge Styling for discounts and shipping */
                        .ticket-badge {
                            position: relative;
                            display: inline-flex;
                            align-items: center;
                            justify-content: center;
                            background: transparent;
                            padding: 4px 14px;
                            font-size: 0.85rem;
                            font-weight: 700;
                            border-radius: 6px;
                            border: 1.5px solid currentColor;
                            line-height: 1.2;
                            box-sizing: border-box;
                        }
                        .ticket-badge::before,
                        .ticket-badge::after {
                            content: '';
                            position: absolute;
                            top: 50%;
                            width: 6px;
                            height: 8px;
                            background: var(--bg-white, #ffffff);
                            border: 1.5px solid currentColor;
                            border-radius: 50%;
                            transform: translateY(-50%);
                            box-sizing: border-box;
                            z-index: 2;
                        }
                        .ticket-badge::before {
                            left: -4.5px;
                            clip-path: inset(0 0 0 3px);
                        }
                        .ticket-badge::after {
                            right: -4.5px;
                            clip-path: inset(0 3px 0 0);
                        }
                        .ticket-green {
                            color: #10b981 !important;
                            background: rgba(16, 185, 129, 0.04);
                        }
                        .ticket-blue {
                            color: var(--primary) !important;
                            background: rgba(0, 51, 102, 0.04);
                        }
                        [data-theme="dark"] .ticket-badge::before,
                        [data-theme="dark"] .ticket-badge::after {
                            background: var(--bg-white, #1e293b);
                        }

                        .shopee-voucher-container {
                            border: 1px solid var(--border-color);
                            background: var(--bg-gray);
                            border-radius: var(--radius-md);
                            padding: 16px;
                            margin: 20px 0;
                            font-family: inherit;
                        }
                        .voucher-header {
                            display: flex;
                            align-items: center;
                            gap: 10px;
                            margin-bottom: 12px;
                        }
                        .voucher-tag {
                            background: rgba(0, 51, 102, 0.08); /* brand blue light tint */
                            color: var(--primary);
                            font-size: 0.72rem;
                            font-weight: 700;
                            padding: 4px 8px;
                            border-radius: 6px;
                            letter-spacing: 0.5px;
                            display: inline-flex;
                            align-items: center;
                            gap: 4px;
                            white-space: nowrap;
                            flex-shrink: 0;
                        }
                        [data-theme="dark"] .voucher-tag {
                            background: rgba(51, 133, 255, 0.15);
                            color: #66a3ff;
                        }
                        .voucher-title {
                            font-weight: 700;
                            color: var(--text-dark);
                            font-size: 0.9rem;
                        }
                        .voucher-ticket {
                            display: flex;
                            align-items: stretch;
                            background: var(--bg-white, #ffffff);
                            border: 1px solid var(--border-color);
                            border-radius: 12px;
                            overflow: hidden;
                            position: relative;
                            box-shadow: 0 4px 12px rgba(0,0,0,0.02);
                        }
                        /* Ticket style circular notches centered at the boundary between left and right */
                        .voucher-ticket::before,
                        .voucher-ticket::after {
                            content: '';
                            position: absolute;
                            width: 14px;
                            height: 14px;
                            background: var(--bg-gray); /* Blends with shopee-voucher-container background */
                            border: 1px solid var(--border-color);
                            border-radius: 50%;
                            z-index: 5;
                            box-sizing: border-box;
                        }
                        .voucher-ticket::before {
                            top: -7px;
                            right: 63px; /* centered at 70px boundary: 70 - 7 = 63px */
                            clip-path: inset(7px 0 0 0); /* only show bottom half */
                        }
                        .voucher-ticket::after {
                            bottom: -7px;
                            right: 63px; /* centered at 70px boundary: 70 - 7 = 63px */
                            clip-path: inset(0 0 7px 0); /* only show top half */
                        }
                        .voucher-left {
                            background: var(--bg-white);
                            padding: 16px 20px;
                            flex: 1;
                            display: flex;
                            flex-direction: column;
                            justify-content: center;
                            align-items: flex-start;
                            text-align: left;
                            border-right: 1px dashed var(--border-color);
                            box-sizing: border-box;
                        }
                        .voucher-right {
                            background: #003366;
                            width: 70px;
                            flex-shrink: 0;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            box-sizing: border-box;
                        }
                        .voucher-checkbox {
                            width: 24px;
                            height: 24px;
                            border-radius: 6px;
                            background: rgba(255, 255, 255, 0.2);
                            border: 1.5px solid #ffffff;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                        }
                        .voucher-checkbox i {
                            color: #ffffff;
                            font-size: 1rem;
                        }
                        [data-theme="dark"] .voucher-left {
                            background: var(--bg-white);
                        }
                        [data-theme="dark"] .voucher-right {
                            background: #002244;
                        }
                        .voucher-desc {
                            font-weight: 700;
                            color: var(--text-dark);
                            margin-bottom: 3px;
                            font-size: 0.85rem;
                        }
                        .voucher-subtext {
                            color: var(--text-gray);
                            font-size: 0.78rem;
                        }
                        .kol-input-box {
                            display: flex;
                            gap: 8px;
                            margin-top: 15px;
                        }
                        .kol-input {
                            flex: 1;
                            padding: 10px 14px;
                            border: 1px solid var(--border-color);
                            border-radius: 8px;
                            font-size: 0.88rem;
                            outline: none;
                            background: var(--bg-white, #ffffff);
                            transition: 0.2s;
                            box-sizing: border-box;
                            min-width: 0; /* allows input to shrink on small screens */
                        }
                        .kol-input:focus {
                            border-color: var(--primary);
                            background: var(--bg-white, #ffffff);
                        }
                        .kol-btn {
                            padding: 10px 20px;
                            background: var(--primary);
                            color: white;
                            border: none;
                            border-radius: 8px;
                            font-weight: 700;
                            cursor: pointer;
                            transition: all 0.2s;
                            font-size: 0.88rem;
                            white-space: nowrap;
                            flex-shrink: 0;
                        }
                        .kol-btn:hover {
                            background: var(--primary-light);
                        }
                    </style>
                    <div class="shopee-voucher-container">
                        <div class="voucher-header">
                            <span class="voucher-tag"><i class="ph-fill ph-tag"></i> NAVA Voucher</span>
                            <span class="voucher-title">Khuyến mãi dành cho bạn</span>
                        </div>
                        <div class="voucher-ticket">
                            <div class="voucher-left">
                                <div class="voucher-desc" id="applied-voucher-title">Tự động áp dụng mã NAVAVIP</div>
                                <div class="voucher-subtext" id="applied-voucher-sub">Đã giảm <span id="voucher-discount-amount" style="color: var(--primary); font-weight: 800;">356.800đ</span></div>
                            </div>
                            <div class="voucher-right">
                                <div class="voucher-checkbox">
                                    <i class="ph-bold ph-check"></i>
                                </div>
                            </div>
                        </div>
                        <div class="kol-input-box">
                            <input type="text" class="kol-input" id="kol-code-input" placeholder="Nhập mã giảm giá...">
                            <button class="kol-btn" onclick="applyKOLCode()">Áp dụng</button>
                        </div>
                        <div id="kol-alert" style="display: none; font-size: 0.8rem; font-weight: 600; margin-top: 8px; color: #10b981;"></div>
                    </div>
                    
                    <div class="summary-total">
                        <span>Tổng Tiền</span>
                        <span class="summary-total-price" id="summary-total-price-val">35.323.200đ</span>
                    </div>
                    
                    <a href="demo_checkout.html" class="btn-checkout-nava">Thanh Toán <i class="ph-bold ph-arrow-right" style="vertical-align: middle; margin-left: 5px;"></i></a>
                    
                    <div style="margin-top: 20px; text-align: center;">
                        <p style="font-size: 0.85rem; color: var(--text-gray); margin-bottom: 10px;">An toàn & Bảo mật</p>
                        <div style="display: flex; gap: 10px; justify-content: center;">
                            <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/payment-1.png?1778729235331" alt="Visa" style="height: 25px;">
                            <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/payment-2.png?1778729235331" alt="Mastercard" style="height: 25px;">
                            <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/payment-4.png?1778729235331" alt="JCB" style="height: 25px;">
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            let cartSubtotal = 35680000;
            let activeDiscountPercent = 1;
            let activeDiscountValue = 356800;
            let appliedCode = 'NAVAVIP';
            
            function changeQty(btn, delta) {
                const spinner = btn.closest('.qty-spinner');
                const input = spinner.querySelector('.qty-input');
                let val = parseInt(input.value) || 1;
                val += delta;
                if (val < 1) val = 1;
                input.value = val;
                recalculateSubtotal();
            }
            
            function removeCartItem(btn) {
                const item = btn.closest('.cart-item');
                if (item) {
                    item.remove();
                    recalculateSubtotal();
                }
            }
            
            function recalculateSubtotal() {
                let subtotal = 0;
                let itemCount = 0;
                const items = document.querySelectorAll('.cart-item');
                items.forEach(item => {
                    const price = parseInt(item.getAttribute('data-price')) || 0;
                    const qty = parseInt(item.querySelector('.qty-input').value) || 1;
                    subtotal += price * qty;
                    itemCount += qty;
                });
                
                cartSubtotal = subtotal;
                
                // Update item count in UI
                const titleEl = document.querySelector('.cart-title');
                if (titleEl) {
                    titleEl.innerHTML = `<i class="ph-fill ph-shopping-cart"></i> <span>Giỏ hàng của bạn (${itemCount} sản phẩm)</span>`;
                }
                
                const summaryQtyEl = document.getElementById('summary-qty-label');
                if (summaryQtyEl) {
                    summaryQtyEl.textContent = `Tạm tính (${itemCount} sản phẩm)`;
                }
                
                const summarySubtotalEl = document.getElementById('summary-subtotal-val');
                if (summarySubtotalEl) {
                    summarySubtotalEl.textContent = subtotal.toLocaleString('vi-VN') + 'đ';
                }
                
                let qty1 = 0;
                let qty2 = 0;
                const item1 = document.getElementById('cart-item-1');
                if (item1) qty1 = parseInt(item1.querySelector('.qty-input').value) || 0;
                const item2 = document.getElementById('cart-item-2');
                if (item2) qty2 = parseInt(item2.querySelector('.qty-input').value) || 0;
                
                localStorage.setItem('nava_qty_item1', qty1);
                localStorage.setItem('nava_qty_item2', qty2);
                localStorage.setItem('nava_cart_subtotal', subtotal);
                
                if (itemCount === 0) {
                    const grid = document.querySelector('.cart-grid');
                    if (grid) {
                        grid.innerHTML = `
                            <div style="grid-column: 1 / -1; text-align: center; padding: 50px 20px;">
                                <i class="ph ph-shopping-cart-simple" style="font-size: 5rem; color: var(--text-gray); margin-bottom: 20px; display: block;"></i>
                                <h2 style="font-size: 1.5rem; font-weight: 700; color: var(--text-dark); margin-bottom: 10px;">Giỏ hàng của bạn đang trống</h2>
                                <p style="color: var(--text-gray); margin-bottom: 25px;">Hãy tiếp tục khám phá và mua sắm các sản phẩm công nghệ tuyệt vời tại Nava Store.</p>
                                <a href="demo_collection.html" class="btn-nava btn-primary-nava" style="display: inline-flex; width: auto; padding: 12px 30px; text-decoration: none; border-radius: 8px;">Tiếp tục mua sắm</a>
                            </div>
                        `;
                    }
                    localStorage.setItem('nava_cart_total', 0);
                    localStorage.setItem('nava_discount_val', 0);
                    return;
                }
                
                updateCartTotals();
            }
            
            function updateCartTotals() {
                const discountValEl = document.getElementById('voucher-discount-amount');
                const discountSummaryEl = document.getElementById('summary-discount-value');
                const totalPriceEl = document.getElementById('summary-total-price-val');
                
                // Recalculate
                activeDiscountValue = Math.round(cartSubtotal * (activeDiscountPercent / 100));
                let finalTotal = cartSubtotal - activeDiscountValue;
                
                // Format currency
                const discountStr = activeDiscountValue.toLocaleString('vi-VN') + 'đ';
                const finalStr = finalTotal.toLocaleString('vi-VN') + 'đ';
                
                if (discountValEl) discountValEl.innerText = discountStr;
                if (discountSummaryEl) discountSummaryEl.innerText = '-' + discountStr;
                if (totalPriceEl) totalPriceEl.innerText = finalStr;
                
                // Save to localStorage so checkout page can sync
                localStorage.setItem('nava_discount_percent', activeDiscountPercent);
                localStorage.setItem('nava_discount_code', appliedCode);
                localStorage.setItem('nava_discount_val', activeDiscountValue);
                localStorage.setItem('nava_cart_total', finalTotal);
            }
            
            function applyKOLCode() {
                const input = document.getElementById('kol-code-input');
                const alertBox = document.getElementById('kol-alert');
                const titleEl = document.getElementById('applied-voucher-title');
                const subEl = document.getElementById('applied-voucher-sub');
                const code = input.value.trim().toUpperCase();
                
                if (!code) return;
                
                if (code === 'KOL10') {
                    activeDiscountPercent = 10;
                    appliedCode = 'KOL10';
                    alertBox.style.color = '#10b981';
                    alertBox.innerText = '🎉 Đã áp dụng mã KOL10: Giảm 10% tổng đơn hàng!';
                    titleEl.innerText = 'Đã áp dụng mã KOL10';
                    alertBox.style.display = 'block';
                    updateCartTotals();
                } else if (code === 'NAVA50') {
                    activeDiscountPercent = 50;
                    appliedCode = 'NAVA50';
                    alertBox.style.color = '#10b981';
                    alertBox.innerText = '🎉 Siêu Voucher NAVA50: Giảm 50% tổng đơn hàng!';
                    titleEl.innerText = 'Đã áp dụng mã NAVA50';
                    alertBox.style.display = 'block';
                    updateCartTotals();
                } else if (code === 'NAVAVIP') {
                    activeDiscountPercent = 1;
                    appliedCode = 'NAVAVIP';
                    alertBox.style.color = '#10b981';
                    alertBox.innerText = 'Đã áp dụng mã giảm giá mặc định NAVAVIP';
                    titleEl.innerText = 'Tự động áp dụng mã NAVAVIP';
                    alertBox.style.display = 'block';
                    updateCartTotals();
                } else {
                    alertBox.style.color = '#ef4444';
                    alertBox.innerText = '❌ Mã voucher không hợp lệ hoặc đã hết lượt sử dụng!';
                    alertBox.style.display = 'block';
                }
            }
            
            // Initialize on load
            window.addEventListener('DOMContentLoaded', () => {
                const q1 = localStorage.getItem('nava_qty_item1') !== null ? parseInt(localStorage.getItem('nava_qty_item1')) : 1;
                const q2 = localStorage.getItem('nava_qty_item2') !== null ? parseInt(localStorage.getItem('nava_qty_item2')) : 1;
                
                const item1 = document.getElementById('cart-item-1');
                if (item1) {
                    if (q1 > 0) {
                        item1.querySelector('.qty-input').value = q1;
                    } else {
                        item1.remove();
                    }
                }
                const item2 = document.getElementById('cart-item-2');
                if (item2) {
                    if (q2 > 0) {
                        item2.querySelector('.qty-input').value = q2;
                    } else {
                        item2.remove();
                    }
                }
                recalculateSubtotal();
            });
        </script>
    """
    full_html = clean_liquid_tags(header_part + cart_html + local_footer_part, 'cart')
    full_html = inject_seo_metadata(
        full_html,
        title="Giỏ Hàng - Nava Store",
        description="Giỏ hàng của bạn tại Nava Store. Kiểm tra sản phẩm và tiến hành thanh toán.",
        keywords="gio hang, nava store, thanh toan"
    )
    with open(os.path.join(base_dir, "demo_cart.html"), "w", encoding="utf-8") as f:
        f.write(full_html)

def build_checkout_page(base_dir):
    # Standalone Checkout UI matching App
    checkout_html = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nava Store - Thanh Toán</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="assets/style.css?v=2">
    <link rel="stylesheet" href="assets/checkout.css">
    <script src="https://unpkg.com/@phosphor-icons/web"></script>
</head>
<body>
    <div class="bg-glow orb-1"></div>
    <div class="bg-glow orb-2"></div>
    <div class="bg-glow orb-3"></div>
    <img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/favicon.png?1775454528082" alt="Decor" class="bg-decor-logo top-left" aria-hidden="true" loading="lazy" decoding="async" style="pointer-events: none; z-index: 0; opacity: 0.4;">
    <div class="container" style="position: relative; z-index: 10;">
        <div class="checkout-grid">
            <!-- Left: Forms -->
            <div class="checkout-main">
                <!-- Shipping Info -->
                <div class="checkout-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <h2 class="section-title" style="margin: 0; font-size: 1.2rem;"><i class="ph-fill ph-map-pin"></i> Thông tin mua hàng</h2>
                        <a href="demo_login.html" style="color: var(--primary); text-decoration: none; font-size: 0.9rem; font-weight: 600;"><i class="ph-bold ph-sign-out"></i> Đăng xuất</a>
                    </div>
                    
                    <!-- NATURAL ORDER FOR FIELDS: Full Name -> Phone -> Email -> Address -->
                    <div class="input-group">
                        <label>Họ và tên</label>
                        <input type="text" class="nava-input" id="checkout-fullname" placeholder="Nhập họ và tên" value="Turnio Dev" required>
                    </div>

                    <div class="input-group">
                        <label>Số điện thoại</label>
                        <input type="tel" class="nava-input" id="checkout-phone" placeholder="Nhập số điện thoại" value="0972178527" required>
                    </div>

                    <div class="input-group">
                        <label>Email (tùy chọn)</label>
                        <input type="email" class="nava-input" id="checkout-email" placeholder="Nhập địa chỉ Email" value="turniodev@gmail.com">
                    </div>
                    
                    <div class="input-group">
                        <label>Địa chỉ nhận hàng</label>
                        <div id="address-trigger" onclick="openAddressModal()" class="nava-input" style="cursor: pointer; display: flex; align-items: center; gap: 10px; background: var(--bg-white); min-height: 52px; user-select: none;">
                            <i class="ph-bold ph-map-pin" style="color: var(--primary); font-size: 1.1rem; flex-shrink: 0;"></i>
                            <span id="address-display" style="flex: 1; font-weight: 600; color: var(--text-dark); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; pointer-events: none;">Thành phố Thủ Đức, TP Hồ Chí Minh</span>
                            <i class="ph-bold ph-caret-down" style="color: var(--text-muted); flex-shrink: 0;"></i>
                        </div>
                        <input type="text" id="street-address-input" class="nava-input" placeholder="Số nhà, tên đường..." style="margin-top: 10px; display: block;" value="270 Đường Linh Trung">
                        <input type="hidden" id="province-select" value="HCM">
                        <input type="hidden" id="ward-select" value="1">
                    </div>
                    
                    <div class="input-group" style="margin-bottom: 0;">
                        <label>Ghi chú đơn hàng (tùy chọn)</label>
                        <textarea class="nava-input" rows="3" placeholder="Nhập ghi chú hoặc yêu cầu giao hàng..."></textarea>
                    </div>
                </div>
                <!-- Payment Methods -->
                <div class="checkout-card">
                    <h2 class="section-title" style="font-size: 1.2rem; margin-bottom: 20px;"><i class="ph-fill ph-credit-card"></i> Thanh toán</h2>
                            
                    <div style="border: 1px solid var(--border-color); border-radius: var(--radius-md); background: var(--bg-white); overflow: hidden;">
                        <div class="payment-method-wrapper" style="margin: 0; border-bottom: 1px solid var(--border-color);">
                            <label class="radio-option" style="border: none; border-radius: 0; margin: 0; background: transparent; padding: 15px;">
                                <input type="radio" name="payment" value="bank" checked>
                                <div>
                                    <span class="radio-label">Chuyển khoản qua ngân hàng (ACB Auto-banking)</span>
                                </div>
                                <i class="ph-fill ph-bank" style="font-size: 1.5rem; color: var(--primary); margin-left: auto;"></i>
                            </label>
                            <div class="payment-details" id="bank-details" style="display: block; padding: 0 15px 15px 15px; margin: 0;">
                                <div style="background: #f8fafc; border: 1px solid var(--border-color); border-radius: 12px; padding: 20px; text-align: left; margin-top: 5px;">
                                    <p style="font-weight: 800; color: var(--text-dark); margin: 0 0 15px 0; text-align: center; font-size: 1.05rem;"><i class="ph-bold ph-info"></i> THÔNG TIN CHUYỂN KHOẢN</p>
                                    
                                    <div style="display: flex; flex-direction: column; gap: 12px; margin-bottom: 20px;">
                                        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); padding-bottom: 8px;">
                                            <span style="color: var(--text-gray); font-size: 0.9rem;">Ngân hàng</span>
                                            <span style="font-weight: 700; color: var(--text-dark); font-size: 0.95rem;">TMCP Á Châu (ACB)</span>
                                        </div>
                                        
                                        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); padding-bottom: 8px;">
                                            <span style="color: var(--text-gray); font-size: 0.9rem;">Chủ tài khoản</span>
                                            <span style="font-weight: 700; color: var(--text-dark); font-size: 0.95rem;">CÔNG TY TNHH NAVATEK</span>
                                        </div>
                                        
                                        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); padding-bottom: 8px;">
                                            <span style="color: var(--text-gray); font-size: 0.9rem;">Số tài khoản</span>
                                            <div style="display: flex; align-items: center; gap: 8px;">
                                                <span id="bank-acc-no" style="font-weight: 800; color: var(--primary); font-size: 1.1rem; letter-spacing: 0.5px;">123434688</span>
                                                <button type="button" onclick="copyToClipboard('bank-acc-no', this)" style="background: var(--bg-white); border: 1px solid var(--border-color); border-radius: 6px; padding: 4px 10px; font-size: 0.8rem; cursor: pointer; display: inline-flex; align-items: center; gap: 4px; font-weight: 700; color: var(--text-dark); transition: all 0.2s;" onmouseover="this.style.borderColor='var(--primary)';" onmouseout="this.style.borderColor='var(--border-color)';">
                                                    <i class="ph-bold ph-copy"></i> Copy
                                                </button>
                                            </div>
                                        </div>
                                        
                                        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); padding-bottom: 8px;">
                                            <span style="color: var(--text-gray); font-size: 0.9rem;">Số tiền</span>
                                            <span id="bank-amount" style="font-weight: 800; color: var(--text-dark); font-size: 1rem;">35.323.200đ</span>
                                        </div>
                                        
                                        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); padding-bottom: 8px;">
                                            <span style="color: var(--text-gray); font-size: 0.9rem;">Nội dung CK</span>
                                            <div style="display: flex; align-items: center; gap: 8px;">
                                                <span id="bank-ck-content" style="font-weight: 800; color: var(--primary); font-size: 1.05rem; letter-spacing: 0.5px;">DH NAVA 8527</span>
                                                <button type="button" onclick="copyToClipboard('bank-ck-content', this)" style="background: var(--bg-white); border: 1px solid var(--border-color); border-radius: 6px; padding: 4px 10px; font-size: 0.8rem; cursor: pointer; display: inline-flex; align-items: center; gap: 4px; font-weight: 700; color: var(--text-dark); transition: all 0.2s;" onmouseover="this.style.borderColor='var(--primary)';" onmouseout="this.style.borderColor='var(--border-color)';">
                                                    <i class="ph-bold ph-copy"></i> Copy
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <img id="checkout-qr-img" src="https://qr.sepay.vn/img?acc=123434688&bank=ACB&amount=35323200&des=DH%%20NAVA%%208527" alt="QR Code" style="width: 140px; height: 140px; object-fit: contain; border-radius: 8px; border: 1px solid var(--border-color); display: block; margin: 0 auto; background: white; padding: 5px;">
                                    <p style="font-size: 0.8rem; color: var(--text-gray); margin: 15px 0 0 0; text-align: center;"><i class="ph-bold ph-qr-code"></i> Quét mã QR bằng ứng dụng ngân hàng để tự duyệt đơn tự động</p>
                                </div>
                            </div>
                        </div>
                        
                        <div class="payment-method-wrapper" style="margin: 0; border-bottom: 1px solid var(--border-color);">
                            <label class="radio-option" style="border: none; border-radius: 0; margin: 0; background: transparent; padding: 15px;">
                                <input type="radio" name="payment" value="momo">
                                <div>
                                    <span class="radio-label">Thanh toán qua MoMo</span>
                                </div>
                                <img src="https://upload.wikimedia.org/wikipedia/vi/f/fe/MoMo_Logo.png" alt="MoMo" style="max-height: 24px; margin-left: auto; border-radius: 4px;">
                            </label>
                        </div>
    
                        <div class="payment-method-wrapper" style="margin: 0; border-bottom: 1px solid var(--border-color);">
                            <label class="radio-option" style="border: none; border-radius: 0; margin: 0; background: transparent; padding: 15px;">
                                <input type="radio" name="payment" value="vnpay">
                                <div>
                                    <span class="radio-label">Thanh toán qua VNPAY</span>
                                </div>
                                <img src="https://vnpay.vn/s1/statics.vnpay.vn/2023/9/06ncktiwd6dc1694418189687.png" alt="VNPAY" style="max-height: 20px; margin-left: auto;">
                            </label>
                        </div>
    
                        <div class="payment-method-wrapper" style="margin: 0; border-bottom: 1px solid var(--border-color);">
                            <label class="radio-option" style="border: none; border-radius: 0; margin: 0; background: transparent; padding: 15px;">
                                <input type="radio" name="payment" value="zalopay">
                                <div>
                                    <span class="radio-label">Thanh toán qua ZaloPay</span>
                                </div>
                                <img src="https://cdn.haitrieu.com/wp-content/uploads/2022/10/Logo-ZaloPay-Square.png" alt="ZaloPay" style="max-height: 24px; margin-left: auto; border-radius: 4px;">
                            </label>
                        </div>
    
                        <div class="payment-method-wrapper" style="margin: 0;">
                            <label class="radio-option" style="border: none; border-radius: 0; margin: 0; background: transparent; padding: 15px;">
                                <input type="radio" name="payment" value="cod">
                                <div>
                                    <span class="radio-label">Thu hộ (COD)</span>
                                </div>
                                <i class="ph-fill ph-money" style="font-size: 1.5rem; color: #10b981; margin-left: auto;"></i>
                            </label>
                            <div class="payment-details" id="cod-details" style="display: none; padding: 0 15px 15px 15px; margin: 0;">
                                <p style="font-size: 0.9rem; color: var(--text-gray); background: #f8fafc; padding: 15px; border-radius: 8px; border: 1px solid var(--border-color); margin: 5px 0 0 0;">Khách hàng thanh toán bằng tiền mặt cho nhân viên giao hàng khi nhận được sản phẩm.</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="checkout-footer-links" style="display: flex; gap: 20px; font-size: 0.85rem; padding: 20px 0; border-top: 1px solid var(--border-color); margin-top: 40px; flex-wrap: wrap;">
                    <a href="demo_policy.html#return" style="color: var(--primary); text-decoration: none; font-weight: 500;">Chính sách hoàn trả</a>
                    <a href="demo_policy.html#privacy" style="color: var(--primary); text-decoration: none; font-weight: 500;">Chính sách bảo mật</a>
                    <a href="demo_policy.html#terms" style="color: var(--primary); text-decoration: none; font-weight: 500;">Điều khoản sử dụng</a>
                </div>
            </div>
            
            <!-- Right: Order Summary -->
            <div style="position: sticky; top: 30px; display: flex; flex-direction: column; gap: 30px; height: fit-content;">
                <!-- Shipping Methods -->
                <div class="checkout-card" style="margin-bottom: 0;">
                    <h2 class="section-title" style="font-size: 1.2rem; margin-bottom: 20px;"><i class="ph-fill ph-truck"></i> Vận chuyển</h2>
                    <div style="border: 1px solid var(--border-color); border-radius: var(--radius-md); background: var(--bg-white); overflow: hidden;">
                        <label class="radio-option" style="border: none; border-bottom: 1px solid var(--border-color); border-radius: 0; padding: 15px; margin: 0; background: transparent;">
                            <input type="radio" name="shipping" value="freeship">
                            <div style="flex: 1; display: flex; justify-content: space-between; align-items: center;">
                                <span class="radio-label" style="font-weight: 500;">NAVA - Chuyển phát nhanh</span>
                                <span style="font-weight: 700; color: var(--primary);">FREESHIP</span>
                            </div>
                        </label>
                        <label class="radio-option" id="hoatoc-shipping-option" style="border: none; border-radius: 0; padding: 15px; margin: 0; background: transparent;">
                            <input type="radio" name="shipping" value="hoatoc" checked>
                            <div style="flex: 1; display: flex; justify-content: space-between; align-items: center;">
                                <span class="radio-label" style="font-weight: 500;">Hoả Tốc (HCM)</span>
                                <span style="font-weight: 700;">39.000đ</span>
                            </div>
                        </label>
                    </div>
                </div>

                <div class="order-summary" style="margin-bottom: 0; top: 0; position: relative;">
                    <h2 class="section-title" style="font-size: 1.2rem; margin-bottom: 20px;"><i class="ph-fill ph-receipt"></i> Tóm Tắt Đơn Hàng</h2>
                    
                    <div class="order-items-list">
                        <!-- Item 1 -->
                        <div class="order-item" id="checkout-item-1">
                            <div class="item-img-wrap">
                                <span class="item-badge">1</span>
                                <img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" alt="ASUS NUC 14" class="item-img">
                            </div>
                            <div class="item-info">
                                <h4 class="item-title">ASUS NUC 14 Essential</h4>
                                <span class="item-var">Core i3 / 8GB / 256GB</span>
                            </div>
                            <div class="item-price">4.490.000đ</div>
                        </div>
                        
                        <!-- Item 2 -->
                        <div class="order-item" id="checkout-item-2">
                            <div class="item-img-wrap">
                                <span class="item-badge">1</span>
                                <img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_1.png" alt="GMK EVO X1" class="item-img">
                            </div>
                            <div class="item-info">
                                <h4 class="item-title">GMK EVO X1 32G</h4>
                                <span class="item-var">Ryzen AI 9 HX370 / 32GB / 1TB</span>
                            </div>
                            <div class="item-price">31.190.000đ</div>
                        </div>
                    </div>
                    
                    <div class="summary-details" style="margin-top: 30px;">
                        <div class="summary-line">
                            <span>Tạm tính</span>
                            <span style="color: var(--text-dark); font-weight: 600;">35.680.000đ</span>
                        </div>
                        <div class="summary-line">
                            <span>Phí vận chuyển</span>
                            <span id="summary-shipping-fee" style="color: #10b981; font-weight: 600;">Miễn phí</span>
                        </div>
                        <div class="summary-line" id="checkout-discount-row">
                            <span>Giảm giá</span>
                            <span id="checkout-discount-val" style="color: var(--text-dark); font-weight: 600;">0đ</span>
                        </div>
                    </div>
                    
                    <div class="summary-total">
                        <div class="summary-total-label">Tổng thanh toán</div>
                        <div class="summary-total-val" id="summary-total">35.680.000đ</div>
                    </div>
                    
                    <!-- 15-DAY RETURN ASSURANCE BANNER -->
                    <div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin-top: 20px; padding: 12px; background: rgba(16, 185, 129, 0.08); border-radius: 8px; color: #065f46; font-weight: 700; font-size: 0.88rem; border: 1px solid rgba(16, 185, 129, 0.2);">
                        <i class="ph-fill ph-arrow-counter-clockwise" style="font-size: 1.1rem;"></i>
                        <span>Đổi trả hàng trong vòng 15 ngày</span>
                    </div>
                    
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 30px;">
                        <a href="demo_cart.html" style="color: var(--primary); text-decoration: none; font-weight: 600; font-size: 0.95rem; display: flex; align-items: center; gap: 5px; transition: 0.2s;"><i class="ph-bold ph-caret-left"></i> Quay lại giỏ hàng</a>
                        <button class="btn-pay" style="width: auto; margin-top: 0; padding: 14px 30px;" onclick="validateAndOrder()">ĐẶT HÀNG</button>
                    </div>
                </div>
            </div>
            
        </div>
    </div>

    <!-- Mobile Sticky Bottom Bar -->
    <div class="mobile-sticky-bar">
        <div>
            <div class="sticky-price-label">Tổng thanh toán</div>
            <div class="sticky-price-val" id="sticky-total-price">35.323.200đ</div>
        </div>
        <button class="btn-sticky-pay" onclick="validateAndOrder()">THANH TOÁN</button>
    </div>

    <!-- Address Modal -->
    <div id="address-modal" class="address-modal-overlay" onclick="closeAddressModal()" style="display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(15,23,42,0.5); z-index: 999999; align-items: center; justify-content: center; backdrop-filter: blur(6px); opacity: 1; visibility: visible;">
        <div class="modal-content" onclick="event.stopPropagation()" style="background: #fff; width: 100%; max-width: 460px; border-radius: 24px; overflow: hidden; display: flex; flex-direction: column; max-height: 80vh; box-shadow: 0 25px 60px -12px rgba(0,0,0,0.25); margin: 20px; z-index: 1000000; position: relative; opacity: 1; visibility: visible;">
            <div class="modal-header">
                <h3 id="modal-title">Chọn Tỉnh / Thành phố</h3>
                <button id="close-modal" class="btn-close" onclick="closeAddressModal()"><i class="ph-bold ph-x"></i></button>
            </div>
            <div class="modal-search">
                <input type="text" id="address-search" class="nava-input" placeholder="Tìm kiếm..." style="background: var(--bg-white);">
            </div>
            <div class="modal-body" id="address-list">
                <!-- JS populated -->
            </div>
            <div class="modal-footer" id="modal-footer" style="display: none;">
                <button id="modal-back" class="btn secondary sm" onclick="goBackAddressStep()" style="display: flex; align-items: center; gap: 6px; background: var(--bg-gray); border: 1px solid var(--border-color); padding: 8px 16px; border-radius: 8px; font-weight: 600; cursor: pointer; color: var(--text-dark);"><i class="ph-bold ph-arrow-left"></i> Quay lại</button>
            </div>
        </div>
    </div>

    <script>
        function validateAndOrder() {
            const fullname = document.getElementById('checkout-fullname').value.trim();
            const phone = document.getElementById('checkout-phone').value.trim();
            const streetInput = document.getElementById('street-address-input');
            const streetVal = streetInput ? streetInput.value.trim() : '';
            const addressDisplay = document.getElementById('address-display').textContent.trim();
            
            if (!fullname) {
                alert('Vui lòng nhập Họ và tên');
                document.getElementById('checkout-fullname').focus();
                return;
            }
            if (!phone) {
                alert('Vui lòng nhập Số điện thoại');
                document.getElementById('checkout-phone').focus();
                return;
            }
            if (!streetVal) {
                alert('Vui lòng nhập Số nhà, tên đường');
                if (streetInput) {
                    streetInput.focus();
                }
                return;
            }
            
            alert('Đặt hàng thành công!');
        }

        // Copy to clipboard function with premium feedback
        function copyToClipboard(elementId, btn) {
            const el = document.getElementById(elementId);
            if (!el) return;
            let text = el.innerText || el.textContent;
            if (elementId === 'bank-amount') {
                text = text.replace(/[^0-9]/g, '');
            }
            navigator.clipboard.writeText(text).then(() => {
                const originalHTML = btn.innerHTML;
                btn.innerHTML = '<i class="ph-bold ph-check" style="color: #10b981;"></i> Đã copy';
                btn.style.borderColor = '#10b981';
                btn.style.color = '#10b981';
                setTimeout(() => {
                    btn.innerHTML = originalHTML;
                    btn.style.borderColor = '';
                    btn.style.color = '';
                }, 1500);
            }).catch(err => {
                console.error('Lỗi sao chép: ', err);
            });
        }

        // --- Address Modal Logic (Global) ---
        let cityData = { cities: [], wards: [] };
        let addressStep = 1; 
        let selectedCity = null;
        let selectedWard = null;
        let fetchError = false;

        fetch('assets/ctiy.json')
            .then(r => r.json())
            .then(data => { cityData = data; })
            .catch(err => { console.error("Lỗi tải json", err); fetchError = true; });

        function getCleanCityName(name) {
            const match = name.match(/\\[(.*?)\\]/);
            return match ? match[1] : name.replace(/\\s*\\(.*?\\)\\s*/g, '').trim();
        }

        function openAddressModal() {
            const modal = document.getElementById("address-modal");
            if (modal && modal.parentNode !== document.body) { document.body.appendChild(modal); }
            console.log("--> openAddressModal() called");
            addressStep = 1;
            selectedCity = null;
            selectedWard = null;
            const searchInput = document.getElementById('address-search');
            if(searchInput) searchInput.value = '';
            renderAddressList();
            if(modal) {
                console.log("Setting modal display to flex");
                modal.style.display = 'flex';
                modal.style.position = 'fixed';
                modal.style.top = '0';
                modal.style.left = '0';
                modal.style.width = '100vw';
                modal.style.height = '100vh';
                modal.style.zIndex = '999999';
                modal.style.opacity = '1';
                modal.style.visibility = 'visible';
            } else {
                console.error("Modal element not found!");
            }
        }

        function closeAddressModal() {
            const modal = document.getElementById('address-modal');
            if(modal) modal.style.display = 'none';
        }

        function goBackAddressStep() {
            if (addressStep === 3) { addressStep = 2; document.querySelector(".modal-search").style.display = "block"; renderAddressList(); } else if (addressStep === 2) {
                addressStep = 1;
                selectedCity = null;
                const searchInput = document.getElementById('address-search');
                if(searchInput) searchInput.value = '';
                renderAddressList();
            }
        }

        function triggerShippingUpdate() {
            if(window.updateShippingStateGlobal) {
                window.updateShippingStateGlobal();
            }
        }

        function confirmAddress() {
            const street = document.getElementById('street-input').value;
            if(!street) { alert('Vui lòng nhập số nhà & đường'); return; }
            const fullAddress = street + ', ' + selectedWard.wnew + ', ' + getCleanCityName(selectedCity.name);
            document.getElementById('address-display').textContent = fullAddress;
            document.getElementById('address-display').style.color = 'var(--text-dark)';
            closeAddressModal();
        }
    
        function renderAddressList() {
            const searchInput = document.getElementById('address-search');
            const listEl = document.getElementById('address-list');
            const displayEl = document.getElementById('address-display');
            const provinceSelectHidden = document.getElementById('province-select');
            const hoatocShipping = document.getElementById('hoatoc-shipping-option');
            
            const query = searchInput ? searchInput.value.toLowerCase() : '';
            if(listEl) listEl.innerHTML = '';
            
            document.getElementById('modal-title').textContent = addressStep === 1 ? 'Chọn Tỉnh / Thành phố' : 'Chọn Quận / Huyện / Xã';
            document.getElementById('modal-footer').style.display = addressStep === 2 ? 'flex' : 'none';
            
            if (fetchError) {
                if(listEl) listEl.innerHTML = '<div style="padding: 30px; text-align: center; color: red;">Lỗi tải dữ liệu. Vui lòng mở bằng Live Server.</div>';
                return;
            }

            if (addressStep === 1) {
                const filtered = cityData.cities.filter(c => c.name.toLowerCase().includes(query) || getCleanCityName(c.name).toLowerCase().includes(query));
                if (filtered.length === 0) listEl.innerHTML = '<div style="padding: 20px; text-align: center; color: var(--text-gray);">Không tìm thấy</div>';
                filtered.forEach(c => {
                    const div = document.createElement('div');
                    div.className = 'list-item';
                    div.innerHTML = `<span>${getCleanCityName(c.name)}</span> <i class="ph-bold ph-caret-right" style="color:var(--text-gray)"></i>`;
                    div.onclick = (e) => {
                        e.stopPropagation();
                        selectedCity = c;
                        addressStep = 2;
                        if(searchInput) searchInput.value = '';
                        renderAddressList();
                    };
                    if(listEl) listEl.appendChild(div);
                });
            } else if (addressStep === 3) { addressStep = 2; document.querySelector(".modal-search").style.display = "block"; renderAddressList(); } else if (addressStep === 2) {
                const cleanName = getCleanCityName(selectedCity.name);
                let wards = cityData.wards.filter(w => w.city === cleanName);
                if (query) {
                    wards = wards.filter(w => w.wnew.toLowerCase().includes(query) || (w.wold && w.wold.toLowerCase().includes(query)));
                }
                if (wards.length === 0) listEl.innerHTML = '<div style="padding: 20px; text-align: center; color: var(--text-gray);">Không có dữ liệu</div>';
                wards.forEach(w => {
                    const div = document.createElement('div');
                    div.className = 'list-item';
                    div.innerHTML = `<div><span>${w.wnew}</span>${w.wold && w.wold !== w.wnew ? `<div class="list-item-sub">(Cũ: ${w.wold})</div>` : ''}</div> <i class="ph-bold ph-check" style="color:transparent"></i>`;
                    div.onclick = (e) => {
                        e.stopPropagation();
                        selectedWard = w;
                        if(displayEl) {
                            displayEl.textContent = `${w.wnew}, ${cleanName}`;
                            displayEl.style.color = 'var(--text-dark)';
                        }
                        
                        const streetInput = document.getElementById('street-address-input');
                        if (streetInput) {
                            streetInput.style.display = 'block';
                            streetInput.value = '';
                            setTimeout(() => { streetInput.focus(); }, 150);
                        }
                        
                        if (cleanName.includes("Hà Nội") || cleanName.includes("Hồ Chí Minh") || cleanName.includes("HCM")) {
                            if(provinceSelectHidden) provinceSelectHidden.value = 'HCM';
                            if (hoatocShipping) hoatocShipping.style.display = 'flex';
                        } else {
                            if(provinceSelectHidden) provinceSelectHidden.value = cleanName;
                            if (hoatocShipping) hoatocShipping.style.display = 'none';
                            const freeShip = document.querySelector('input[name="shipping"][value="freeship"]');
                            if(freeShip) freeShip.checked = true;
                            triggerShippingUpdate();
                        }
                        
                        closeAddressModal();
                    };
                    if(listEl) listEl.appendChild(div);
                });
            }
        }

        document.addEventListener("DOMContentLoaded", function() {
            const searchInput = document.getElementById('address-search');
            if(searchInput) searchInput.addEventListener('input', renderAddressList);
            const paymentRadios = document.querySelectorAll('input[name="payment"]');
            const shippingRadios = document.querySelectorAll('input[name="shipping"]');
            
            // Recalculation logic using dynamic discount and quantities from localStorage
            const qty1 = localStorage.getItem('nava_qty_item1') !== null ? parseInt(localStorage.getItem('nava_qty_item1')) : 1;
            const qty2 = localStorage.getItem('nava_qty_item2') !== null ? parseInt(localStorage.getItem('nava_qty_item2')) : 1;
            
            // Update Item 1 UI
            const orderItem1 = document.getElementById('checkout-item-1');
            if (orderItem1) {
                if (qty1 > 0) {
                    orderItem1.querySelector('.item-badge').textContent = qty1;
                    orderItem1.querySelector('.item-price').textContent = (qty1 * 4490000).toLocaleString('vi-VN') + 'đ';
                    orderItem1.style.display = 'flex';
                } else {
                    orderItem1.style.display = 'none';
                }
            }
            
            // Update Item 2 UI
            const orderItem2 = document.getElementById('checkout-item-2');
            if (orderItem2) {
                if (qty2 > 0) {
                    orderItem2.querySelector('.item-badge').textContent = qty2;
                    orderItem2.querySelector('.item-price').textContent = (qty2 * 31190000).toLocaleString('vi-VN') + 'đ';
                    orderItem2.style.display = 'flex';
                } else {
                    orderItem2.style.display = 'none';
                }
            }
            
            const subtotal = (qty1 * 4490000) + (qty2 * 31190000);
            
            // Update Tạm tính in summary details
            const summarySubtotalEl = document.querySelector('.summary-details .summary-line:first-child span:last-child');
            if (summarySubtotalEl) {
                summarySubtotalEl.textContent = subtotal.toLocaleString('vi-VN') + 'đ';
            }
            
            let discountPercent = parseFloat(localStorage.getItem('nava_discount_percent')) || 1;
            let discountVal = Math.round(subtotal * (discountPercent / 100));
            let discountCode = localStorage.getItem('nava_discount_code') || 'NAVAVIP';
            
            function updatePaymentState() {
                paymentRadios.forEach(r => r.closest('.radio-option').classList.remove('active'));
                document.querySelectorAll('.payment-details').forEach(el => el.style.display = 'none');
                
                const checkedPayment = document.querySelector('input[name="payment"]:checked');
                if (checkedPayment) {
                    checkedPayment.closest('.radio-option').classList.add('active');
                    if (checkedPayment.value === 'bank') {
                        document.getElementById('bank-details').style.display = 'block';
                    } else if (checkedPayment.value === 'cod') {
                        document.getElementById('cod-details').style.display = 'block';
                    }
                }
            }
            
            function updateShippingState() {
                shippingRadios.forEach(r => r.closest('.radio-option').classList.remove('active'));
                const checkedShipping = document.querySelector('input[name="shipping"]:checked');
                
                let shippingFee = 0;
                if (checkedShipping) {
                    checkedShipping.closest('.radio-option').classList.add('active');
                    if (checkedShipping.value === 'hoatoc') {
                        shippingFee = 39000;
                    }
                }
                
                const shippingFeeEl = document.getElementById('summary-shipping-fee');
                const totalEl = document.getElementById('summary-total');
                const stickyTotalEl = document.getElementById('sticky-total-price');
                const discountValEl = document.getElementById('checkout-discount-val');
                const discountRowEl = document.getElementById('checkout-discount-row');
                
                // Update discount display
                if (discountValEl) {
                    if (discountVal > 0) {
                        discountValEl.textContent = '-' + discountVal.toLocaleString('vi-VN') + 'đ';
                        discountValEl.style.color = 'var(--primary)';
                        discountValEl.style.fontWeight = '700';
                        if (discountRowEl) {
                            discountRowEl.querySelector('span:first-child').innerHTML = `Giảm giá <span style="background:var(--primary);color:white;font-size:0.75rem;font-weight:800;padding:2px 6px;border-radius:3px;margin-left:5px;">${discountCode}</span>`;
                        }
                    } else {
                        discountValEl.textContent = '0đ';
                        discountValEl.style.color = '';
                        discountValEl.style.fontWeight = '';
                    }
                }
                
                if (shippingFeeEl && totalEl) {
                    if (shippingFee === 0) {
                        shippingFeeEl.textContent = 'Miễn phí';
                        shippingFeeEl.style.color = '#10b981';
                    } else {
                        shippingFeeEl.textContent = shippingFee.toLocaleString('vi-VN') + 'đ';
                        shippingFeeEl.style.color = 'var(--text-dark)';
                    }
                    const total = subtotal - discountVal + shippingFee;
                    const formattedTotal = total.toLocaleString('vi-VN') + 'đ';
                    totalEl.textContent = formattedTotal;
                    if (stickyTotalEl) stickyTotalEl.textContent = formattedTotal;
                    
                    // Update bank amount & QR code
                    const bankAmountEl = document.getElementById('bank-amount');
                    const bankCkContentEl = document.getElementById('bank-ck-content');
                    const qrImgEl = document.getElementById('checkout-qr-img');
                    
                    if (bankAmountEl) bankAmountEl.textContent = formattedTotal;
                    
                    const ckContent = (bankCkContentEl ? bankCkContentEl.textContent : 'DH NAVA 8527').toUpperCase();
                    if (qrImgEl) {
                        qrImgEl.src = `https://qr.sepay.vn/img?acc=123434688&bank=ACB&amount=${total}&des=${encodeURIComponent(ckContent)}`;
                    }
                }
            }
            
            // Dynamic Auto-banking description update based on phone number input
            const phoneInput = document.getElementById('checkout-phone');
            const bankCkContentEl = document.getElementById('bank-ck-content');
            
            function updateCKContentText() {
                const phoneVal = (phoneInput ? phoneInput.value.trim() : '0972178527') || '0972178527';
                const last4Digits = phoneVal.length >= 4 ? phoneVal.slice(-4) : phoneVal;
                const ckContent = `DH NAVA ${last4Digits}`.toUpperCase();
                if (bankCkContentEl) bankCkContentEl.textContent = ckContent;
                updateShippingState();
            }
            
            if (phoneInput) {
                phoneInput.addEventListener('input', updateCKContentText);
            }
            
            window.updateShippingStateGlobal = updateShippingState;
            
            paymentRadios.forEach(radio => radio.addEventListener('change', updatePaymentState));
            shippingRadios.forEach(radio => radio.addEventListener('change', updateShippingState));
 
            updatePaymentState();
            updateShippingState();
            updateCKContentText();
        });
    </script>
</body>
</html>
"""
    with open(os.path.join(base_dir, "demo_checkout.html"), "w", encoding="utf-8") as f:
        f.write(checkout_html)

def build_policy_pages(base_dir, header_part, footer_part):
    sticky_stuff = ""
    with open(os.path.join(base_dir, "index.bwt"), "r", encoding="utf-8") as f:
        idx_content = f.read()
        if "<!-- Mobile Sidebar Drawer -->" in idx_content:
            sticky_stuff = idx_content[idx_content.find("<!-- Mobile Sidebar Drawer -->"):]
            if "<!-- /MASTER SAPO ESCAPE WRAPPER -->" in sticky_stuff:
                sticky_stuff = sticky_stuff.split("<!-- /MASTER SAPO ESCAPE WRAPPER -->")[0]
                
    local_footer_part = sticky_stuff + '<script src="assets/main.js" defer></script>\n' + footer_part

    policy_html = """
        <style>
            .nava-policy-page { max-width: 1200px; margin: 60px auto 30px; padding: 20px 15px; }
            .policy-hero { text-align: center; margin-bottom: 25px; padding: 25px 20px; background: linear-gradient(135deg, rgba(0, 51, 102, 0.08), rgba(0, 76, 153, 0.03)); border-radius: var(--radius-md); border: 1px solid rgba(0, 51, 102, 0.15); }
            .policy-hero h1 { font-size: 1.8rem; font-weight: 800; color: var(--text-dark); margin: 0 0 6px 0; }
            .policy-hero p { color: var(--text-gray); font-size: 0.95rem; margin: 0; }
            
            .policy-grid { display: grid; grid-template-columns: 240px 1fr; gap: 20px; }
            
            .policy-sidebar { position: sticky; top: 80px; background: var(--bg-white); border-radius: var(--radius-md); padding: 15px; box-shadow: var(--shadow-sm); border: 1px solid var(--border-color); height: fit-content; }
            .policy-sidebar h3 { font-size: 1.05rem; font-weight: 800; color: var(--text-dark); margin: 0 0 15px 0; padding-bottom: 10px; border-bottom: 1px solid var(--border-color); }
            .policy-menu { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 8px; }
            .policy-menu-link { display: flex; align-items: center; gap: 10px; padding: 12px 15px; color: var(--text-gray); text-decoration: none; border-radius: var(--radius-md); font-weight: 600; font-size: 0.92rem; transition: all 0.2s; border: 1px solid transparent; white-space: nowrap; }
            .policy-menu-link:hover { background: var(--bg-gray); color: var(--text-dark); }
            .policy-menu-link.active { background: rgba(0, 51, 102, 0.05); color: var(--primary); border-color: rgba(0, 51, 102, 0.15); }
            
            .policy-content { background: var(--bg-white); border-radius: var(--radius-md); padding: 30px; box-shadow: var(--shadow-sm); border: 1px solid var(--border-color); min-height: 400px; }
            
            .policy-tab-content { display: none; }
            .policy-tab-content.active { display: block; animation: fadeIn 0.3s ease-out; }
            @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
            
            .policy-tab-content h2 { font-size: 1.4rem; font-weight: 800; color: var(--text-dark); margin: 0 0 20px 0; border-bottom: 1px solid var(--border-color); padding-bottom: 10px; }
            .policy-tab-content h3 { font-size: 1.1rem; font-weight: 700; color: var(--text-dark); margin: 25px 0 12px 0; }
            .policy-tab-content p { color: var(--text-gray); line-height: 1.6; font-size: 0.95rem; margin-bottom: 15px; }
            .policy-tab-content ul { padding-left: 20px; color: var(--text-gray); font-size: 0.95rem; line-height: 1.6; margin-bottom: 20px; }
            .policy-tab-content li { margin-bottom: 8px; }
            
            .warranty-block { border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 15px 20px; margin-bottom: 20px; background: var(--bg-gray); }
            .warranty-block h3 { margin-top: 0 !important; }
            .note-block { background: rgba(59, 130, 246, 0.05); border-color: rgba(59, 130, 246, 0.2); color: #1e3a8a; }
            
            @media (max-width: 768px) {
                .policy-grid { grid-template-columns: 1fr; gap: 15px; }
                .policy-sidebar {
                    position: sticky;
                    top: 60px;
                    z-index: 10;
                    background: var(--bg-white);
                    padding: 10px !important;
                    margin: 0 -15px 10px;
                    border-radius: 0;
                    border-left: none;
                    border-right: none;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
                    width: calc(100% + 30px);
                    box-sizing: border-box;
                    overflow: hidden;
                }
                .policy-sidebar h3 { display: none !important; }
                .policy-menu {
                    flex-direction: row !important;
                    overflow-x: auto;
                    -webkit-overflow-scrolling: touch;
                    gap: 8px;
                    padding-bottom: 5px;
                    scrollbar-width: none;
                    width: 100%;
                }
                .policy-menu::-webkit-scrollbar { display: none; }
                .policy-menu li { margin: 0; }
                .policy-menu-link {
                    padding: 8px 14px !important;
                    font-size: 0.85rem !important;
                }
                
                .policy-content { padding: 20px 15px !important; }
                .policy-hero h1 { font-size: 1.4rem; }
                .policy-hero { padding: 15px 10px !important; }
                .policy-tab-content h2 { font-size: 1.2rem !important; }
            }
        </style>
        
        <div class="nava-policy-page">
            <div class="breadcrumb" style="background: transparent; padding: 0; margin-bottom: 20px;">
                <a href="/" style="color: var(--text-gray); text-decoration: none;"><i class="ph ph-house"></i> Trang chủ</a> 
                <span style="margin: 0 10px; color: var(--text-gray);">/</span> 
                <span style="color: var(--primary); font-weight: bold;">Chính sách & Điều khoản</span>
            </div>
            
            <div class="policy-hero">
                <h1>Chính Sách & Điều Khoản</h1>
                <p>Thông tin chi tiết về các chính sách bán hàng, bảo hành và bảo mật tại Nava Store</p>
            </div>
            
            <div class="policy-grid">
                <!-- Sidebar -->
                <div class="policy-sidebar">
                    <h3>Danh mục chính sách</h3>
                    <ul class="policy-menu">
                        <li><a href="#warranty" onclick="switchPolicyTab('warranty'); return false;" id="tab-btn-warranty" class="policy-menu-link active"><i class="ph-bold ph-shield-check"></i> Chính sách bảo hành</a></li>
                        <li><a href="#shipping" onclick="switchPolicyTab('shipping'); return false;" id="tab-btn-shipping" class="policy-menu-link"><i class="ph-bold ph-truck"></i> Chính sách vận chuyển</a></li>
                        <li><a href="#return" onclick="switchPolicyTab('return'); return false;" id="tab-btn-return" class="policy-menu-link"><i class="ph-bold ph-arrow-counter-clockwise"></i> Chính sách hoàn trả</a></li>
                        <li><a href="#privacy" onclick="switchPolicyTab('privacy'); return false;" id="tab-btn-privacy" class="policy-menu-link"><i class="ph-bold ph-lock-key"></i> Chính sách bảo mật</a></li>
                        <li><a href="#terms" onclick="switchPolicyTab('terms'); return false;" id="tab-btn-terms" class="policy-menu-link"><i class="ph-bold ph-file-text"></i> Điều khoản dịch vụ</a></li>
                    </ul>
                </div>
                
                <!-- Content Column with CTA -->
                <div style="display: flex; flex-direction: column; gap: 25px; min-width: 0;">
                    <div class="policy-content" id="policy-main-content" style="margin-bottom: 0;">
                        <!-- Tab 1: Warranty -->
                        <div class="policy-tab-content active" id="policy-tab-warranty">
                            <h2>Chính Sách Bảo Hành</h2>
                            <p>Nava Store cam kết mang đến chính sách bảo hành tối ưu nhất cho quý khách hàng đối với tất cả các dòng sản phẩm Mini PC, eGPU và linh kiện công nghệ bán ra.</p>
                            
                            <div class="warranty-block warranty-eligible">
                                <h3><i class="ph-fill ph-check-circle" style="color: #10b981;"></i> Điều Kiện Được Bảo Hành:</h3>
                                <ul>
                                    <li>Sản phẩm được bán ra bởi Nava Store và có tem bảo hành của Nava Store hoặc tem bảo hành từ nhà cung cấp/sản xuất (còn nguyên vẹn).</li>
                                    <li>Sản phẩm trong thời hạn bảo hành hợp lệ, đầy đủ phụ kiện và bao bì theo yêu cầu.</li>
                                    <li>Sản phẩm lỗi do kỹ thuật hoặc từ nhà sản xuất, được xác định bởi Nava Store hoặc nhà phân phối.</li>
                                </ul>
                            </div>
                            
                            <div class="warranty-block warranty-ineligible">
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
                                <p>- Nếu sản phẩm lỗi trong vòng 15 ngày đầu, quý khách sẽ được đổi sản phẩm mới cùng model.</p>
                                <p>- Thời gian bảo hành thông thường là từ 7 đến 15 ngày làm việc tùy thuộc vào linh kiện lỗi cần xử lý.</p>
                            </div>
                        </div>
                        
                        <!-- Tab 2: Shipping -->
                        <div class="policy-tab-content" id="policy-tab-shipping">
                            <h2>Chính Sách Vận Chuyển</h2>
                            <p>Chúng tôi cung cấp dịch vụ giao hàng toàn quốc nhanh chóng và an toàn tuyệt đối với mọi đơn hàng.</p>
                            
                            <h3>1. Thời gian giao hàng dự kiến:</h3>
                            <ul>
                                <li><strong>Khu vực nội thành TP.HCM:</strong> Giao nhanh trong vòng 2-4 giờ (với tùy chọn Hoả Tốc) hoặc trong vòng 24 giờ.</li>
                                <li><strong>Các tỉnh thành khác:</strong> Thời gian từ 2-4 ngày làm việc tuỳ thuộc địa chỉ của quý khách.</li>
                            </ul>
                            
                            <h3>2. Phí vận chuyển:</h3>
                            <ul>
                                <li>Miễn phí vận chuyển Standard (Freeship) cho mọi đơn hàng Mini PC, eGPU trên toàn quốc.</li>
                                <li>Phí giao hàng hoả tốc áp dụng mức phí cố định 39.000đ cho khu vực TP.HCM.</li>
                            </ul>
                            
                            <h3>3. Đồng kiểm khi nhận hàng:</h3>
                            <p>Quý khách hàng được quyền mở gói hàng đồng kiểm ngoại quan cùng với nhân viên giao nhận. Vui lòng quay video clip khui hộp để đảm bảo quyền lợi đổi trả tối đa khi xảy ra sự cố nứt vỡ, móp méo sản phẩm do vận chuyển.</p>
                        </div>
                        
                        <!-- Tab 3: Return -->
                        <div class="policy-tab-content" id="policy-tab-return">
                            <h2>Chính Sách Hoàn Trả & Đổi Hàng</h2>
                            <p>Chính sách bảo vệ khách hàng vượt trội tại Nava Store cho phép đổi trả hàng trong vòng 15 ngày.</p>
                            
                            <h3>1. Thời hạn đổi trả hàng:</h3>
                            <p>Quý khách có thể yêu cầu đổi hàng hoặc hoàn trả tiền trong vòng tối đa 15 ngày kể từ ngày nhận hàng (xác nhận theo phiếu giao hàng hoặc hệ thống đơn vị vận chuyển).</p>
                            
                            <h3>2. Điều kiện đổi trả:</h3>
                            <ul>
                                <li>Sản phẩm lỗi kỹ thuật từ nhà sản xuất.</li>
                                <li>Sản phẩm giao không đúng loại, không đúng model, thiếu phụ kiện so với đơn hàng đã đặt.</li>
                                <li>Sản phẩm phải còn nguyên hộp, tem mác niêm phong ban đầu, không trầy xước cấn móp cọ xát và đầy đủ quà tặng đi kèm nếu có.</li>
                            </ul>
                            
                            <h3>3. Chi phí vận chuyển đổi trả:</h3>
                            <p>Nava Store sẽ chịu 100% chi phí vận chuyển phát sinh khi thực hiện đổi trả do lỗi kỹ thuật hoặc lỗi giao sai từ phía cửa hàng.</p>
                        </div>
                        
                        <!-- Tab 4: Privacy -->
                        <div class="policy-tab-content" id="policy-tab-privacy">
                            <h2>Chính Sách Bảo Mật</h2>
                            <p>Nava Store tôn trọng và cam kết bảo vệ thông tin riêng tư cá nhân của khách hàng khi truy cập và mua hàng tại hệ thống.</p>
                            
                            <h3>1. Thu thập thông tin:</h3>
                            <p>Chúng tôi chỉ thu thập thông tin cơ bản liên quan đến giao dịch đặt hàng gồm: Họ tên, Số điện thoại, Email và Địa chỉ giao nhận hàng.</p>
                            
                            <h3>2. Mục đích sử dụng:</h3>
                            <p>Thông tin thu thập chỉ được dùng để xác nhận đơn hàng, xử lý giao hàng, cung cấp dịch vụ bảo hành sửa chữa, và gửi thông báo chương trình khuyến mãi nếu được sự đồng ý của khách hàng.</p>
                            
                            <h3>3. Cam kết bảo mật:</h3>
                            <p>Thông tin của khách hàng được mã hoá và lưu trữ trên hệ thống an toàn. Chúng tôi tuyệt đối không bán, chia sẻ hay tiết lộ thông tin khách hàng cho bên thứ ba ngoại trừ đơn vị vận chuyển trung gian phục vụ giao nhận đơn hàng.</p>
                        </div>
                        
                        <!-- Tab 5: Terms -->
                        <div class="policy-tab-content" id="policy-tab-terms">
                            <h2>Điều Khoản Dịch Vụ</h2>
                            <p>Chào mừng bạn đến với trang web demo của Nava Store. Bằng cách truy cập và sử dụng dịch vụ tại đây, bạn đồng ý với các điều khoản dưới đây:</p>
                            
                            <h3>1. Bản quyền nội dung:</h3>
                            <p>Mọi hình ảnh, văn bản, thông số kỹ thuật sản phẩm và thiết kế giao diện trên website thuộc sở hữu độc quyền của Nava Store. Nghiêm cấm mọi hành vi sao chép trái phép.</p>
                            
                            <h3>2. Giá cả & Mô tả sản phẩm:</h3>
                            <p>Nava Store luôn cố gắng cung cấp thông tin giá cả chính xác nhất. Tuy nhiên, nếu có sai sót kỹ thuật hiển thị sai giá trị thực tế, chúng tôi có quyền từ chối hoặc hủy đơn hàng đó sau khi liên hệ giải thích với quý khách.</p>
                            
                            <h3>3. Trách nhiệm người dùng:</h3>
                            <p>Người dùng cam kết cung cấp thông tin liên hệ chính xác, trung thực khi thực hiện đặt mua hàng để đảm bảo quyền lợi vận chuyển và dịch vụ hậu mãi chăm sóc khách hàng tốt nhất.</p>
                        </div>
                    </div>
                    
                    <div style="text-align: center; margin-top: 5px;">
                        <a href="demo_collection.html" class="btn-nava btn-primary-nava" style="display: inline-flex; width: auto; padding: 14px 35px; text-decoration: none; border-radius: var(--radius-md); font-weight: 700; color: white; background: linear-gradient(90deg, var(--primary), var(--primary-light)); align-items: center; gap: 8px; box-shadow: 0 4px 15px rgba(0, 51, 102, 0.2);">
                            <i class="ph-bold ph-shopping-bag"></i> Tiếp tục mua sắm
                        </a>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            function switchPolicyTab(tabId) {
                // Hide all tab contents
                document.querySelectorAll('.policy-tab-content').forEach(el => el.classList.remove('active'));
                // Remove active class from all links
                document.querySelectorAll('.policy-menu-link').forEach(el => el.classList.remove('active'));
                
                // Show current tab & set active link
                const targetTab = document.getElementById('policy-tab-' + tabId);
                const targetLink = document.getElementById('tab-btn-' + tabId);
                if (targetTab) targetTab.classList.add('active');
                if (targetLink) targetLink.classList.add('active');
                
                // Update URL hash
                window.location.hash = tabId;
            }
            
            // Check hash on load
            window.addEventListener('DOMContentLoaded', () => {
                const hash = window.location.hash.replace('#', '');
                if (hash && ['warranty', 'shipping', 'return', 'privacy', 'terms'].includes(hash)) {
                    switchPolicyTab(hash);
                }
            });
        </script>
    """
    full_html = clean_liquid_tags(header_part + policy_html + local_footer_part, 'page')
    full_html = inject_seo_metadata(
        full_html,
        title="Chính Sách & Điều Khoản - Nava Store",
        description="Thông tin chi tiết về các chính sách bán hàng, bảo hành, hoàn tiền và bảo mật tại Nava Store.",
        keywords="chinh sach bao hanh, chinh sach van chuyen, dieu khoan dich vu, nava store"
    )
    with open(os.path.join(base_dir, "demo_policy.html"), "w", encoding="utf-8") as f:
        f.write(full_html)

def build_contact_page(base_dir, header_part, footer_part):
    sticky_stuff = ""
    with open(os.path.join(base_dir, "index.bwt"), "r", encoding="utf-8") as f:
        idx_content = f.read()
        if "<!-- Mobile Sidebar Drawer -->" in idx_content:
            sticky_stuff = idx_content[idx_content.find("<!-- Mobile Sidebar Drawer -->"):]
            if "<!-- /MASTER SAPO ESCAPE WRAPPER -->" in sticky_stuff:
                sticky_stuff = sticky_stuff.split("<!-- /MASTER SAPO ESCAPE WRAPPER -->")[0]
                
    local_footer_part = sticky_stuff + '<script src="assets/main.js" defer></script>\n' + footer_part

    # Load BWT template
    with open(os.path.join(base_dir, "sapo_BWT_new", "Templates", "page.contact.bwt"), "r", encoding="utf-8") as f:
        bwt_template = f.read()

    # Do compilation replacements
    compiled = bwt_template
    compiled = compiled.replace("{%- include 'breadcrumb' -%}", """
        <div class="breadcrumbs mt-3">
            <div class="container">
                <ul class="breadcrumb align-items-center m-0 pl-0 pr-0 small pt-2 pb-2" style="list-style: none; display: flex; gap: 8px; padding-left: 0;">					
                    <li class="home">
                        <a href="index.html" title="Trang chủ" style="text-decoration: none; color: var(--text-gray);"><i class="ph ph-house"></i> Trang chủ</a>
                        <span class="slash-divider ml-2 mr-2">/</span>
                    </li>
                    <li class="active" style="color: var(--primary); font-weight: 700;">Liên hệ</li>
                </ul>
            </div>
        </div>
    """)
    compiled = compiled.replace("{{page.title}}", "Liên hệ với NAVA STORE")
    
    # Replace dynamic contact info cards block
    info_block_start = compiled.find("{%- if settings.edit_contact_page == 'page_option' -%}")
    info_block_end = compiled.find('<div class="mt-4">')
    if info_block_start != -1 and info_block_end != -1:
        mock_info_html = """
						<div class="contact-info-cards mb-4">
							<div class="contact-info-card">
								<div class="card-icon"><i class="ph-bold ph-map-pin"></i></div>
								<div class="card-content">
									<h6>Địa chỉ</h6>
									<p>702 Võ Nguyên Giáp, Hiệp Phú, Thủ Đức, Hồ Chí Minh</p>
								</div>
							</div>
							<div class="contact-info-card">
								<div class="card-icon"><i class="ph-bold ph-envelope"></i></div>
								<div class="card-content">
									<h6>Email</h6>
									<p><a href="mailto:hi@navastore.vn" title="hi@navastore.vn">hi@navastore.vn</a></p>
								</div>
							</div>
							<div class="contact-info-card">
								<div class="card-icon"><i class="ph-bold ph-phone"></i></div>
								<div class="card-content">
									<h6>Hotline</h6>
									<p><a href="tel:0972178527" title="0972178527">0972178527</a></p>
								</div>
							</div>
							<div class="contact-info-card">
								<div class="card-icon"><i class="ph-bold ph-scroll"></i></div>
								<div class="card-content">
									<h6>Mã số thuế</h6>
									<p>MST: 8080980349-001</p>
								</div>
							</div>
						</div>
						
"""
        compiled = compiled[:info_block_start] + mock_info_html + compiled[info_block_end:]
        
    # Replace map block
    map_block_start = compiled.find('<div class="google-map rounded-10 overflow-hidden border">')
    map_block_end = compiled.find('</div>', map_block_start)
    if map_block_start != -1 and map_block_end != -1:
        map_block_end_full = compiled.find('</div>', map_block_end + 1)
        mock_map_html = """<div class="google-map rounded-10 overflow-hidden border">
							<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d721.3317906792457!2d106.74626274648564!3d10.801656253942495!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3175275302646ec5%3A0x82d15ef590c22180!2sNAVA%20STORE!5e1!3m2!1svi!2s!4v1747503843870!5m2!1svi!2s" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
						</div>"""
        compiled = compiled[:map_block_start] + mock_map_html + compiled[map_block_end_full + 6:]

    # Form mock
    compiled = compiled.replace("{%- form 'contact' -%}", '<form action="javascript:;" onsubmit="alert(\'Gửi liên hệ thành công!\'); this.reset();">')
    compiled = compiled.replace("{%- endform -%}", '</form>')
    compiled = compiled.replace("{%- include 'form-errors-custom' -%}", '')
    
    compiled = compiled.replace("{{settings.form_contact_name | append: ' *'}}", "Họ & Tên *")
    compiled = compiled.replace("{{settings.form_contact_mail | append: ' *'}}", "Địa chỉ email *")
    compiled = compiled.replace("{{settings.form_contact_content | append: ' *'}}", "Nội dung *")
    compiled = compiled.replace("{{settings.form_contact_require}}", "Thông tin bắt buộc")
    compiled = compiled.replace("{{settings.form_contact_submit}}", "Gửi liên hệ")
    
    full_html = clean_liquid_tags(header_part + compiled + local_footer_part, 'page')
    full_html = inject_seo_metadata(
        full_html,
        title="Liên Hệ - Nava Store",
        description="Liên hệ với Nava Store - Địa chỉ cung cấp Mini PC & eGPU uy tín hàng đầu Việt Nam.",
        keywords="lien he nava store, mini pc, egpu, thu duc"
    )
    with open(os.path.join(base_dir, "demo_contact.html"), "w", encoding="utf-8") as f:
        f.write(full_html)

def build_article_page(base_dir, header_part, footer_part):
    sticky_stuff = ""
    with open(os.path.join(base_dir, "index.bwt"), "r", encoding="utf-8") as f:
        idx_content = f.read()
        if "<!-- Mobile Sidebar Drawer -->" in idx_content:
            sticky_stuff = idx_content[idx_content.find("<!-- Mobile Sidebar Drawer -->"):]
            if "<!-- /MASTER SAPO ESCAPE WRAPPER -->" in sticky_stuff:
                sticky_stuff = sticky_stuff.split("<!-- /MASTER SAPO ESCAPE WRAPPER -->")[0]
                
    local_footer_part = sticky_stuff + '<script src="assets/main.js" defer></script>\n' + footer_part

    # Load BWT template
    with open(os.path.join(base_dir, "sapo_BWT_new", "Templates", "article.bwt"), "r", encoding="utf-8") as f:
        bwt_template = f.read()

    # Load extracted real content
    with open(os.path.join(base_dir, "scratch", "m_content_art.html"), "r", encoding="utf-8") as f:
        real_content = f.read()

    # Mock elements
    mock_breadcrumb = """
        <div class="breadcrumbs mt-3">
            <div class="container">
                <ul class="breadcrumb align-items-center m-0 pl-0 pr-0 small pt-2 pb-2" style="list-style: none; display: flex; gap: 8px; padding-left: 0;">
                    <li class="home">
                        <a href="index.html" title="Trang chủ" style="text-decoration: none; color: var(--text-gray);"><i class="ph ph-house"></i> Trang chủ</a>
                        <span class="slash-divider ml-2 mr-2">/</span>
                    </li>
                    <li>
                        <a href="demo_collection.html" title="Tin tức" style="text-decoration: none; color: var(--text-gray);">Tin tức</a>
                        <span class="slash-divider ml-2 mr-2">/</span>
                    </li>
                    <li class="active" style="color: var(--primary); font-weight: 700;">NPU Và AI: Công Nghệ Cốt Lõi Tạo Nên Mini PC Asus Thế Hệ Mới</li>
                </ul>
            </div>
        </div>
    """

    mock_aside_cate = """
        <div class="aside-widget">
            <h3 class="align-items-center d-flex font-weight-bold mb-3 pb-2 border-bottom" style="font-size: 1.15rem;">
                <i class="ph ph-tag" style="color: var(--primary); margin-right: 8px;"></i>
                Danh mục tin tức
            </h3>
            <ul class="list-unstyled" style="padding-left: 0; list-style: none; margin-bottom: 0;">
                <li class="mb-2" style="margin-bottom: 8px;"><a href="#" style="color: var(--text-dark); font-weight: 600; text-decoration: none; font-size: 0.95rem;"><i class="ph ph-caret-right" style="font-size: 0.8rem; margin-right: 4px;"></i> Tin công nghệ (12)</a></li>
                <li class="mb-2" style="margin-bottom: 8px;"><a href="#" style="color: var(--text-dark); font-weight: 600; text-decoration: none; font-size: 0.95rem;"><i class="ph ph-caret-right" style="font-size: 0.8rem; margin-right: 4px;"></i> Đánh giá chi tiết (8)</a></li>
                <li class="mb-2" style="margin-bottom: 8px;"><a href="#" style="color: var(--text-dark); font-weight: 600; text-decoration: none; font-size: 0.95rem;"><i class="ph ph-caret-right" style="font-size: 0.8rem; margin-right: 4px;"></i> Hướng dẫn kỹ thuật (15)</a></li>
                <li class="mb-2" style="margin-bottom: 8px;"><a href="#" style="color: var(--text-dark); font-weight: 600; text-decoration: none; font-size: 0.95rem;"><i class="ph ph-caret-right" style="font-size: 0.8rem; margin-right: 4px;"></i> Sự kiện & Khuyến mãi (5)</a></li>
            </ul>
        </div>
        <div class="aside-widget">
            <h3 class="align-items-center d-flex font-weight-bold mb-3 pb-2 border-bottom" style="font-size: 1.15rem; display: flex; align-items: center;">
                <img alt="Chủ đề Hot" class="lazy mr-2" style="width: 20px; height: 20px;" data-src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/hot_ico.png?1780651888006" src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/placeholder_1x1.png?1780651888006"/>
                Chủ đề Hot
            </h3>
            <ul class="list-unstyled mb-0" style="padding-left: 0; list-style: none;">
                <li class="d-flex align-items-center mb-3" style="gap: 12px; margin-bottom: 15px;">
                    <div class="image rounded-10 overflow-hidden" style="width: 70px; height: 55px; flex-shrink: 0; border: 1px solid var(--border-color);">
                        <a href="#" class="d-block w-100 h-100">
                            <img class="lazy w-100 h-100" style="object-fit: cover;" src="//bizweb.dktcdn.net/thumb/large/100/543/817/articles/64063744dd568fdbb2011743919ea563.jpg?v=1759158346080" alt="Đánh giá ASUS NUC 14 Pro">
                        </a>
                    </div>
                    <div class="text" style="flex: 1; min-width: 0;">
                        <h4 class="font-weight-bold mb-1" style="font-size: 0.9rem; line-height: 1.35; margin: 0 0 4px 0;">
                            <a href="#" class="line_2 text-dark" style="text-decoration: none; color: var(--text-dark); transition: color 0.2s;">Đánh giá ASUS NUC 14 Pro: Sức mạnh AI trong thân máy siêu nhỏ gọn</a>
                        </h4>
                        <span class="d-block text-muted small" style="font-size: 0.78rem; color: var(--text-gray);">01/06/2026</span>
                    </div>
                </li>
                <li class="d-flex align-items-center mb-3" style="gap: 12px; margin-bottom: 15px;">
                    <div class="image rounded-10 overflow-hidden" style="width: 70px; height: 55px; flex-shrink: 0; border: 1px solid var(--border-color);">
                        <a href="#" class="d-block w-100 h-100">
                            <img class="lazy w-100 h-100" style="object-fit: cover;" src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_1.png" alt="Thế hệ Mini PC AI 2025">
                        </a>
                    </div>
                    <div class="text" style="flex: 1; min-width: 0;">
                        <h4 class="font-weight-bold mb-1" style="font-size: 0.9rem; line-height: 1.35; margin: 0 0 4px 0;">
                            <a href="#" class="line_2 text-dark" style="text-decoration: none; color: var(--text-dark); transition: color 0.2s;">Thế hệ Mini PC AI 2025: Những cải tiến đột phá từ chip Intel Core Ultra</a>
                        </h4>
                        <span class="d-block text-muted small" style="font-size: 0.78rem; color: var(--text-gray);">28/05/2026</span>
                    </div>
                </li>
                <li class="d-flex align-items-center mb-3" style="gap: 12px; margin-bottom: 15px;">
                    <div class="image rounded-10 overflow-hidden" style="width: 70px; height: 55px; flex-shrink: 0; border: 1px solid var(--border-color);">
                        <a href="#" class="d-block w-100 h-100">
                            <img class="lazy w-100 h-100" style="object-fit: cover;" src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" alt="NPU vs GPU">
                        </a>
                    </div>
                    <div class="text" style="flex: 1; min-width: 0;">
                        <h4 class="font-weight-bold mb-1" style="font-size: 0.9rem; line-height: 1.35; margin: 0 0 4px 0;">
                            <a href="#" class="line_2 text-dark" style="text-decoration: none; color: var(--text-dark); transition: color 0.2s;">NPU vs GPU: Chọn cấu hình nào để học tập và làm việc với AI hiệu quả?</a>
                        </h4>
                        <span class="d-block text-muted small" style="font-size: 0.78rem; color: var(--text-gray);">20/05/2026</span>
                    </div>
                </li>
                <li class="d-flex align-items-center mb-3" style="gap: 12px; margin-bottom: 15px;">
                    <div class="image rounded-10 overflow-hidden" style="width: 70px; height: 55px; flex-shrink: 0; border: 1px solid var(--border-color);">
                        <a href="#" class="d-block w-100 h-100">
                            <img class="lazy w-100 h-100" style="object-fit: cover;" src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/placeholder_1x1.png?1780651888006" data-src="//bizweb.dktcdn.net/100/543/817/articles/2d8b49e4ab1b128c52c8ffa44eeb7e7f.jpg?v=1759161126157" alt="Gemini Đổ Bộ Google TV">
                        </a>
                    </div>
                    <div class="text" style="flex: 1; min-width: 0;">
                        <h4 class="font-weight-bold mb-1" style="font-size: 0.9rem; line-height: 1.35; margin: 0 0 4px 0;">
                            <a href="#" class="line_2 text-dark" style="text-decoration: none; color: var(--text-dark); transition: color 0.2s;">Nói Chuyện Với TV: Gemini Đổ Bộ Trực Tiếp Lên Google TV Thế Hệ Mới</a>
                        </h4>
                        <span class="d-block text-muted small" style="font-size: 0.78rem; color: var(--text-gray);">15/05/2026</span>
                    </div>
                </li>
                <li class="d-flex align-items-center mb-3" style="gap: 12px; margin-bottom: 15px;">
                    <div class="image rounded-10 overflow-hidden" style="width: 70px; height: 55px; flex-shrink: 0; border: 1px solid var(--border-color);">
                        <a href="#" class="d-block w-100 h-100">
                            <img class="lazy w-100 h-100" style="object-fit: cover;" src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/placeholder_1x1.png?1780651888006" data-src="//bizweb.dktcdn.net/100/543/817/articles/03325267e248a4f5acaa4902ac15df08.jpg?v=1759162962320" alt="Windows 11 SST Fix">
                        </a>
                    </div>
                    <div class="text" style="flex: 1; min-width: 0;">
                        <h4 class="font-weight-bold mb-1" style="font-size: 0.9rem; line-height: 1.35; margin: 0 0 4px 0;">
                            <a href="#" class="line_2 text-dark" style="text-decoration: none; color: var(--text-dark); transition: color 0.2s;">Windows 11 SST Fix: Intel Smart Sound Technology Được Vá Lỗi</a>
                        </h4>
                        <span class="d-block text-muted small" style="font-size: 0.78rem; color: var(--text-gray);">12/05/2026</span>
                    </div>
                </li>
                <li class="d-flex align-items-center mb-3" style="gap: 12px; margin-bottom: 15px;">
                    <div class="image rounded-10 overflow-hidden" style="width: 70px; height: 55px; flex-shrink: 0; border: 1px solid var(--border-color);">
                        <a href="#" class="d-block w-100 h-100">
                            <img class="lazy w-100 h-100" style="object-fit: cover;" src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/placeholder_1x1.png?1780651888006" data-src="//bizweb.dktcdn.net/100/543/817/articles/1000003603-asus-rog-nuc-2.jpg?v=1759229363977" alt="ROG NUC 2025">
                        </a>
                    </div>
                    <div class="text" style="flex: 1; min-width: 0;">
                        <h4 class="font-weight-bold mb-1" style="font-size: 0.9rem; line-height: 1.35; margin: 0 0 4px 0;">
                            <a href="#" class="line_2 text-dark" style="text-decoration: none; color: var(--text-dark); transition: color 0.2s;">Đánh giá Asus ROG NUC 2025: Sức mạnh Gaming trong khung máy siêu gọn</a>
                        </h4>
                        <span class="d-block text-muted small" style="font-size: 0.78rem; color: var(--text-gray);">08/05/2026</span>
                    </div>
                </li>
                <li class="d-flex align-items-center mb-3" style="gap: 12px; margin-bottom: 15px;">
                    <div class="image rounded-10 overflow-hidden" style="width: 70px; height: 55px; flex-shrink: 0; border: 1px solid var(--border-color);">
                        <a href="#" class="d-block w-100 h-100">
                            <img class="lazy w-100 h-100" style="object-fit: cover;" src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/placeholder_1x1.png?1780651888006" data-src="//bizweb.dktcdn.net/100/543/817/articles/feaa6c11b9330f909a13255c505893be.jpg?v=1759244477907" alt="Wi-Fi 7 Mini PC">
                        </a>
                    </div>
                    <div class="text" style="flex: 1; min-width: 0;">
                        <h4 class="font-weight-bold mb-1" style="font-size: 0.9rem; line-height: 1.35; margin: 0 0 4px 0;">
                            <a href="#" class="line_2 text-dark" style="text-decoration: none; color: var(--text-dark); transition: color 0.2s;">Tương lai kết nối: Wi-Fi 7 Đổ Bộ Dòng Máy Tính Mini PC Thế Hệ Mới</a>
                        </h4>
                        <span class="d-block text-muted small" style="font-size: 0.78rem; color: var(--text-gray);">02/05/2026</span>
                    </div>
                </li>
                <li class="d-flex align-items-center mb-3" style="gap: 12px; margin-bottom: 15px;">
                    <div class="image rounded-10 overflow-hidden" style="width: 70px; height: 55px; flex-shrink: 0; border: 1px solid var(--border-color);">
                        <a href="#" class="d-block w-100 h-100">
                            <img class="lazy w-100 h-100" style="object-fit: cover;" src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/placeholder_1x1.png?1780651888006" data-src="//bizweb.dktcdn.net/100/543/817/articles/6aded0f940f25f3ff7994130764b7c7f.jpg?v=1759247489540" alt="GMK EVO-X1">
                        </a>
                    </div>
                    <div class="text" style="flex: 1; min-width: 0;">
                        <h4 class="font-weight-bold mb-1" style="font-size: 0.9rem; line-height: 1.35; margin: 0 0 4px 0;">
                            <a href="#" class="line_2 text-dark" style="text-decoration: none; color: var(--text-dark); transition: color 0.2s;">So Sánh GMK EVO-X1 Và Beelink Ser 9: Cạnh Tranh Ngôi Vương Windows</a>
                        </h4>
                        <span class="d-block text-muted small" style="font-size: 0.78rem; color: var(--text-gray);">28/04/2026</span>
                    </div>
                </li>
            </ul>
        </div>
    """

    mock_blog_relate = """
        <h3 class="font-weight-bold mb-4" style="font-size: 1.3rem; color: var(--text-dark); display: flex; align-items: center; gap: 10px;">
            <i class="ph-fill ph-newspaper" style="color: var(--primary);"></i> Bài viết liên quan
        </h3>
        <div class="row">
            <div class="col-12 col-md-4 mb-3">
                <div class="card border-0 shadow-sm" style="border-radius: 12px; overflow: hidden; background: var(--bg-gray); border: 1px solid var(--border-color); display: flex; flex-direction: column; height: 100%;">
                    <img src="//bizweb.dktcdn.net/thumb/large/100/543/817/articles/64063744dd568fdbb2011743919ea563.jpg?v=1759158346080" class="card-img-top" style="height: 140px; width: 100%; object-fit: cover;">
                    <div class="card-body p-3" style="padding: 15px;">
                        <h5 class="card-title font-weight-bold mb-2" style="font-size: 0.92rem; line-height: 1.45; margin: 0 0 8px 0;"><a href="#" style="color: var(--text-dark); text-decoration: none; font-weight: 800;">Đánh giá ASUS NUC 14 Pro: Sức mạnh AI trong thân máy siêu nhỏ gọn</a></h5>
                        <span class="text-muted small" style="color: var(--text-gray); font-size: 0.8rem;">01/06/2026</span>
                    </div>
                </div>
            </div>
            <div class="col-12 col-md-4 mb-3">
                <div class="card border-0 shadow-sm" style="border-radius: 12px; overflow: hidden; background: var(--bg-gray); border: 1px solid var(--border-color); display: flex; flex-direction: column; height: 100%;">
                    <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_1.png" class="card-img-top" style="height: 140px; width: 100%; object-fit: cover;">
                    <div class="card-body p-3" style="padding: 15px;">
                        <h5 class="card-title font-weight-bold mb-2" style="font-size: 0.92rem; line-height: 1.45; margin: 0 0 8px 0;"><a href="#" style="color: var(--text-dark); text-decoration: none; font-weight: 800;">Thế hệ Mini PC AI 2025: Những cải tiến đột phá từ chip Intel Core Ultra</a></h5>
                        <span class="text-muted small" style="color: var(--text-gray); font-size: 0.8rem;">28/05/2026</span>
                    </div>
                </div>
            </div>
            <div class="col-12 col-md-4 mb-3">
                <div class="card border-0 shadow-sm" style="border-radius: 12px; overflow: hidden; background: var(--bg-gray); border: 1px solid var(--border-color); display: flex; flex-direction: column; height: 100%;">
                    <img src="//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" class="card-img-top" style="height: 140px; width: 100%; object-fit: cover;">
                    <div class="card-body p-3" style="padding: 15px;">
                        <h5 class="card-title font-weight-bold mb-2" style="font-size: 0.92rem; line-height: 1.45; margin: 0 0 8px 0;"><a href="#" style="color: var(--text-dark); text-decoration: none; font-weight: 800;">NPU vs GPU: Chọn cấu hình nào để học tập và làm việc với AI hiệu quả?</a></h5>
                        <span class="text-muted small" style="color: var(--text-gray); font-size: 0.8rem;">20/05/2026</span>
                    </div>
                </div>
            </div>
        </div>
    """

    mock_tags = """
        <div class="tags-list" style="margin-top: 15px;"><strong>Tags:</strong> 
            <span class="badge" style="background: var(--bg-gray); border: 1px solid var(--border-color); border-radius: 6px; padding: 4px 8px; font-size: 0.82rem; font-weight: 600; color: var(--text-gray); margin-right: 6px;">ASUS NUC</span> 
            <span class="badge" style="background: var(--bg-gray); border: 1px solid var(--border-color); border-radius: 6px; padding: 4px 8px; font-size: 0.82rem; font-weight: 600; color: var(--text-gray); margin-right: 6px;">AI PC</span> 
            <span class="badge" style="background: var(--bg-gray); border: 1px solid var(--border-color); border-radius: 6px; padding: 4px 8px; font-size: 0.82rem; font-weight: 600; color: var(--text-gray);">NPU</span>
        </div>
    """

    # Do compilation replacements
    compiled = bwt_template
    compiled = compiled.replace("{%- include 'breadcrumb' -%}", mock_breadcrumb)
    compiled = compiled.replace("{{ article.title | replace: '\"', '&quot;' }}", "NPU Và AI: Công Nghệ Cốt Lõi Tạo Nên Mini PC Asus Thế Hệ Mới")
    compiled = compiled.replace("{{ article.title }}", "NPU Và AI: Công Nghệ Cốt Lõi Tạo Nên Mini PC Asus Thế Hệ Mới")
    compiled = compiled.replace("{{ article.image.src | img_url: '1024x1024' }}", "https://bizweb.dktcdn.net/thumb/grande/100/543/817/articles/64063744dd568fdbb2011743919ea563.jpg?v=1759158346080")
    compiled = compiled.replace("{{ article.author }}", "Châu Bảo")
    compiled = compiled.replace("{{ article.published_on | date:'dd/MM/yyyy' }}", "01/06/2026")
    compiled = compiled.replace("{{ number_of_comments }}", "0")
    compiled = compiled.replace("{{ article.summary }}", "Khám phá cách NPU và AI trở thành nền tảng cốt lõi của Mini PC Asus thế hệ mới. Hiệu năng mạnh mẽ, tiết kiệm năng lượng, hỗ trợ học tập, sáng tạo nội dung và nghiên cứu AI - Tất cả gói gọn trong thiết kế của máy tính mini thương hiệu Asus.")
    compiled = compiled.replace("{%- include 'm_content_art' -%}", real_content)
    compiled = compiled.replace("{% include 'aside-cate-blog' %}", mock_aside_cate)
    compiled = compiled.replace("{%- include 'm_blog_relate' -%}", mock_blog_relate)
    compiled = compiled.replace("{% include 'mew_tag_article' %}", mock_tags)
    
    # Author mock
    compiled = compiled.replace("{{ avata | file_url }}", "https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/logo.png?1780651888006")
    compiled = compiled.replace("{{ pages[author_handle].title | default: article.author }}", "Châu Bảo")
    compiled = compiled.replace("{{ pages[author_handle].content | strip_html | truncate: 400 }}", "Châu Bảo là chuyên gia công nghệ và biên tập viên tại Nava Store, chuyên sâu về các dòng máy tính mini PC, linh kiện máy tính và các giải pháp eGPU cao cấp.")
    compiled = compiled.replace("{{ pages[author_handle].url }}", "javascript:;")
    
    # Form mock
    compiled = compiled.replace('{%- form "article_comments", article -%}', '<form action="javascript:;" onsubmit="alert(\'Bình luận của bạn đã được gửi thành công và đang chờ kiểm duyệt!\'); this.reset();">')
    compiled = compiled.replace('{%- endform -%}', '</form>')
    compiled = compiled.replace("{%- include 'form-errors-custom' -%}", '')
    compiled = compiled.replace("{%- if form.posted_successfully -%}", "{% if false %}")
    compiled = compiled.replace("{%- endif -%}", "{% endif %}")
    
    # Settings mock
    compiled = compiled.replace("{{ settings.blog_write_comment }}", "Để lại bình luận của bạn")
    compiled = compiled.replace("{{ settings.blog_comment_name }}", "Tên của bạn")
    compiled = compiled.replace("{{ settings.blog_comment_mail }}", "Email của bạn")
    compiled = compiled.replace("{{ settings.blog_comment_content }}", "Nhập nội dung bình luận")
    compiled = compiled.replace("{{ settings.blog_comment_submit }}", "Gửi bình luận")
    compiled = compiled.replace("{{ settings.blog_comment }}", "Bình luận nổi bật")
    compiled = compiled.replace("{{ settings.blog_no_comment_noti }}", "Chưa có bình luận nào cho bài viết này. Hãy là người đầu tiên chia sẻ cảm nghĩ!")
    
    full_html = clean_liquid_tags(header_part + compiled + local_footer_part, 'article')
    
    full_html = inject_seo_metadata(
        full_html,
        title="NPU Và AI: Công Nghệ Cốt Lõi Tạo Nên Mini PC Asus Thế Hệ Mới - Nava Store",
        description="Khám phá cách NPU và AI trở thành nền tảng cốt lõi của Mini PC Asus thế hệ mới. Hiệu năng mạnh mẽ, tiết kiệm năng lượng, hỗ trợ học tập, sáng tạo nội dung và nghiên cứu AI.",
        keywords="npu, ai, asus mini pc, asus nuc, nava store"
    )
    with open(os.path.join(base_dir, "demo_article.html"), "w", encoding="utf-8") as f:
        f.write(full_html)

def build_blog_page(base_dir, header_part, footer_part):
    sticky_stuff = ""
    with open(os.path.join(base_dir, "index.bwt"), "r", encoding="utf-8") as f:
        idx_content = f.read()
        if "<!-- Mobile Sidebar Drawer -->" in idx_content:
            sticky_stuff = idx_content[idx_content.find("<!-- Mobile Sidebar Drawer -->"):]
            if "<!-- /MASTER SAPO ESCAPE WRAPPER -->" in sticky_stuff:
                sticky_stuff = sticky_stuff.split("<!-- /MASTER SAPO ESCAPE WRAPPER -->")[0]
                
    local_footer_part = sticky_stuff + '<script src="assets/main.js" defer></script>\n' + footer_part

    # Load BWT template
    with open(os.path.join(base_dir, "sapo_BWT_new", "Templates", "blog.bwt"), "r", encoding="utf-8") as f:
        bwt_template = f.read()
    compiled = bwt_template

    # Mock breadcrumb
    mock_breadcrumb = """
        <div class="breadcrumbs mt-3">
            <div class="container">
                <ul class="breadcrumb align-items-center m-0 pl-0 pr-0 small pt-2 pb-2" style="list-style: none; display: flex; gap: 8px; padding-left: 0;">
                    <li class="home">
                        <a href="index.html" title="Trang chủ" style="text-decoration: none; color: var(--text-gray);"><i class="ph ph-house"></i> Trang chủ</a>
                        <span class="slash-divider ml-2 mr-2">/</span>
                    </li>
                    <li class="active" style="color: var(--primary); font-weight: 700;">Tin tức công nghệ</li>
                </ul>
            </div>
        </div>
    """

    # Mock elements
    mock_featured = """
				<div class="col-md-7 col-12">
					<div class="large-article-wrapper position-relative modal-open mb-3 mb-md-0">
						<img src="https://bizweb.dktcdn.net/thumb/grande/100/543/817/articles/64063744dd568fdbb2011743919ea563.jpg?v=1759158346080" class="img-cover position-absolute" alt="Đánh giá ASUS NUC 14 Pro">
						<div class="large-article-info">
							<span class="tag-badge">Đánh giá</span>
							<h3 class="title_blo font-weight-bold mt-2 mt-md-0 mb-0 mb-md-2">
								<a class="line_2" href="demo_article.html" title="Đánh giá ASUS NUC 14 Pro: Sức mạnh AI trong thân máy siêu nhỏ gọn">Đánh giá ASUS NUC 14 Pro: Sức mạnh AI trong thân máy siêu nhỏ gọn</a>
							</h3>
							<div class="meta-date">
								<i class="ph ph-calendar"></i> 01/06/2026
							</div>
							<p class="desc line_2 d-none d-md-block">Khám phá ASUS NUC 14 Pro sở hữu vi xử lý Intel Core Ultra tích hợp NPU đầu tiên, mang lại hiệu năng xử lý tác vụ AI vượt trội cùng thiết kế nhỏ gọn, nâng cao năng suất làm việc.</p>
						</div>
					</div>
				</div>
				<div class="col-12 col-md-5">
					<div class="sidebar-articles-list">
						<div class="mini-article-item">
							<a href="demo_article.html" title="Thế hệ Mini PC AI 2025" class="thumb-link">
								<img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_1.png" alt="Thế hệ Mini PC AI 2025">
							</a>
							<div class="mini-article-info">
								<h4 class="title">
									<a class="line_2" href="demo_article.html" title="Thế hệ Mini PC AI 2025: Những cải tiến đột phá từ chip Intel Core Ultra">Thế hệ Mini PC AI 2025: Những cải tiến đột phá từ chip Intel Core Ultra</a>
								</h4>
								<span class="date">
									<i class="ph ph-calendar"></i> 28/05/2026
								</span>
							</div>
						</div>
						<div class="mini-article-item">
							<a href="demo_article.html" title="NPU vs GPU" class="thumb-link">
								<img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" alt="NPU vs GPU">
							</a>
							<div class="mini-article-info">
								<h4 class="title">
									<a class="line_2" href="demo_article.html" title="NPU vs GPU: Chọn cấu hình nào để học tập và làm việc với AI hiệu quả?">NPU vs GPU: Chọn cấu hình nào để học tập và làm việc với AI hiệu quả?</a>
								</h4>
								<span class="date">
									<i class="ph ph-calendar"></i> 20/05/2026
								</span>
							</div>
						</div>
						<div class="mini-article-item">
							<a href="demo_article.html" title="Gemini Đổ Bộ Google TV" class="thumb-link">
								<img src="https://bizweb.dktcdn.net/thumb/large/100/543/817/articles/2d8b49e4ab1b128c52c8ffa44eeb7e7f.jpg?v=1759161126157" alt="Gemini Đổ Bộ Google TV">
							</a>
							<div class="mini-article-info">
								<h4 class="title">
									<a class="line_2" href="demo_article.html" title="Nói Chuyện Với TV: Gemini Đổ Bộ Trực Tiếp Lên Google TV Thế Hệ Mới">Nói Chuyện Với TV: Gemini Đổ Bộ Trực Tiếp Lên Google TV Thế Hệ Mới</a>
								</h4>
								<span class="date">
									<i class="ph ph-calendar"></i> 15/05/2026
								</span>
							</div>
						</div>
						<div class="mini-article-item">
							<a href="demo_article.html" title="Windows 11 SST Fix" class="thumb-link">
								<img src="https://bizweb.dktcdn.net/thumb/large/100/543/817/articles/03325267e248a4f5acaa4902ac15df08.jpg?v=1759162962320" alt="Windows 11 SST Fix">
							</a>
							<div class="mini-article-info">
								<h4 class="title">
									<a class="line_2" href="demo_article.html" title="Windows 11 SST Fix: Intel Smart Sound Technology Được Vá Lỗi Khóa Màn Hình Xanh">Windows 11 SST Fix: Intel Smart Sound Technology Được Vá Lỗi Khóa Màn Hình Xanh</a>
								</h4>
								<span class="date">
									<i class="ph ph-calendar"></i> 12/05/2026
								</span>
							</div>
						</div>
						<div class="mini-article-item">
							<a href="demo_article.html" title="Đánh giá Asus ROG NUC 2025" class="thumb-link">
								<img src="https://bizweb.dktcdn.net/thumb/large/100/543/817/articles/1000003603-asus-rog-nuc-2.jpg?v=1759229363977" alt="Đánh giá Asus ROG NUC 2025">
							</a>
							<div class="mini-article-info">
								<h4 class="title">
									<a class="line_2" href="demo_article.html" title="Đánh giá Asus ROG NUC 2025: Sức mạnh Gaming trong khung máy siêu gọn">Đánh giá Asus ROG NUC 2025: Sức mạnh Gaming trong khung máy siêu gọn</a>
								</h4>
								<span class="date">
									<i class="ph ph-calendar"></i> 08/05/2026
								</span>
							</div>
						</div>
					</div>
				</div>
    """

    mock_categories = """
	<div class="container mt-3 mb-3">
		<div class="blog-list b_mew_cate rounded-10 p-lg-3 pl-2 pr-2 bg-white">
			<h3 class="align-items-center blog-name d-flex font-weight-bold pt-2 pt-lg-0">
				<img class="lazy mr-2" src="assets/placeholder_1x1.png" data-src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/hot_ico.png?1780651888006" alt="Chủ đề Hot"> 
				Chủ đề Hot
			</h3>
			<ul class="d-flex b_item flex-wrap mobi_cate mb-0 p-0">
				<li class="d-flex align-items-center position-relative">
					<div class="image">
						<a href="#" title="Tin công nghệ">
							<img class="lazy" src="assets/placeholder_1x1.png" data-src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_1.png" alt="Tin công nghệ">
						</a>
					</div>
					<div class="text">
						<h4 class="font-weight-bold">
							<a href="#" title="Tin công nghệ">Tin công nghệ</a>
						</h4>
						<span>12 bài viết</span>
					</div>
				</li>
				<li class="d-flex align-items-center position-relative">
					<div class="image">
						<a href="#" title="Đánh giá chi tiết">
							<img class="lazy" src="assets/placeholder_1x1.png" data-src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" alt="Đánh giá chi tiết">
						</a>
					</div>
					<div class="text">
						<h4 class="font-weight-bold">
							<a href="#" title="Đánh giá chi tiết">Đánh giá chi tiết</a>
						</h4>
						<span>8 bài viết</span>
					</div>
				</li>
				<li class="d-flex align-items-center position-relative">
					<div class="image">
						<a href="#" title="Hướng dẫn kỹ thuật">
							<img class="lazy" src="assets/placeholder_1x1.png" data-src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_1_1.png" alt="Hướng dẫn kỹ thuật">
						</a>
					</div>
					<div class="text">
						<h4 class="font-weight-bold">
							<a href="#" title="Hướng dẫn kỹ thuật">Hướng dẫn kỹ thuật</a>
						</h4>
						<span>15 bài viết</span>
					</div>
				</li>
				<li class="d-flex align-items-center position-relative">
					<div class="image">
						<a href="#" title="Sự kiện & Khuyến mãi">
							<img class="lazy" src="assets/placeholder_1x1.png" data-src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_4_1.png" alt="Sự kiện & Khuyến mãi">
						</a>
					</div>
					<div class="text">
						<h4 class="font-weight-bold">
							<a href="#" title="Sự kiện & Khuyến mãi">Sự kiện & Khuyến mãi</a>
						</h4>
						<span>5 bài viết</span>
					</div>
				</li>
			</ul>
		</div>
	</div>
    """

    mock_grid_feed = """
			<article>
				<div class="grid_article">
					<div class="row" id="AjaxinateContainer">
						
						<!-- Item 1 -->
						<div class="col-12 col-sm-6 col-md-6 col-lg-4 its">
							<div class="custom-article-item mb-4 overflow-hidden">
								<a href="demo_article.html" title="Đánh giá ASUS NUC 14 Pro" class="effect-ming">
									<img src="assets/placeholder_1x1.png" data-src="https://bizweb.dktcdn.net/thumb/grande/100/543/817/articles/64063744dd568fdbb2011743919ea563.jpg?v=1759158346080" class="lazy d-block" alt="Đánh giá ASUS NUC 14 Pro">
								</a>
								<div class="custom-article-item_info">
									<h3 class="title_blo font-weight-bold">
										<a href="demo_article.html" title="Đánh giá ASUS NUC 14 Pro: Sức mạnh AI trong thân máy siêu nhỏ gọn">Đánh giá ASUS NUC 14 Pro: Sức mạnh AI trong thân máy siêu nhỏ gọn</a>
									</h3>
									<span class="meta-date">
										<i class="ph ph-calendar"></i> 01/06/2026
									</span>
									<p class="sum">
										Khám phá ASUS NUC 14 Pro sở hữu vi xử lý Intel Core Ultra tích hợp NPU đầu tiên, mang lại hiệu năng xử lý tác vụ AI vượt trội cùng thiết kế nhỏ gọn.
									</p>
									<div class="tags mt-2">
										<a class="item_tags badge-warning" href="#" title="Đánh giá">Đánh giá</a>
										<a class="item_tags badge-warning" href="#" title="ASUS NUC">ASUS NUC</a>
									</div>
								</div>
							</div>
						</div>

						<!-- Item 2 -->
						<div class="col-12 col-sm-6 col-md-6 col-lg-4 its">
							<div class="custom-article-item mb-4 overflow-hidden">
								<a href="demo_article.html" title="Thế hệ Mini PC AI 2025" class="effect-ming">
									<img src="assets/placeholder_1x1.png" data-src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_1.png" class="lazy d-block" alt="Thế hệ Mini PC AI 2025">
								</a>
								<div class="custom-article-item_info">
									<h3 class="title_blo font-weight-bold">
										<a href="demo_article.html" title="Thế hệ Mini PC AI 2025: Những cải tiến đột phá từ chip Intel Core Ultra">Thế hệ Mini PC AI 2025: Những cải tiến đột phá từ chip Intel Core Ultra</a>
									</h3>
									<span class="meta-date">
										<i class="ph ph-calendar"></i> 28/05/2026
									</span>
									<p class="sum">
										Điểm danh những nâng cấp phần cứng đáng giá nhất trên các thế hệ máy tính mini PC trang bị vi xử lý Intel Core Ultra thế hệ mới nhất.
									</p>
									<div class="tags mt-2">
										<a class="item_tags badge-warning" href="#" title="Mini PC">Mini PC</a>
										<a class="item_tags badge-warning" href="#" title="AI PC">AI PC</a>
									</div>
								</div>
							</div>
						</div>

						<!-- Item 3 -->
						<div class="col-12 col-sm-6 col-md-6 col-lg-4 its">
							<div class="custom-article-item mb-4 overflow-hidden">
								<a href="demo_article.html" title="NPU vs GPU" class="effect-ming">
									<img src="assets/placeholder_1x1.png" data-src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png" class="lazy d-block" alt="NPU vs GPU">
								</a>
								<div class="custom-article-item_info">
									<h3 class="title_blo font-weight-bold">
										<a href="demo_article.html" title="NPU vs GPU: Chọn cấu hình nào để học tập và làm việc với AI hiệu quả?">NPU vs GPU: Chọn cấu hình nào để học tập và làm việc với AI hiệu quả?</a>
									</h3>
									<span class="meta-date">
										<i class="ph ph-calendar"></i> 20/05/2026
									</span>
									<p class="sum">
										So sánh sự khác biệt trong kiến trúc và hiệu suất tính toán giữa NPU tích hợp và GPU rời khi xử lý các mô hình ngôn ngữ lớn LLM và sinh ảnh AI.
									</p>
									<div class="tags mt-2">
										<a class="item_tags badge-warning" href="#" title="Công nghệ">Công nghệ</a>
										<a class="item_tags badge-warning" href="#" title="AI">AI</a>
									</div>
								</div>
							</div>
						</div>

						<!-- Item 4 -->
						<div class="col-12 col-sm-6 col-md-6 col-lg-4 its">
							<div class="custom-article-item mb-4 overflow-hidden">
								<a href="demo_article.html" title="Gemini Đổ Bộ Google TV" class="effect-ming">
									<img src="assets/placeholder_1x1.png" data-src="https://bizweb.dktcdn.net/thumb/large/100/543/817/articles/2d8b49e4ab1b128c52c8ffa44eeb7e7f.jpg?v=1759161126157" class="lazy d-block" alt="Gemini Đổ Bộ Google TV">
								</a>
								<div class="custom-article-item_info">
									<h3 class="title_blo font-weight-bold">
										<a href="demo_article.html" title="Nói Chuyện Với TV: Gemini Đổ Bộ Trực Tiếp Lên Google TV Thế Hệ Mới">Nói Chuyện Với TV: Gemini Đổ Bộ Trực Tiếp Lên Google TV Thế Hệ Mới</a>
									</h3>
									<span class="meta-date">
										<i class="ph ph-calendar"></i> 15/05/2026
									</span>
									<p class="sum">
										Google TV cập nhật giao diện và tính năng trợ lý ảo Gemini, cho phép bạn tìm kiếm phim bằng giọng nói tự nhiên cực kỳ mượt mà.
									</p>
									<div class="tags mt-2">
										<a class="item_tags badge-warning" href="#" title="Google TV">Google TV</a>
										<a class="item_tags badge-warning" href="#" title="Gemini">Gemini</a>
									</div>
								</div>
							</div>
						</div>

						<!-- Item 5 -->
						<div class="col-12 col-sm-6 col-md-6 col-lg-4 its">
							<div class="custom-article-item mb-4 overflow-hidden">
								<a href="demo_article.html" title="Windows 11 SST Fix" class="effect-ming">
									<img src="assets/placeholder_1x1.png" data-src="https://bizweb.dktcdn.net/thumb/large/100/543/817/articles/03325267e248a4f5acaa4902ac15df08.jpg?v=1759162962320" class="lazy d-block" alt="Windows 11 SST Fix">
								</a>
								<div class="custom-article-item_info">
									<h3 class="title_blo font-weight-bold">
										<a href="demo_article.html" title="Windows 11 SST Fix: Intel Smart Sound Technology Được Vá Lỗi Khóa Màn Hình Xanh">Windows 11 SST Fix: Intel Smart Sound Technology Được Vá Lỗi Khóa Màn Hình Xanh</a>
									</h3>
									<span class="meta-date">
										<i class="ph ph-calendar"></i> 12/05/2026
									</span>
									<p class="sum">
										Bản cập nhật tích hợp driver mới từ Intel đã giải quyết triệt để lỗi xung đột giữa Windows 11 và driver âm thanh Intel SST cũ gây lỗi màn hình xanh.
									</p>
									<div class="tags mt-2">
										<a class="item_tags badge-warning" href="#" title="Windows 11">Windows 11</a>
										<a class="item_tags badge-warning" href="#" title="Fix Lỗi">Fix Lỗi</a>
									</div>
								</div>
							</div>
						</div>

						<!-- Item 6 -->
						<div class="col-12 col-sm-6 col-md-6 col-lg-4 its">
							<div class="custom-article-item mb-4 overflow-hidden">
								<a href="demo_article.html" title="Đánh giá Asus ROG NUC 2025" class="effect-ming">
									<img src="assets/placeholder_1x1.png" data-src="https://bizweb.dktcdn.net/thumb/large/100/543/817/articles/1000003603-asus-rog-nuc-2.jpg?v=1759229363977" class="lazy d-block" alt="Đánh giá Asus ROG NUC 2025">
								</a>
								<div class="custom-article-item_info">
									<h3 class="title_blo font-weight-bold">
										<a href="demo_article.html" title="Đánh giá Asus ROG NUC 2025: Sức mạnh Gaming trong khung máy siêu gọn">Đánh giá Asus ROG NUC 2025: Sức mạnh Gaming trong khung máy siêu gọn</a>
									</h3>
									<span class="meta-date">
										<i class="ph ph-calendar"></i> 08/05/2026
									</span>
									<p class="sum">
										Đánh giá chi tiết quái vật mini PC Asus ROG NUC thế hệ thứ 2 với GPU rời RTX 4070, chiến mượt mà các tựa game AAA nặng ở độ phân giải 2K.
									</p>
									<div class="tags mt-2">
										<a class="item_tags badge-warning" href="#" title="ROG NUC">ROG NUC</a>
										<a class="item_tags badge-warning" href="#" title="Gaming">Gaming</a>
									</div>
								</div>
							</div>
						</div>

					</div>
					<div id="AjaxinatePagination">
						<a href="#" title="Xem thêm bài viết">
							Xem thêm bài viết
						</a>
					</div>
				</div>
			</article>
    """

    compiled = compiled.replace("{{ blog.name | default: 'Tất cả tin tức' }}", "Tất cả tin tức")
    compiled = compiled.replace("{% if blog.articles.size < 7 %}d-none{% endif %}", "")

    # Regex replacements for Liquid loops
    featured_block_regex = r"{%\s*if\s*blog\.articles\.size\s*>\s*0\s*%}.*?{%\s*endif\s*%}"
    compiled = re.sub(featured_block_regex, mock_featured, compiled, flags=re.DOTALL)

    category_block_regex = r"{%\s*if\s*linklists\[settings\.blogs_all_menu\]\.links\.size\s*>\s*0\s*%}.*?{%\s*endif\s*%}"
    compiled = re.sub(category_block_regex, mock_categories, compiled, flags=re.DOTALL)

    feed_block_regex = r"{%-\s*if\s*blog\.articles\.size\s*>\s*6\s*-%}.*?{%-\s*endif\s*-%}(?=\s*</div>\s*</div>)"
    compiled = re.sub(feed_block_regex, mock_grid_feed, compiled, flags=re.DOTALL)

    full_html = clean_liquid_tags(header_part + compiled + local_footer_part, 'blog')
    
    full_html = inject_seo_metadata(
        full_html,
        title="Tin Tức Công Nghệ & Đánh Giá Sản Phẩm - Nava Store",
        description="Cập nhật tin tức công nghệ mới nhất, đánh giá chi tiết mini PC, linh kiện eGPU, hướng dẫn cài đặt và thủ thuật từ các chuyên gia Nava Store.",
        keywords="tin tuc, cong nghe, danh gia mini pc, egpu, nava store"
    )
    with open(os.path.join(base_dir, "demo_blog.html"), "w", encoding="utf-8") as f:
        f.write(full_html)

def build_all():
    base_dir = r"F:\BAO_SAPO\sapo_new"
    
    # Copy icons to assets folder so local references load properly
    icon_dir = os.path.join(base_dir, "assets", "icon")
    assets_dir = os.path.join(base_dir, "assets")
    if os.path.exists(icon_dir):
        import shutil
        for f_name in os.listdir(icon_dir):
            src = os.path.join(icon_dir, f_name)
            if os.path.isfile(src):
                dst = os.path.join(assets_dir, f_name)
                shutil.copy2(src, dst)
        # Handle blender.png
        blender_src = os.path.join(icon_dir, "Blender logo.png")
        if os.path.exists(blender_src):
            shutil.copy2(blender_src, os.path.join(assets_dir, "blender.png"))
            shutil.copy2(blender_src, os.path.join(icon_dir, "blender.png"))

    header_part, footer_part = get_core_layout(base_dir)
    
    build_index(base_dir, header_part, footer_part)
    print("Generated index.html successfully!")
    
    build_collection(base_dir, header_part, footer_part)
    print("Generated demo_collection.html successfully!")
    
    build_product(base_dir, header_part, footer_part)
    print("Generated demo_product.html successfully!")
    
    build_compare_page(base_dir, header_part, footer_part)
    print("Generated demo_compare.html successfully!")
    
    build_cart_page(base_dir, header_part, footer_part)
    print("Generated demo_cart.html successfully!")

    build_checkout_page(base_dir)
    print("Generated demo_checkout.html successfully!")
    
    build_policy_pages(base_dir, header_part, footer_part)
    print("Generated demo_policy.html successfully!")
    
    build_auth_pages(base_dir)
    print("Generated demo_login.html and demo_register.html successfully!")
    
    build_article_page(base_dir, header_part, footer_part)
    print("Generated demo_article.html successfully!")
    
    build_blog_page(base_dir, header_part, footer_part)
    print("Generated demo_blog.html successfully!")
    
    build_contact_page(base_dir, header_part, footer_part)
    print("Generated demo_contact.html successfully!")

if __name__ == "__main__":
    build_all()
