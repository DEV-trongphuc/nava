import os

sticky_html = """
<!-- Sticky Compare Bar -->
<style>
    @media (max-width: 768px) {
        #compare-bar-inner { flex-direction: column !important; gap: 12px !important; }
        #compare-slots { flex-direction: column !important; gap: 10px !important; width: 100% !important; }
        #compare-actions { width: 100% !important; justify-content: center !important; }
        #compare-actions button { flex: 1 !important; justify-content: center !important; padding: 10px 15px !important; font-size: 0.95rem !important; }
        .compare-slot-item { padding: 8px 12px !important; }
        .compare-slot-item img { width: 40px !important; height: 40px !important; }
    }
</style>
<div id="compare-bar" style="font-family: system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'; --primary: #1e3a8a; --bg-white: #ffffff; --bg-gray: #f8fafc; --text-color: #0f172a; --text-gray: #64748b; --border-color: #e2e8f0; --radius-lg: 16px; position: fixed !important; bottom: 0 !important; left: 0 !important; width: 100% !important; z-index: 2147483647 !important; display: none; background: var(--bg-white) !important; box-shadow: 0 -10px 50px rgba(0,0,0,0.15) !important; border-top: 1px solid var(--border-color) !important; padding: 25px 0 !important;">
    <!-- Nút X tắt nhanh -->
    <button onclick="hideCompareBar()" style="position: absolute; top: -18px; right: 25px; width: 36px; height: 36px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-gray); box-shadow: 0 4px 10px rgba(0,0,0,0.1); cursor: pointer; display: flex; align-items: center; justify-content: center; z-index: 10; transition: all 0.2s;" onmouseover="this.style.color='#ef4444'; this.style.borderColor='#ef4444'" onmouseout="this.style.color='var(--text-gray)'; this.style.borderColor='var(--border-color)'"><i class="ph-bold ph-x" style="font-size: 1.1rem;"></i></button>

    <!-- Nút mũi tên kéo lên -->
    <button id="compare-expand" onclick="executeCompare(true)" disabled style="position: absolute; top: -24px; left: 50%; transform: translateX(-50%); width: 70px; height: 25px; border-radius: 12px 12px 0 0; background: var(--primary); border: none; color: white; cursor: not-allowed; display: flex; align-items: center; justify-content: center; z-index: 10; transition: all 0.2s; box-shadow: 0 -4px 10px rgba(14,165,233,0.3); opacity: 0.5;"><i class="ph-bold ph-caret-up" style="font-size: 1.3rem;"></i></button>

    <div id="compare-bar-inner" style="max-width: 1200px; margin: 0 auto; padding: 0 15px; display: flex; align-items: center; justify-content: space-between; gap: 20px; width: 100%; box-sizing: border-box; position: relative;">
        <div style="display: flex; align-items: center; gap: 20px; flex: 1; width: 100%;">
            <div id="compare-slots" style="display: flex; gap: 20px; flex: 1;">
                <!-- Slots populated by JS -->
            </div>
        </div>
        <div id="compare-actions" style="display: flex; flex-shrink: 0; min-width: 180px;">
            <button id="compare-submit" onclick="executeCompare()" disabled style="width: 100%; justify-content: center; padding: 12px 50px; border-radius: 10px; border: none; background: var(--primary); color: white; font-size: 1.05rem; font-weight: 700; cursor: not-allowed; opacity: 0.5; transition: all 0.2s; box-shadow: 0 4px 15px rgba(14,165,233,0.3); display: flex; align-items: center; gap: 8px; font-family: inherit; white-space: nowrap;"><i class="ph-bold ph-magic-wand"></i> So sánh ngay</button>
        </div>
        
        <!-- COMPARE PRODUCT SELECT MODAL -->
        <div id="compare-select-modal" style="display: none; position: fixed !important; inset: 0 !important; z-index: 2147483646 !important; background: rgba(15, 23, 42, 0.6) !important; backdrop-filter: blur(4px) !important; align-items: center; justify-content: center; opacity: 0; transition: opacity 0.25s ease;" onclick="if(event.target===this) hideCompareSelectDropdown()">
            <div id="compare-select-dropdown" style="background: var(--bg-white, #ffffff); border: 1px solid var(--border-color); border-radius: 16px; box-shadow: 0 20px 50px rgba(0,0,0,0.2); width: 90%; max-width: 850px; padding: 25px; box-sizing: border-box; font-family: inherit; position: relative; display: flex; flex-direction: column; transform: scale(0.95); transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);">
                <div style="font-weight: 800; font-size: 1.1rem; color: var(--text-dark); margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center;">
                    <span>Chọn sản phẩm so sánh</span>
                    <button onclick="hideCompareSelectDropdown()" style="background: none; border: none; color: var(--text-gray); cursor: pointer; font-size: 1.3rem; display: flex; align-items: center; justify-content: center; padding: 4px;" onmouseover="this.style.color='#ef4444'" onmouseout="this.style.color='var(--text-gray)'"><i class="ph ph-x"></i></button>
                </div>
                <div style="margin-bottom: 15px; position: relative;">
                    <input type="text" id="compare-search-input" oninput="filterCompareProducts()" placeholder="Nhập tên sản phẩm cần so sánh..." style="width: 100%; padding: 10px 14px 10px 38px; border: 1px solid var(--border-color); border-radius: 8px; font-size: 0.9rem; outline: none; box-sizing: border-box; font-family: inherit; background: var(--bg-gray); transition: all 0.2s; color: var(--text-dark);" onfocus="this.style.borderColor='var(--primary)'; this.style.background='var(--bg-white)';" onblur="this.style.borderColor='var(--border-color)'; this.style.background='var(--bg-gray)'">
                    <i class="ph ph-magnifying-glass" style="position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: var(--text-gray); font-size: 1.1rem; pointer-events: none;"></i>
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 12px; max-height: 420px; overflow-y: auto; padding-right: 4px;" id="compare-select-list">
                    <!-- JS populated product items -->
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Comparison Modal -->
<div id="compare-modal" style="font-family: system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'; --primary: #1e3a8a; --bg-white: #ffffff; --bg-gray: #f8fafc; --text-color: #0f172a; --text-gray: #64748b; --border-color: #e2e8f0; --radius-lg: 16px; position: fixed !important; inset: 0 !important; z-index: 2147483647 !important; background: rgba(15,23,42,0.8) !important; backdrop-filter: blur(8px) !important; display: none; align-items: center; justify-content: center; opacity: 0; transition: opacity 0.3s ease;">
    <div style="background: var(--bg-white); width: 95%; max-width: 1100px; max-height: 90vh; border-radius: var(--radius-lg); border: 1px solid var(--border-color); box-shadow: 0 25px 50px rgba(0,0,0,0.25); display: flex; flex-direction: column; overflow: hidden; position: relative; transform: scale(0.95); transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);" id="compare-modal-content">
        <!-- Header -->
        <div style="padding: 25px 30px; border-bottom: 1px solid var(--border-color); display: flex; justify-content: space-between; align-items: center; background: var(--bg-gray);">
            <h3 style="margin: 0; font-size: 1.4rem; font-weight: 800; color: var(--text-dark); display: flex; align-items: center; gap: 12px;"><i class="ph-fill ph-scales" style="color: var(--primary); font-size: 1.6rem;"></i> Phân Tích & Đối Chiếu</h3>
            <button onclick="closeCompareModal()" style="width: 40px; height: 40px; border-radius: 50%; background: var(--bg-white); border: 1px solid var(--border-color); color: var(--text-dark); cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.2s;" onmouseover="this.style.borderColor='#ef4444'; this.style.color='#ef4444'" onmouseout="this.style.borderColor='var(--border-color)'; this.style.color='var(--text-dark)'"><i class="ph ph-x" style="font-size: 1.3rem;"></i></button>
        </div>
        <!-- Body -->
        <div id="compare-body" style="padding: 35px; overflow-y: auto; flex: 1;">
            <!-- Loading State -->
            <div id="compare-loading" style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 50px 0;">
                <div style="position: relative; width: 70px; height: 70px; display: flex; align-items: center; justify-content: center; margin-bottom: 25px;">
                    <div style="position: absolute; inset: 0; border: 3px solid transparent; border-top-color: var(--primary); border-bottom-color: var(--primary); border-radius: 50%; animation: nava-spin 1.5s linear infinite; opacity: 0.8;"></div>
                    <div style="position: absolute; inset: 5px; border: 3px solid transparent; border-left-color: #38bdf8; border-right-color: #38bdf8; border-radius: 50%; animation: nava-spin-reverse 2s linear infinite; opacity: 0.6;"></div>
                    <div style="font-size: 2.2rem; font-weight: 900; color: var(--primary); font-family: 'Inter', sans-serif; letter-spacing: -1px; text-shadow: 0 0 10px rgba(30,58,138,0.3); z-index: 2;">N</div>
                </div>
                <style>
                    @keyframes nava-spin { 100% { transform: rotate(360deg); } }
                    @keyframes nava-spin-reverse { 100% { transform: rotate(-360deg); } }
                </style>
                <h4 style="margin: 0 0 10px 0; font-size: 1.3rem; font-weight: 700; color: var(--text-dark);">Nava Store đang xử lý dữ liệu...</h4>
                <p style="color: var(--text-gray); margin: 0; font-size: 1.05rem;">Vui lòng đợi trong giây lát để hệ thống đối chiếu thông số.</p>
            </div>
            <!-- Result State -->
            <div id="compare-result" style="display: none;">
                <!-- Injected via JS -->
            </div>
        </div>
    </div>
</div>

<!-- Comparison Logic -->
<script>
    // Ensure the sticky bar and modal are direct children of document.documentElement (HTML tag)
    document.addEventListener("DOMContentLoaded", function() {
        const cb = document.getElementById('compare-bar');
        const cm = document.getElementById('compare-modal');
        if (cb && cb.parentNode !== document.documentElement) { document.documentElement.appendChild(cb); }
        if (cm && cm.parentNode !== document.documentElement) { document.documentElement.appendChild(cm); }
    });

    var compareList = [];
    
    function toggleCompare(btn, name, img, price) {
        console.log('--- toggleCompare called ---');
        const idx = compareList.findIndex(p => p.name === name);
        if (idx > -1) {
            compareList.splice(idx, 1);
            btn.style.background = 'var(--bg-white)';
            btn.style.color = 'var(--text-dark)';
            btn.querySelector('i').className = 'ph ph-arrows-left-right';
        } else {
            if (compareList.length >= 2) {
                alert('Chỉ có thể so sánh tối đa 2 sản phẩm cùng lúc!');
                return;
            }
            compareList.push({ name, img, price });
            btn.style.background = 'var(--primary)';
            btn.style.color = 'white';
            btn.querySelector('i').className = 'ph-bold ph-check';
        }
        updateCompareBar();
    }
    
    function removeCompare(name) {
        compareList = compareList.filter(p => p.name !== name);
        // Reset buttons
        document.querySelectorAll('.compare-btn').forEach(btn => {
            if (btn.getAttribute('data-name') === name) {
                btn.style.background = 'var(--bg-white)';
                btn.style.color = 'var(--text-dark)';
                btn.querySelector('i').className = 'ph ph-arrows-left-right';
            }
        });
        updateCompareBar();
    }
    
    function clearCompare() {
        compareList = [];
        document.querySelectorAll('.compare-btn').forEach(btn => {
            btn.style.background = 'var(--bg-white)';
            btn.style.color = 'var(--text-dark)';
            btn.querySelector('i').className = 'ph ph-arrows-left-right';
        });
        updateCompareBar();
        if(typeof showToast === 'function') {
            showToast('Đã xóa tất cả sản phẩm khỏi danh sách đối chiếu');
        }
    }
    function hideCompareBar() {
        const bar = document.getElementById('compare-bar');
        bar.style.setProperty('display', 'none', 'important');
    }

    function updateCompareBar() {
        const bar = document.getElementById('compare-bar');
        const slots = document.getElementById('compare-slots');
        const submitBtn = document.getElementById('compare-submit');
        const expandBtn = document.getElementById('compare-expand');
        
        // Hide compare bar if bottom sheet is currently open
        const bs = document.getElementById('nava-bottom-sheet');
        const isBsOpen = bs && (bs.classList.contains('open') || bs.style.display === 'flex');
        
        if (compareList.length > 0 && !isBsOpen) {
            bar.style.setProperty('display', 'block', 'important');
        } else {
            bar.style.setProperty('display', 'none', 'important');
        }
        
        if (compareList.length === 2) {
            submitBtn.disabled = false;
            submitBtn.style.cursor = 'pointer';
            submitBtn.style.opacity = '1';
            expandBtn.disabled = false;
            expandBtn.style.cursor = 'pointer';
            expandBtn.style.opacity = '1';
        } else {
            submitBtn.disabled = true;
            submitBtn.style.cursor = 'not-allowed';
            submitBtn.style.opacity = '0.5';
            expandBtn.disabled = true;
            expandBtn.style.cursor = 'not-allowed';
            expandBtn.style.opacity = '0.5';
        }
        
        let html = '';
        for (let i = 0; i < 2; i++) {
            if (i > 0) {
                html += `
                    <div style="display: flex; align-items: center; justify-content: center; font-weight: 800; color: white; background: var(--primary); font-size: 0.75rem; width: 26px; height: 26px; border-radius: 50%; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin: 0 -5px; z-index: 2; align-self: center; flex-shrink: 0; user-select: none;">VS</div>
                `;
            }
            if (i < compareList.length) {
                const p = compareList[i];
                let displayPrice = p.price;
                if (!displayPrice || displayPrice === 0 || displayPrice === '0' || displayPrice === '0đ' || displayPrice === '0₫' || (typeof displayPrice === 'string' && (displayPrice.trim() === '0đ' || displayPrice.trim() === '0₫' || displayPrice.trim() === '0' || displayPrice.trim().startsWith('0')))) {
                    displayPrice = 'Liên hệ';
                }
                const escapedNameForAttr = p.name.replace(/"/g, '&quot;');
                html += `
                    <div class="compare-slot-item" style="display: flex; align-items: center; gap: 15px; background: var(--bg-gray); padding: 10px 15px; border-radius: 12px; border: 1px solid var(--border-color); flex: 1; max-width: 380px; min-width: 0; position: relative; font-family: inherit; box-sizing: border-box;">
                        <img src="${p.img}" style="width: 55px; height: 55px; object-fit: contain; background: var(--bg-white); border-radius: 6px; padding: 3px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                        <div style="flex: 1; min-width: 0; text-align: left;">
                            <div style="font-size: 0.85rem; font-weight: 700; color: var(--text-dark); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-bottom: 4px;" title="${escapedNameForAttr}">${p.name}</div>
                            <div style="font-size: 1.05rem; font-weight: 800; color: var(--primary);">${displayPrice}</div>
                        </div>
                        <button onclick="removeCompare('${p.name}')" style="background: none; border: none; color: var(--text-gray); cursor: pointer; padding: 5px; display: flex; font-size: 1.2rem; transition: color 0.2s;" onmouseover="this.style.color='#ef4444'" onmouseout="this.style.color='var(--text-gray)'"><i class="ph-bold ph-x"></i></button>
                    </div>
                `;
            } else {
                html += `
                    <div class="compare-slot-item" onclick="showCompareSelectDropdown(event, this)" style="display: flex; align-items: center; justify-content: center; gap: 10px; background: transparent; padding: 10px 15px; border-radius: 12px; border: 1px dashed var(--border-color); flex: 1; max-width: 380px; min-width: 0; color: var(--text-gray); font-size: 0.95rem; font-family: inherit; cursor: pointer; box-sizing: border-box;">
                        <div style="width: 45px; height: 45px; border-radius: 50%; background: var(--bg-gray); display: flex; align-items: center; justify-content: center;"><i class="ph ph-plus" style="font-size: 1.2rem;"></i></div>
                        Thêm sản phẩm
                    </div>
                `;
            }
        }
        slots.innerHTML = html;
    }
    
    var allProductsForCompare = [
        { name: 'ASUS NUC AI 350', img: '//bizweb.dktcdn.net/thumb/large/100/543/817/products/mini-pc-asus-nuc-ai-350-pn54-ryzen-ai-7-350-gaming.jpg?v=1763971973973', price: '12.390.000đ' },
        { name: 'MINISFORUM UM890 Pro', img: '//bizweb.dktcdn.net/thumb/large/100/543/817/products/mini-pc-minisforum-um890-pro-ai-r9-8945hs-gaming-do-hoa.jpg?v=1761015394420', price: '14.990.000đ' },
        { name: 'GMKTEC NucBox K6 (Ryzen 7 7840HS)', img: 'https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_3_1.png', price: '14.200.000đ' },
        { name: 'ASUS NUC 14 Essential Intel', img: '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png', price: '4.490.000đ' },
        { name: 'Mini PC GMK EVO X1 32G', img: '//bizweb.dktcdn.net/thumb/large/100/543/817/products/mini-pc-gmk-evo-x1-ai.jpg', price: '31.190.000đ' },
        { name: 'AtomMan G7 PT Mini PC', img: '//bizweb.dktcdn.net/100/543/817/themes/1000289/assets/collec_img_2_1.png', price: '34.490.000đ' }
    ];

    function showCompareSelectDropdown(event, slotElement) {
        if(event) event.stopPropagation();
        
        // Close bottom sheet if open
        if (typeof closeBottomSheet === 'function') {
            closeBottomSheet();
        }
        
        const modal = document.getElementById('compare-select-modal');
        const modalContent = document.getElementById('compare-select-dropdown');
        const searchInput = document.getElementById('compare-search-input');
        if (searchInput) searchInput.value = '';
        
        if (modal && modalContent) {
            modal.style.setProperty('display', 'flex', 'important');
            // Trigger reflow
            void modal.offsetWidth;
            modal.style.opacity = '1';
            modalContent.style.transform = 'scale(1)';
        }
        
        filterCompareProducts();
        
        // Auto-focus search input
        setTimeout(() => {
            if (searchInput) searchInput.focus();
        }, 100);
    }

    function filterCompareProducts() {
        const query = document.getElementById('compare-search-input')?.value.toLowerCase().trim() || '';
        const listContainer = document.getElementById('compare-select-list');
        if (!listContainer) return;
        
        // Filter out products already in compare list
        let available = allProductsForCompare.filter(p => !compareList.some(item => item.name === p.name));
        
        let displayList = available;
        if (query) {
            displayList = available.filter(p => p.name.toLowerCase().includes(query));
        } else {
            displayList = available.slice(0, 6);
        }
        
        let html = '';
        displayList.forEach(p => {
            html += `
                <div onclick="selectProductForCompare('${p.name}', '${p.img}', '${p.price}')" style="display: flex; align-items: center; gap: 10px; padding: 8px; border: 1px solid var(--border-color); border-radius: 8px; cursor: pointer; transition: all 0.2s;" onmouseover="this.style.borderColor='var(--primary)'; this.style.background='var(--bg-gray)';" onmouseout="this.style.borderColor='var(--border-color)'; this.style.background='transparent';">
                    <img src="${p.img}" style="width: 40px; height: 40px; object-fit: contain; background: white;">
                    <div style="flex: 1; min-width: 0; text-align: left;">
                        <div style="font-size: 0.85rem; font-weight: 700; color: var(--text-dark); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${p.name}</div>
                        <div style="font-size: 0.9rem; font-weight: 800; color: var(--primary);">${p.price}</div>
                    </div>
                </div>
            `;
        });
        
        if(available.length === 0) {
            html = '<div style="font-size: 0.85rem; color: var(--text-gray); text-align: center; padding: 15px;">Không tìm thấy sản phẩm phù hợp</div>';
        }
        
        listContainer.innerHTML = html;
    }

    function selectProductForCompare(name, img, price) {
        if (compareList.length >= 2) return;
        compareList.push({ name, img, price });
        updateCompareBar();
        hideCompareSelectDropdown();
    }

    function hideCompareSelectDropdown() {
        const modal = document.getElementById('compare-select-modal');
        const modalContent = document.getElementById('compare-select-dropdown');
        if (modal && modalContent) {
            modal.style.opacity = '0';
            modalContent.style.transform = 'scale(0.95)';
            setTimeout(() => {
                modal.style.setProperty('display', 'none', 'important');
            }, 250);
        }
    }

    function openCompareDrawerDirect(name = 'ASUS NUC AI 350', img = '//bizweb.dktcdn.net/thumb/large/100/543/817/products/mini-pc-asus-nuc-ai-350-pn54-ryzen-ai-7-350-gaming.jpg?v=1763971973973', price = '12.390.000đ') {
        const idx = compareList.findIndex(p => p.name === name);
        if (idx === -1) {
            if (compareList.length >= 2) {
                // Ignore
            } else {
                compareList.push({ name, img, price });
            }
        }
        updateCompareBar();
        
        setTimeout(() => {
            const slots = document.getElementById('compare-slots');
            if (slots && compareList.length < 2) {
                const emptySlot = slots.children[compareList.length];
                if (emptySlot) {
                    showCompareSelectDropdown(null, emptySlot);
                }
            }
        }, 100);
    }
    
    // Close modal on click outside (fallback check)
    document.addEventListener('click', function(e) {
        const modal = document.getElementById('compare-select-modal');
        if (modal && modal.style.display === 'flex' && e.target === modal) {
            hideCompareSelectDropdown();
        }
    });

    function executeCompare(isFullScreen = false) {
        // Close bottom sheet if open
        if (typeof closeBottomSheet === 'function') {
            closeBottomSheet();
        }
        
        const modal = document.getElementById('compare-modal');
        const modalContent = document.getElementById('compare-modal-content');
        const loading = document.getElementById('compare-loading');
        const result = document.getElementById('compare-result');
        
        modal.style.setProperty('display', 'flex', 'important');
        
        if (isFullScreen) {
            modalContent.style.width = '100%';
            modalContent.style.maxWidth = '100%';
            modalContent.style.height = '100vh';
            modalContent.style.maxHeight = '100vh';
            modalContent.style.borderRadius = '0';
            modalContent.style.transform = 'translateY(100vh)';
            
            // Trigger reflow
            void modal.offsetWidth;
            
            modalContent.style.transition = 'transform 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
            modal.style.opacity = '1';
            modalContent.style.transform = 'translateY(0)';
        } else {
            modalContent.style.width = '95%';
            modalContent.style.maxWidth = '1100px';
            modalContent.style.height = 'auto';
            modalContent.style.maxHeight = '90vh';
            modalContent.style.borderRadius = 'var(--radius-lg)';
            modalContent.style.transform = 'scale(0.95)';
            
            // Trigger reflow
            void modal.offsetWidth;
            
            modalContent.style.transition = 'transform 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
            modal.style.opacity = '1';
            modalContent.style.transform = 'scale(1)';
        }
        
        loading.style.display = 'flex';
        result.style.display = 'none';
        
        setTimeout(() => {
            loading.style.display = 'none';
            
            // Generate mock specs based on names
            const getSpecs = (name) => {
                if (name.includes('NUC 14')) return ['Intel Core Ultra 5', 'Intel Arc Graphics', '16GB DDR5 5600MHz', '512GB PCIe Gen4', 'Wi-Fi 6E, Bluetooth 5.3', '4x USB 3.2, 2x Type-C'];
                if (name.includes('AtomMan')) return ['AMD Ryzen 9 7945HX', 'AMD Radeon RX 7600M', '32GB DDR5 5200MHz', '1TB PCIe Gen4', 'Wi-Fi 7, Bluetooth 5.4', 'Dual 2.5G LAN, USB4'];
                if (name.includes('GMK EVO')) return ['AMD Ryzen 7 8845HS', 'Radeon 780M', '32GB DDR5 5600MHz', '1TB PCIe Gen4', 'Wi-Fi 6, Bluetooth 5.2', 'Oculink, Dual 2.5G LAN'];
                if (name.includes('Beelink')) return ['AMD Ryzen 7 8845HS', 'Radeon 780M', '16GB DDR5 5600MHz', '1TB PCIe Gen4', 'Wi-Fi 6, Bluetooth 5.2', 'USB4, 2.5G LAN'];
                return ['Intel Core i5', 'Intel UHD', '16GB DDR4', '512GB SSD', 'Wi-Fi 6', 'USB 3.0'];
            };
            
            const p1 = compareList[0];
            const p2 = compareList[1];
            const specs1 = getSpecs(p1.name);
            const specs2 = getSpecs(p2.name);
            const labels = ['CPU', 'GPU', 'RAM', 'Lưu trữ', 'Kết nối', 'Cổng giao tiếp'];
            
            let tableHtml = `
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 30px;">
                    <div style="text-align: center; padding: 20px; border: 1px solid var(--border-color); border-radius: var(--radius-lg); background: var(--bg-gray);">
                        <img src="${p1.img}" style="width: 150px; height: 150px; object-fit: contain; margin-bottom: 15px; background: var(--bg-white); border-radius: 8px; padding: 10px;">
                        <h4 style="margin: 0 0 10px 0; font-size: 1.1rem; color: var(--text-dark); font-weight: 800;">${p1.name}</h4>
                        <div style="color: var(--primary); font-weight: 800; font-size: 1.3rem;">${p1.price}</div>
                        <a href="demo_product.html" style="display: inline-block; margin-top: 15px; padding: 8px 20px; background: var(--primary); color: white; border-radius: 20px; text-decoration: none; font-weight: 700; font-size: 0.9rem;">Xem chi tiết</a>
                    </div>
                    <div style="text-align: center; padding: 20px; border: 1px solid var(--border-color); border-radius: var(--radius-lg); background: var(--bg-gray);">
                        <img src="${p2.img}" style="width: 150px; height: 150px; object-fit: contain; margin-bottom: 15px; background: var(--bg-white); border-radius: 8px; padding: 10px;">
                        <h4 style="margin: 0 0 10px 0; font-size: 1.1rem; color: var(--text-dark); font-weight: 800;">${p2.name}</h4>
                        <div style="color: var(--primary); font-weight: 800; font-size: 1.3rem;">${p2.price}</div>
                        <a href="demo_product.html" style="display: inline-block; margin-top: 15px; padding: 8px 20px; background: var(--primary); color: white; border-radius: 20px; text-decoration: none; font-weight: 700; font-size: 0.9rem;">Xem chi tiết</a>
                    </div>
                </div>
                
                <div style="background: var(--bg-white); border: 1px solid var(--border-color); border-radius: var(--radius-lg); overflow: hidden;">
            `;
            
            for(let i=0; i<labels.length; i++) {
                const bg = i % 2 === 0 ? 'var(--bg-gray)' : 'var(--bg-white)';
                let s1 = specs1[i], s2 = specs2[i];
                let color1 = 'var(--text-dark)', color2 = 'var(--text-dark)';
                let icon1 = '', icon2 = '';
                
                // Dumb mock logic to make one look better
                if (s1 !== s2 && s1.length > s2.length) {
                    color1 = 'var(--primary)'; icon1 = ' <i class="ph-fill ph-check-circle" style="color:var(--primary)"></i>';
                } else if (s1 !== s2) {
                    color2 = 'var(--primary)'; icon2 = ' <i class="ph-fill ph-check-circle" style="color:var(--primary)"></i>';
                }
                
                tableHtml += `
                    <div style="display: grid; grid-template-columns: 150px 1fr 1fr; border-bottom: 1px solid var(--border-color); background: ${bg};">
                        <div style="padding: 15px 20px; font-weight: 800; color: var(--text-gray); border-right: 1px solid var(--border-color); display: flex; align-items: center;">${labels[i]}</div>
                        <div style="padding: 15px 20px; border-right: 1px solid var(--border-color); font-weight: 600; color: ${color1}; line-height: 1.4;">${s1}${icon1}</div>
                        <div style="padding: 15px 20px; font-weight: 600; color: ${color2}; line-height: 1.4;">${s2}${icon2}</div>
                    </div>
                `;
            }
            
            tableHtml += `
                </div>
                
                <div style="margin-top: 30px; padding: 20px; background: linear-gradient(135deg, rgba(14,165,233,0.05), rgba(15,23,42,0.02)); border-radius: var(--radius-lg); border: 1px solid rgba(14,165,233,0.2); display: flex; gap: 15px;">
                    <i class="ph-fill ph-storefront" style="color: var(--primary); font-size: 2rem;"></i>
                    <div>
                        <h4 style="margin: 0 0 5px 0; color: var(--text-dark); font-weight: 800;">Đề xuất từ Nava Store</h4>
                        <p style="margin: 0; color: var(--text-gray); line-height: 1.5;">Nếu bạn ưu tiên hiệu năng mạnh mẽ để chơi game hoặc làm đồ họa nặng, <strong>${p1.price > p2.price ? p1.name : p2.name}</strong> là lựa chọn tốt hơn. Tuy nhiên, nếu bạn cần sự nhỏ gọn và mức giá tối ưu, <strong>${p1.price <= p2.price ? p1.name : p2.name}</strong> sẽ rất phù hợp.</p>
                    </div>
                </div>
            `;
            
            result.innerHTML = tableHtml;
            result.style.display = 'block';
        }, 1200);
    }
    
    function closeCompareModal() {
        const modal = document.getElementById('compare-modal');
        const modalContent = document.getElementById('compare-modal-content');
        modal.style.opacity = '0';
        if (modalContent.style.width === '100%') {
            modalContent.style.transform = 'translateY(100vh)';
        } else {
            modalContent.style.transform = 'scale(0.95)';
        }
        setTimeout(() => {
            modal.style.setProperty('display', 'none', 'important');
        }, 300);
    }
</script>
"""

file_path = 'demo_collection.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

if "<!-- Sticky Compare Bar -->" in content:
    # Always update existing sticky bar with the latest code
    parts = content.split("<!-- Sticky Compare Bar -->")
    content = parts[0] + "</body>"

content = content.replace('</body>', sticky_html + '\n</body>')
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Successfully updated/injected sticky bar in demo_collection.html")
