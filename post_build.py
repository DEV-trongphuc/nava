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
        <div id="compare-select-modal" style="display: none; position: fixed !important; inset: 0 !important; z-index: 2147483648 !important; background: rgba(15, 23, 42, 0.6) !important; backdrop-filter: blur(4px) !important; align-items: center; justify-content: center; opacity: 0; transition: opacity 0.25s ease;" onclick="if(event.target===this) hideCompareSelectDropdown()">
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
