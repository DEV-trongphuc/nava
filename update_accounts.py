import os
import re
from build_demos import get_core_layout, clean_liquid_tags

base_dir = r"f:\BAO_SAPO\sapo_new"
header_part, footer_part = get_core_layout(base_dir)

# Common Dashboard Sidebar
sidebar = """
<div class="dashboard-sidebar-wrapper">
    <div class="dashboard-sidebar">
        <div class="user-profile-section">
            <img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/account.png?1778729235331" alt="Avatar" style="width: 70px; height: 70px; margin: 0 auto 15px auto; display: block; border-radius: 50%;">
            <h3 class="user-name">Turnio Dev</h3>
        </div>
        
        <div class="sidebar-nav">
            <a href="account.html" class="nav-item-nava" id="nav-account">
                <i class="ph ph-user-circle"></i> Thông tin tài khoản
            </a>
            <a href="addresses.html" class="nav-item-nava" id="nav-addresses">
                <i class="ph ph-map-pin"></i> Sổ địa chỉ
            </a>
            <a href="change_pass.html" class="nav-item-nava" id="nav-change-pass">
                <i class="ph ph-lock-key"></i> Đổi mật khẩu
            </a>
            <div class="nav-divider"></div>
            <a href="demo_login.html" class="nav-item-nava text-danger">
                <i class="ph ph-sign-out"></i> Đăng xuất
            </a>
        </div>
    </div>
</div>
"""

custom_styles = """
<style>
    :root {
        --primary: #003366;
        --secondary: #004c99;
        --bg-white: #ffffff;
        --bg-gray: #f8fafc;
        --text-dark: #0f172a;
        --text-gray: #64748b;
        --border-color: #e2e8f0;
        --radius-md: 12px;
        --radius-lg: 24px;
    }
    
    /* Dashboard Base */
    body { background-color: var(--bg-gray); }
    .dashboard-container { max-width: 1200px; margin: 40px auto; padding: 0 15px; }
    
    /* Bulletproof Grid */
    .dashboard-grid { display: flex; gap: 30px; align-items: flex-start; }
    .dashboard-sidebar-wrapper { flex: 0 0 280px; width: 280px; align-self: stretch; }
    .dashboard-main-wrapper { flex: 1; min-width: 0; }
    
    /* Sidebar Styling */
    .dashboard-sidebar {
        background: #fff;
        border-radius: var(--radius-lg);
        box-shadow: 0 2px 10px rgba(0,0,0,0.02);
        border: 1px solid var(--border-color);
        overflow: hidden;
        position: sticky;
        top: 140px;
        height: fit-content;
    }
    .user-profile-section {
        padding: 30px 20px;
        text-align: center;
        border-bottom: 1px solid var(--border-color);
        background: #fff;
    }
    .user-name { font-size: 1.1rem; font-weight: 800; color: var(--text-dark); margin: 0; }
    
    .sidebar-nav { padding: 15px; }
    .nav-item-nava {
        display: flex; align-items: center; gap: 12px;
        padding: 12px 15px;
        color: var(--text-gray);
        text-decoration: none;
        font-weight: 600; font-size: 0.95rem;
        border-radius: var(--radius-md);
        transition: all 0.2s ease;
        margin-bottom: 4px;
    }
    .nav-item-nava i { font-size: 1.3rem; }
    .nav-item-nava:hover { background: var(--bg-gray); color: var(--primary); }
    .nav-item-nava.active { background: rgba(14, 165, 233, 0.08); color: var(--primary); font-weight: 700; }
    .nav-item-nava.text-danger:hover { background: rgba(239, 68, 68, 0.08); color: #ef4444; }
    .nav-divider { height: 1px; background: var(--border-color); margin: 10px 15px; }

    /* Main Content Styling */
    .dashboard-content {
        background: #fff;
        border-radius: var(--radius-lg);
        padding: 35px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.02);
        border: 1px solid var(--border-color);
        min-height: 100%;
    }
    .content-header {
        display: flex; justify-content: space-between; align-items: center;
        margin-bottom: 30px; padding-bottom: 20px;
        border-bottom: 1px solid var(--border-color);
    }
    .content-title { font-size: 1.4rem; font-weight: 800; color: var(--text-dark); margin: 0; display: flex; align-items: center; gap: 10px; }
    
    /* Info Box */
    .info-box {
        background: #f8fafc;
        border-radius: var(--radius-md);
        padding: 25px;
        border: 1px solid var(--border-color);
        margin-bottom: 40px;
    }
    .info-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
    .info-item label { display: block; font-size: 0.8rem; color: var(--text-gray); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 5px; }
    .info-item div { font-size: 1rem; font-weight: 600; color: var(--text-dark); }
    
    /* Table Styling */
    .section-title { font-size: 1.1rem; font-weight: 700; color: var(--text-dark); margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; }
    .table-container { border: 1px solid var(--border-color); border-radius: var(--radius-md); overflow: hidden; }
    .table-nava { width: 100%; border-collapse: collapse; }
    .table-nava th { background: #f8fafc; padding: 15px 20px; text-align: left; font-size: 0.85rem; font-weight: 700; color: var(--text-gray); text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 1px solid var(--border-color); }
    .table-nava td { padding: 15px 20px; border-bottom: 1px solid var(--border-color); vertical-align: middle; font-size: 0.95rem; }
    .table-nava tr:last-child td { border-bottom: none; }
    .table-nava tr:hover td { background: #f8fafc; }
    
    /* Badges & Buttons */
    .badge-status { padding: 6px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; display: inline-block; }
    .badge-success { background: rgba(16, 185, 129, 0.1); color: #059669; }
    .badge-warning { background: rgba(245, 158, 11, 0.1); color: #d97706; }
    .link-primary { color: var(--primary); text-decoration: none; font-weight: 600; transition: 0.2s; }
    .link-primary:hover { color: var(--secondary); text-decoration: underline; }
    
    .btn-nava { padding: 10px 20px; border-radius: var(--radius-md); font-weight: 600; font-size: 0.95rem; cursor: pointer; transition: all 0.2s; display: inline-flex; align-items: center; justify-content: center; gap: 8px; border: none; }
    .btn-nava-primary { background: linear-gradient(90deg, #0284c7, #2563eb) !important; color: white !important; box-shadow: 0 4px 10px rgba(37,99,235,0.2); }
    .btn-nava-primary:hover { transform: translateY(-2px); box-shadow: 0 6px 15px rgba(37,99,235,0.3); }
    
    /* Forms */
    .form-group-nava { margin-bottom: 20px; }
    .form-group-nava label { display: block; font-size: 0.9rem; font-weight: 600; margin-bottom: 8px; color: var(--text-dark); }
    .input-nava { width: 100%; padding: 12px 15px; border: 1px solid var(--border-color); border-radius: var(--radius-md); background: #f8fafc; font-size: 0.95rem; color: var(--text-dark); outline: none; transition: 0.3s; }
    .input-nava:focus { border-color: #0284c7; box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.15); background: #fff; }
    .select-nava { width: 100%; padding: 12px 15px; border: 1px solid var(--border-color); border-radius: var(--radius-md); background: #f8fafc url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 256 256'%3E%3Cpath fill='%2364748b' d='M213.66,101.66l-80,80a8,8,0,0,1-11.32,0l-80-80A8,8,0,0,1,53.66,90.34L128,164.69l74.34-74.35a8,8,0,0,1,11.32,11.32Z'/%3E%3C/svg%3E") no-repeat calc(100% - 15px) center; appearance: none; font-size: 0.95rem; color: var(--text-dark); outline: none; transition: 0.3s; }
    .select-nava:focus { border-color: #0284c7; box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.15); background-color: #fff; }
    
    /* Toggle Switch */
    .toggle-switch-nava { position: relative; display: inline-block; width: 44px; height: 24px; flex-shrink: 0; }
    .toggle-switch-nava input { opacity: 0; width: 0; height: 0; }
    .toggle-slider-nava { position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: #cbd5e1; transition: .3s; border-radius: 34px; }
    .toggle-slider-nava:before { position: absolute; content: ""; height: 18px; width: 18px; left: 3px; bottom: 3px; background-color: white; transition: .3s; border-radius: 50%; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }
    .toggle-switch-nava input:checked + .toggle-slider-nava { background: linear-gradient(90deg, #0284c7, #2563eb); }
    .toggle-switch-nava input:checked + .toggle-slider-nava:before { transform: translateX(20px); }
    
    /* Addresses Modal */
    .modal-overlay-nava { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); backdrop-filter: blur(4px); z-index: 9999; display: flex; align-items: center; justify-content: center; opacity: 0; visibility: hidden; transition: 0.3s; }
    .modal-overlay-nava.active { opacity: 1; visibility: visible; }
    .modal-content-nava { background: #fff; width: 100%; max-width: 600px; border-radius: var(--radius-lg); box-shadow: 0 10px 30px rgba(0,0,0,0.1); transform: translateY(20px); transition: 0.3s; max-height: 90vh; overflow-y: auto; }
    .modal-overlay-nava.active .modal-content-nava { transform: translateY(0); }
    .modal-header-nava { padding: 20px 25px; border-bottom: 1px solid var(--border-color); display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; background: #fff; z-index: 10; border-radius: var(--radius-lg) var(--radius-lg) 0 0; }
    .modal-title-nava { font-size: 1.2rem; font-weight: 800; color: var(--text-dark); margin: 0; }
    .modal-close-nava { background: none; border: none; font-size: 1.5rem; color: var(--text-gray); cursor: pointer; transition: 0.2s; display: flex; align-items: center; justify-content: center; width: 32px; height: 32px; border-radius: 8px; }
    .modal-close-nava:hover { background: #f1f5f9; color: #ef4444; }
    .modal-body-nava { padding: 25px; }
    .modal-footer-nava { padding: 20px 25px; border-top: 1px solid var(--border-color); display: flex; justify-content: flex-end; gap: 10px; position: sticky; bottom: 0; background: #fff; border-radius: 0 0 var(--radius-lg) var(--radius-lg); z-index: 10; }
    
    /* Addresses */
    .address-card { border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 20px; position: relative; transition: 0.2s; margin-bottom: 15px; background: #fff; }
    .address-card:hover { border-color: var(--primary); box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    .address-card.default { border-color: var(--primary); background: rgba(14, 165, 233, 0.02); }
    .address-actions { position: absolute; top: 20px; right: 20px; display: flex; gap: 10px; }
    .address-actions button { border: none; background: #f1f5f9; width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: var(--text-gray); cursor: pointer; transition: 0.2s; }
    .address-actions button:hover { background: var(--border-color); color: var(--text-dark); }
    .address-actions button.delete:hover { background: #fee2e2; color: #ef4444; }
    
    .region-item { padding: 15px 25px; border-bottom: 1px solid var(--border-color); cursor: pointer; font-size: 0.95rem; font-weight: 500; transition: 0.2s; }
    .region-item:hover { background: #f8fafc; color: #0284c7; }
    
    .list-item { display: flex; justify-content: space-between; align-items: center; padding: 15px 25px; border-bottom: 1px solid var(--border-color); cursor: pointer; transition: 0.2s; }
    .list-item:hover { background: #f8fafc; }
    .list-item-sub { font-size: 0.8rem; color: var(--text-gray); margin-top: 4px; }
    .modal-search-nava { padding: 15px 25px; border-bottom: 1px solid var(--border-color); background: #fff; }
    
    /* Mobile Responsive */
    @media (max-width: 991px) {
        .dashboard-container { margin: 30px auto 20px auto; }
        .dashboard-grid { flex-direction: column; gap: 20px; }
        .dashboard-sidebar-wrapper { flex: 1; width: 100%; }
        .dashboard-main-wrapper { width: 100%; max-width: 100%; }
        .dashboard-content { padding: 15px; width: 100%; max-width: 100%; box-sizing: border-box; }
        .info-grid { grid-template-columns: 1fr; gap: 15px; }
        .table-container { width: 100%; max-width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; border: 1px solid var(--border-color); }
        .table-nava { display: table; width: 100%; min-width: 600px; }
        .dashboard-sidebar { position: static; margin-bottom: 0; }
        .user-profile-section { display: flex; align-items: center; gap: 15px; padding: 20px; text-align: left; }
        .user-profile-section img { margin: 0 !important; width: 50px !important; height: 50px !important; }
        .sidebar-nav { display: flex; flex-wrap: wrap; padding: 10px 15px; gap: 5px; }
        .nav-item-nava { flex: 1 1 calc(50% - 5px); justify-content: center; padding: 10px; font-size: 0.85rem; text-align: center; flex-direction: column; gap: 5px; }
        .nav-item-nava i { font-size: 1.5rem; }
        .nav-divider { display: none; }
        .modal-content-nava { height: 100%; max-height: 100vh; border-radius: 0; transform: translateY(100%); }
        .modal-header-nava { border-radius: 0; }
        .modal-footer-nava { border-radius: 0; padding-bottom: 30px; }
    }
</style>

<script>
    document.addEventListener('DOMContentLoaded', function() {
        const path = window.location.pathname;
        if(path.includes('account.html')) document.getElementById('nav-account').classList.add('active');
        if(path.includes('change_pass.html')) document.getElementById('nav-change-pass').classList.add('active');
        if(path.includes('addresses.html')) document.getElementById('nav-addresses').classList.add('active');
    });
</script>
"""

# 1. ACCOUNT DASHBOARD
account_content = f"""
{custom_styles}
<div class="dashboard-container">
    <div class="dashboard-grid">
        {sidebar}
        <div class="dashboard-main-wrapper">
            <div class="dashboard-content">
                <div class="content-header" style="flex-wrap: wrap; gap: 15px;">
                    <h1 class="content-title"><i class="ph-fill ph-user-circle" style="color: var(--primary);"></i> Thông tin tài khoản</h1>
                    <button class="btn-nava btn-nava-primary" onclick="alert('Tính năng chỉnh sửa thông tin đang giả lập trên Sapo.')"><i class="ph-bold ph-pencil-simple"></i> Edit</button>
                </div>

                <div class="info-box">
                    <div class="info-grid">
                        <!-- Left Column -->
                        <div style="display: flex; flex-direction: column; gap: 20px;">
                            <div class="info-item">
                                <label>Họ và tên</label>
                                <div>Turnio Dev</div>
                            </div>
                            <div class="info-item">
                                <label>Địa chỉ Email</label>
                                <div>dev@turnio.net</div>
                            </div>
                        </div>
                        <!-- Right Column -->
                        <div style="display: flex; flex-direction: column; gap: 20px;">
                            <div class="info-item">
                                <label>Số điện thoại</label>
                                <div>0378859736</div>
                            </div>
                            <div class="info-item">
                                <label>Địa chỉ mặc định</label>
                                <div>123 Đường Nguyễn Văn Linh, Phường Tân Phong, Quận 7, TP. Hồ Chí Minh</div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="section-title">
                    Đơn hàng gần đây
                </div>
                
                <div class="table-container" style="margin-bottom: 40px;">
                    <table class="table-nava">
                        <thead>
                            <tr>
                                <th>Mã ĐH</th>
                                <th>Ngày đặt</th>
                                <th>Sản phẩm</th>
                                <th>Tổng tiền</th>
                                <th>Trạng thái</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><a href="#" class="link-primary">#NAV1025</a></td>
                                <td style="color: var(--text-gray);">18/05/2026</td>
                                <td>
                                    <div style="display: flex; align-items: center; gap: 12px;">
                                        <img src="https://bizweb.dktcdn.net/thumb/small/100/543/817/products/mini-pc-asus-nuc-ai-350-pn54-ryzen-ai-7-350-gaming.jpg" style="width: 44px; height: 44px; border-radius: 8px; border: 1px solid var(--border-color); object-fit: contain;">
                                        <span style="font-weight: 600; max-width: 180px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">ASUS NUC AI 350</span>
                                    </div>
                                </td>
                                <td style="font-weight: 700; color: var(--primary);">12.390.000đ</td>
                                <td><span class="badge-status badge-success">Đã giao hàng</span></td>
                            </tr>
                            <tr>
                                <td><a href="#" class="link-primary">#NAV1026</a></td>
                                <td style="color: var(--text-gray);">19/05/2026</td>
                                <td>
                                    <div style="display: flex; align-items: center; gap: 12px;">
                                        <div style="width: 44px; height: 44px; border-radius: 8px; border: 1px solid var(--border-color); background: #f1f5f9; display: flex; align-items: center; justify-content: center; font-size: 0.85rem; font-weight: bold; color: var(--text-gray);">+2</div>
                                        <span style="font-weight: 600; max-width: 180px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">RAM DDR5 32GB 5600MHz...</span>
                                    </div>
                                </td>
                                <td style="font-weight: 700; color: var(--primary);">3.500.000đ</td>
                                <td><span class="badge-status badge-warning">Đang xử lý</span></td>
                            </tr>
                        </tbody>
                    </table>
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
                            <div class="swiper-button-prev recent-prev" style="color: var(--primary); width: 35px; height: 35px; background: white; border-radius: 50%; box-shadow: 0 4px 10px rgba(0,0,0,0.1); border: 1px solid var(--border-color); display: flex; align-items: center; justify-content: center; --swiper-navigation-size: 14px;"></div>
                            <div class="swiper-button-next recent-next" style="color: var(--primary); width: 35px; height: 35px; background: white; border-radius: 50%; box-shadow: 0 4px 10px rgba(0,0,0,0.1); border: 1px solid var(--border-color); display: flex; align-items: center; justify-content: center; --swiper-navigation-size: 14px;"></div>
                        </div>
                    </div>
                </div>
                
                <script>
                    document.addEventListener('DOMContentLoaded', function() {{
                        const container = document.getElementById('recent-products-wrapper');
                        if (container) {{
                            let items = [];
                            try {{
                                items = JSON.parse(localStorage.getItem('mewRecent')) || [];
                            }} catch(e) {{}}
                            
                            if (items.length === 0) {{
                                items = [
                                    {{
                                        name: 'ASUS NUC AI 350 (PN54)',
                                        img: '//bizweb.dktcdn.net/thumb/large/100/543/817/products/mini-pc-asus-nuc-ai-350-pn54-ryzen-ai-7-350-gaming.jpg?v=1763971973973',
                                        price: '12.390.000đ',
                                        url: 'demo_product.html'
                                    }},
                                    {{
                                        name: 'MINISFORUM UM890 Pro',
                                        img: '//bizweb.dktcdn.net/thumb/large/100/543/817/products/mini-pc-minisforum-um890-pro-ai-r9-8945hs-gaming-do-hoa.jpg?v=1761015394420',
                                        price: '14.990.000đ',
                                        url: 'demo_product.html'
                                    }},
                                    {{
                                        name: 'GMKTEC NucBox K6 (Ryzen 7 7840HS)',
                                        img: 'https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_1.png',
                                        price: '14.200.000đ',
                                        url: 'demo_product.html'
                                    }}
                                ];
                            }}
                            
                            let html = '';
                            items.forEach(item => {{
                                const name = item.name || item.title || item;
                                const img = item.img || item.image || '//bizweb.dktcdn.net/thumb/large/100/543/817/products/mini-pc-asus-nuc-ai-350-pn54-ryzen-ai-7-350-gaming.jpg?v=1763971973973';
                                const price = item.price || 'Liên hệ';
                                const url = item.url || 'demo_product.html';
                                
                                html += `
                                    <div class="swiper-slide" style="height: auto;">
                                        <div class="product-card" style="border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 15px; background: white; text-align: center; height: 100%; display: flex; flex-direction: column; justify-content: space-between; transition: 0.3s; box-sizing: border-box;" onmouseover="this.style.borderColor='var(--primary)'; this.style.boxShadow='0 8px 20px rgba(0,0,0,0.05)'" onmouseout="this.style.borderColor='var(--border-color)'; this.style.boxShadow='none'">
                                            <a href="${{url}}" style="text-decoration: none; display: block; margin-bottom: 10px;">
                                                <img src="${{img}}" style="width: 100px; height: 100px; object-fit: contain; margin: 0 auto;">
                                            </a>
                                            <a href="${{url}}" style="text-decoration: none; color: var(--text-dark); font-weight: 700; font-size: 0.9rem; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; height: 2.7em; margin-bottom: 8px; line-height: 1.35;">${{name}}</a>
                                            <div style="color: var(--primary); font-weight: 800; font-size: 1rem; margin-bottom: 10px;">${{price}}</div>
                                            <a href="${{url}}" class="btn-pill btn-blue" style="padding: 6px 12px; font-size: 0.8rem; border-radius: 6px; text-decoration: none; font-weight: 700; display: inline-block; box-shadow: none !important;">Xem chi tiết</a>
                                        </div>
                                    </div>
                                `;
                            }});
                            container.innerHTML = html;
                            
                            const swiperRecent = new Swiper('.js-recent-slider', {{
                                slidesPerView: 2,
                                spaceBetween: 15,
                                navigation: {{
                                    nextEl: '.recent-next',
                                    prevEl: '.recent-prev',
                                }},
                                breakpoints: {{
                                    576: {{ slidesPerView: 2 }},
                                    768: {{ slidesPerView: 3 }},
                                    992: {{ slidesPerView: 4 }}
                                }}
                            }});
                            
                            function updateRecentNavVisibility() {{
                                const swiperEl = document.querySelector('.js-recent-slider');
                                if (swiperEl) {{
                                    const prevBtn = swiperEl.querySelector('.recent-prev');
                                    const nextBtn = swiperEl.querySelector('.recent-next');
                                    if (prevBtn && nextBtn) {{
                                        let currentSlidesPerView = 2;
                                        const width = window.innerWidth;
                                        if (width >= 992) currentSlidesPerView = 4;
                                        else if (width >= 768) currentSlidesPerView = 3;
                                        else if (width >= 576) currentSlidesPerView = 2;
                                        
                                        if (items.length <= currentSlidesPerView) {{
                                            prevBtn.style.setProperty('display', 'none', 'important');
                                            nextBtn.style.setProperty('display', 'none', 'important');
                                        }} else {{
                                            prevBtn.style.removeProperty('display');
                                            nextBtn.style.removeProperty('display');
                                        }}
                                    }}
                                }}
                            }}
                            updateRecentNavVisibility();
                            swiperRecent.on('resize', updateRecentNavVisibility);
                            swiperRecent.on('update', updateRecentNavVisibility);
                        }}
                    }});
                </script>
            </div>
        </div>
    </div>
</div>
"""

# 2. CHANGE PASSWORD
change_pass_content = f"""
{custom_styles}
<div class="dashboard-container">
    <div class="dashboard-grid">
        {sidebar}
        <div class="dashboard-main-wrapper">
            <div class="dashboard-content">
                <div class="content-header">
                    <h1 class="content-title"><i class="ph-fill ph-lock-key" style="color: var(--primary);"></i> Đổi mật khẩu</h1>
                </div>
                
                <div style="max-width: 500px;">
                    <p style="color: var(--text-gray); margin-bottom: 25px; line-height: 1.5;">Để đảm bảo tính bảo mật, vui lòng đặt mật khẩu với ít nhất 8 kí tự bao gồm chữ cái và số.</p>
                    
                    <form>
                        <div class="form-group-nava">
                            <label>Mật khẩu cũ <span class="text-danger">*</span></label>
                            <input type="password" class="input-nava" required placeholder="Nhập mật khẩu hiện tại">
                        </div>
                        <div class="form-group-nava">
                            <label>Mật khẩu mới <span class="text-danger">*</span></label>
                            <input type="password" class="input-nava" required placeholder="Nhập mật khẩu mới">
                        </div>
                        <div class="form-group-nava" style="margin-bottom: 30px;">
                            <label>Xác nhận lại mật khẩu <span class="text-danger">*</span></label>
                            <input type="password" class="input-nava" required placeholder="Nhập lại mật khẩu mới">
                        </div>
                        <button type="button" class="btn-nava btn-nava-primary" onclick="alert('Đã cập nhật mật khẩu thành công!')">Cập nhật mật khẩu</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
"""

# 3. ADDRESSES
addresses_content = f"""
{custom_styles}
<div class="dashboard-container">
    <div class="dashboard-grid">
        {sidebar}
        <div class="dashboard-main-wrapper">
            <div class="dashboard-content">
                <div class="content-header" style="flex-wrap: wrap; gap: 15px;">
                    <h1 class="content-title"><i class="ph-fill ph-map-pin" style="color: var(--primary);"></i> Sổ địa chỉ</h1>
                    <button class="btn-nava btn-nava-primary" onclick="openAddAddressModal()"><i class="ph-bold ph-plus"></i> Thêm địa chỉ mới</button>
                </div>
                
                <div class="address-list">
                    <div class="address-card default">
                        <div class="address-actions">
                            <button title="Sửa"><i class="ph-bold ph-pencil-simple"></i></button>
                        </div>
                        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
                            <h3 style="margin: 0; font-size: 1.1rem; font-weight: 800; color: var(--text-dark);">Turnio Dev</h3>
                            <span class="badge-status badge-success">Mặc định</span>
                        </div>
                        <div style="color: var(--text-gray); font-size: 0.95rem; margin-bottom: 8px; display: flex; align-items: center; gap: 8px;">
                            <i class="ph-fill ph-phone" style="font-size: 1.1rem; color: var(--text-dark);"></i> 0378859736
                        </div>
                        <div style="color: var(--text-gray); font-size: 0.95rem; display: flex; align-items: flex-start; gap: 8px; line-height: 1.5;">
                            <i class="ph-fill ph-map-pin-line" style="font-size: 1.1rem; color: var(--text-dark); margin-top: 3px;"></i> 
                            <span>123 Đường Nguyễn Văn Linh, Phường Tân Phong, Quận 7, TP. Hồ Chí Minh</span>
                        </div>
                    </div>

                    <div class="address-card">
                        <div class="address-actions">
                            <button title="Sửa"><i class="ph-bold ph-pencil-simple"></i></button>
                            <button title="Xóa" class="delete"><i class="ph-bold ph-trash"></i></button>
                        </div>
                        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
                            <h3 style="margin: 0; font-size: 1.1rem; font-weight: 800; color: var(--text-dark);">Công ty TNHH Turnio</h3>
                        </div>
                        <div style="color: var(--text-gray); font-size: 0.95rem; margin-bottom: 8px; display: flex; align-items: center; gap: 8px;">
                            <i class="ph-fill ph-phone" style="font-size: 1.1rem; color: var(--text-dark);"></i> 0909123456
                        </div>
                        <div style="color: var(--text-gray); font-size: 0.95rem; display: flex; align-items: flex-start; gap: 8px; line-height: 1.5;">
                            <i class="ph-fill ph-map-pin-line" style="font-size: 1.1rem; color: var(--text-dark); margin-top: 3px;"></i> 
                            <span>Tòa nhà Bitexco Financial Tower, Số 2 Hải Triều, Quận 1, TP. Hồ Chí Minh</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Modal Thêm địa chỉ -->
<div class="modal-overlay-nava" id="addressModal">
    <div class="modal-content-nava">
        <div class="modal-header-nava">
            <h3 class="modal-title-nava">Thêm địa chỉ mới</h3>
            <button class="modal-close-nava" onclick="document.getElementById('addressModal').classList.remove('active')"><i class="ph ph-x"></i></button>
        </div>
        <div class="modal-body-nava">
            <div style="display: flex; flex-wrap: wrap; margin: 0 -10px;">
                <div class="form-group-nava" style="flex: 1; padding: 0 10px; min-width: 200px;">
                    <label>Họ và tên</label>
                    <input type="text" class="input-nava" placeholder="Nhập họ và tên">
                </div>
                <div class="form-group-nava" style="flex: 1; padding: 0 10px; min-width: 200px;">
                    <label>Số điện thoại</label>
                    <input type="tel" class="input-nava" placeholder="Nhập số điện thoại">
                </div>
            </div>
            <div class="form-group-nava">
                <label>Khu vực</label>
                <div class="input-nava" style="cursor: pointer; display: flex; align-items: center; gap: 10px; background: #fff; min-height: 52px; user-select: none;">
                    <i class="ph-bold ph-map-pin" style="color: #0284c7; font-size: 1.1rem; flex-shrink: 0;"></i>
                    <span id="regionDisplay" style="flex: 1; font-weight: 600; color: var(--text-gray); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; pointer-events: none;">Chọn Tỉnh/Thành, Phường/Xã</span>
                    <i class="ph-bold ph-caret-down" style="color: var(--text-gray); flex-shrink: 0;"></i>
                </div>
            </div>
            <div class="form-group-nava" id="specificAddressGroup" style="display: none;">
                <label>Địa chỉ cụ thể</label>
                <input type="text" id="specificAddressInput" class="input-nava" placeholder="Nhập số nhà, tên đường cụ thể...">
            </div>
            <div class="form-group-nava" style="display: flex; align-items: center; gap: 12px; margin-bottom: 0;">
                <label class="toggle-switch-nava">
                    <input type="checkbox" id="defaultAddress">
                    <span class="toggle-slider-nava"></span>
                </label>
                <label for="defaultAddress" style="margin: 0; font-weight: 500; cursor: pointer; color: var(--text-dark);">Đặt làm địa chỉ mặc định</label>
            </div>
        </div>
        <div class="modal-footer-nava">
            <button class="btn-nava" style="background: #f1f5f9; color: var(--text-dark);" onclick="document.getElementById('addressModal').classList.remove('active')">Hủy</button>
            <button class="btn-nava btn-nava-primary">Thêm mới</button>
        </div>
    </div>
</div>

<!-- Modal Chọn Khu vực -->
<div class="modal-overlay-nava" id="regionModal" style="z-index: 10000;">
    <div class="modal-content-nava" style="max-width: 500px; height: 70vh; max-height: 70vh; display: flex; flex-direction: column;">
        <div class="modal-header-nava" style="padding: 15px 25px; flex-shrink: 0;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <button id="btnBackRegion" style="display: none; background: none; border: none; font-size: 1.2rem; cursor: pointer; color: var(--text-gray);"><i class="ph-bold ph-arrow-left"></i></button>
                <h3 class="modal-title-nava" id="regionModalTitle" style="font-size: 1.1rem; margin: 0;">Chọn Tỉnh / Thành phố</h3>
            </div>
            <button class="modal-close-nava" onclick="document.getElementById('regionModal').classList.remove('active')"><i class="ph ph-x"></i></button>
        </div>
        <div class="modal-search-nava" style="flex-shrink: 0; padding: 15px 25px; border-bottom: 1px solid var(--border-color); background: #fff;">
            <input type="text" id="regionSearchInput" class="input-nava" placeholder="Tìm kiếm..." style="background: #f1f5f9;">
        </div>
        <div class="modal-body-nava" style="padding: 0; overflow-y: auto; flex-grow: 1;">
            <div id="regionList">
                <div style="padding: 20px; text-align: center; color: var(--text-gray);">Đang tải dữ liệu...</div>
            </div>
        </div>
        <div class="modal-footer-nava" id="regionModalFooter" style="display: none; justify-content: flex-start; padding: 15px 25px; flex-shrink: 0; border-top: 1px solid var(--border-color); background: #fff;">
            <button class="btn-nava" id="btnBackRegionFooter" style="display: flex; align-items: center; gap: 6px; background: #f1f5f9; border: 1px solid var(--border-color); padding: 8px 16px; border-radius: 8px; font-weight: 600; cursor: pointer; color: var(--text-dark);"><i class="ph-bold ph-arrow-left"></i> Quay lại</button>
        </div>
    </div>
</div>

<script>
    let locationData = null;
    let addressStep = 1;
    let selectedCity = null;
    let searchQuery = '';

    // Fetch data
    fetch('/assets/ctiy.json')
        .then(res => res.json())
        .then(data => {{
            locationData = data;
        }})
        .catch(err => console.error("Could not load ctiy.json", err));

    function getCleanCityName(name) {{
        const match = name.match(/\[(.*?)\]/);
        return match ? match[1] : name.replace(/\s*\(.*?\)\s*/g, '').trim();
    }}

    function openAddAddressModal() {{
        document.getElementById('specificAddressGroup').style.display = 'none';
        document.getElementById('specificAddressInput').value = '';
        document.getElementById('regionDisplay').innerText = 'Chọn Tỉnh/Thành, Phường/Xã';
        document.getElementById('regionDisplay').style.color = 'var(--text-gray)';
        document.getElementById('addressModal').classList.add('active');
    }}

    // Open Modal
    document.getElementById('regionDisplay').parentElement.addEventListener('click', function() {{
        if (!locationData) return alert("Dữ liệu đang tải, vui lòng thử lại sau.");
        addressStep = 1;
        selectedCity = null;
        document.getElementById('regionSearchInput').value = '';
        searchQuery = '';
        renderRegionList();
        document.getElementById('regionModal').classList.add('active');
    }});

    function renderRegionList() {{
        const list = document.getElementById('regionList');
        if (!list) return;
        list.innerHTML = '';

        const titleEl = document.getElementById('regionModalTitle');
        const footerEl = document.getElementById('regionModalFooter');
        const backHeaderBtn = document.getElementById('btnBackRegion');

        if (addressStep === 1) {{
            titleEl.innerText = 'Chọn Tỉnh / Thành phố';
            footerEl.style.display = 'none';
            backHeaderBtn.style.display = 'none';

            const filteredCities = locationData.cities.filter(c => {{
                const clean = getCleanCityName(c.name).toLowerCase();
                const raw = c.name.toLowerCase();
                return clean.includes(searchQuery) || raw.includes(searchQuery);
            }});

            if (filteredCities.length === 0) {{
                list.innerHTML = '<div style="padding: 20px; text-align: center; color: var(--text-gray);">Không tìm thấy</div>';
                return;
            }}

            filteredCities.forEach(c => {{
                const div = document.createElement('div');
                div.className = 'list-item';
                div.innerHTML = `<span>${{getCleanCityName(c.name)}}</span> <i class="ph-bold ph-caret-right" style="color: var(--text-gray)"></i>`;
                div.onclick = () => {{
                    addressStep = 2;
                    selectedCity = c;
                    document.getElementById('regionSearchInput').value = '';
                    searchQuery = '';
                    renderRegionList();
                }};
                list.appendChild(div);
            }});
        }} else if (addressStep === 2) {{
            titleEl.innerText = 'Chọn Quận / Huyện / Xã';
            footerEl.style.display = 'flex';
            backHeaderBtn.style.display = 'block';

            const cleanCityName = getCleanCityName(selectedCity.name);
            let filteredWards = locationData.wards.filter(w => w.city === cleanCityName);

            if (searchQuery) {{
                filteredWards = filteredWards.filter(w => 
                    w.wnew.toLowerCase().includes(searchQuery) || 
                    (w.wold && w.wold.toLowerCase().includes(searchQuery))
                );
            }}

            if (filteredWards.length === 0) {{
                list.innerHTML = '<div style="padding: 20px; text-align: center; color: var(--text-gray);">Không tìm thấy</div>';
                return;
            }}

            filteredWards.forEach(w => {{
                const div = document.createElement('div');
                div.className = 'list-item';
                div.innerHTML = `<div><span>${{w.wnew}}</span>${{w.wold && w.wold !== w.wnew ? `<div class="list-item-sub">(Cũ: ${{w.wold}})</div>` : ''}}</div> <i class="ph-bold ph-check" style="color:transparent"></i>`;
                div.onclick = () => {{
                    finishSelection(w.wnew);
                }};
                list.appendChild(div);
            }});
        }}
    }}

    function goBack() {{
        addressStep = 1;
        selectedCity = null;
        document.getElementById('regionSearchInput').value = '';
        searchQuery = '';
        renderRegionList();
    }}

    document.getElementById('btnBackRegion').addEventListener('click', goBack);
    document.getElementById('btnBackRegionFooter').addEventListener('click', goBack);

    document.getElementById('regionSearchInput').addEventListener('input', function(e) {{
        searchQuery = e.target.value.toLowerCase().trim();
        renderRegionList();
    }});

    function finishSelection(wardName) {{
        const cleanCityName = getCleanCityName(selectedCity.name);
        const finalString = `${{cleanCityName}}, ${{wardName}}`;
        document.getElementById('regionDisplay').innerText = finalString;
        document.getElementById('regionDisplay').style.color = 'var(--text-dark)';
        document.getElementById('regionModal').classList.remove('active');
        
        // Show specific address input
        document.getElementById('specificAddressGroup').style.display = 'block';
    }}

    // Close modal when clicking outside
    document.getElementById('addressModal').addEventListener('click', function(e) {{
        if(e.target === this) {{
            this.classList.remove('active');
        }}
    }});
    document.getElementById('regionModal').addEventListener('click', function(e) {{
        if(e.target === this) {{
            this.classList.remove('active');
        }}
    }});
</script>
"""

for filename, content, template_name in [
    ("account.html", account_content, "customers"),
    ("change_pass.html", change_pass_content, "customers"),
    ("addresses.html", addresses_content, "addresses")
]:
    full_html = header_part + content + footer_part
    full_html = clean_liquid_tags(full_html, template_name)
    with open(os.path.join(base_dir, filename), "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Generated {filename}")
