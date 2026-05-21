
    // Ensure the sticky bar and modal are direct children of document.documentElement (HTML tag)
    // This perfectly bypasses ANY transform or overflow bugs on the BODY tag!
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
        
        if (compareList.length > 0) {
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
            if (i < compareList.length) {
                const p = compareList[i];
                html += `
                    <div class="compare-slot-item" style="display: flex; align-items: center; gap: 15px; background: var(--bg-gray); padding: 10px 15px; border-radius: 12px; border: 1px solid var(--border-color); flex: 1; position: relative; font-family: inherit;">
                        <img src="${p.img}" style="width: 55px; height: 55px; object-fit: contain; background: var(--bg-white); border-radius: 6px; padding: 3px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                        <div style="flex: 1; min-width: 0;">
                            <div style="font-size: 0.95rem; font-weight: 700; color: var(--text-dark); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-bottom: 4px;">${p.name}</div>
                            <div style="font-size: 1.05rem; font-weight: 800; color: var(--primary);">${p.price}</div>
                        </div>
                        <button onclick="removeCompare('${p.name}')" style="background: none; border: none; color: var(--text-gray); cursor: pointer; padding: 5px; display: flex; font-size: 1.2rem; transition: color 0.2s;" onmouseover="this.style.color='#ef4444'" onmouseout="this.style.color='var(--text-gray)'"><i class="ph-bold ph-x"></i></button>
                    </div>
                `;
            } else {
                html += `
                    <div class="compare-slot-item" style="display: flex; align-items: center; justify-content: center; gap: 10px; background: transparent; padding: 10px 15px; border-radius: 12px; border: 1px dashed var(--border-color); flex: 1; color: var(--text-gray); font-size: 0.95rem; font-family: inherit;">
                        <div style="width: 45px; height: 45px; border-radius: 50%; background: var(--bg-gray); display: flex; align-items: center; justify-content: center;"><i class="ph ph-plus" style="font-size: 1.2rem;"></i></div>
                        Thêm sản phẩm
                    </div>
                `;
            }
        }
        slots.innerHTML = html;
    }
    
    function executeCompare(isFullScreen = false) {
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
