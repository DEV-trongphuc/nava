  window.currentProductData = {
    name: "Mini PC hỗ trợ AI ASUS NUC 14 PRO RNUC14RVHU700001I (Ultra 7 155H | 2xNVMe, SATA | 2x HDMI 2.1 | 2x DP 1.4a | VESA Mount)",
    img: "//bizweb.dktcdn.net/thumb/medium/100/543/817/products/mini-pc-asus-nuc-14-pro-ai-ultra7-155h-ai-gaming-van-phong.jpg?v=1763972304177",
    price: "12.990.000₫",
    url: "/mini-pc-ho-tro-ai-asus-nuc-14-pro-rnuc14rvhu700001i-ultra-7-155h-2xnvme-sata-2x-hdmi-2-1-2x-dp-1-4a-vesa-mount"
  };
  window.currentCollectionProducts = [];
        window.currentCollectionProducts.push({
          name: "Mini PC hỗ trợ AI ASUS NUC 14 PRO RNUC14RVHU500001I (Ultra 5 125H | 2xNVMe, SATA | 2x HDMI 2.1 | 2x DP 1.4a | VESA Mount)",
          url: "/mini-pc-ho-tro-ai-asus-nuc-14-pro-rnuc14rvhu500001i-ultra-5-125h-2xnvme-sata-2x-hdmi-2-1-2x-dp-1-4a-vesa-mount",
          img: "//bizweb.dktcdn.net/thumb/medium/100/543/817/products/mini-pc-asus-nuc-14-pro-ai-ultra5-125h-ai-gaming-van-phong.jpg?v=1763972398687",
          price: "9.990.000₫"
        });
        window.currentCollectionProducts.push({
          name: "Mini PC ASUS NUC 14 Pro Plus RNUC14RVSU500001I (Ultra 5 125H, Arc Graphics)",
          url: "/mini-pc-asus-nuc-14-pro-plus-rnuc14rvsu500001i-ultra-5-125h-arc-graphics",
          img: "//bizweb.dktcdn.net/thumb/medium/100/543/817/products/mini-pc-asus-nuc-14-pro-plus-ultra5-125h.jpg?v=1764400847650",
          price: "13.490.000₫"
        });
        window.currentCollectionProducts.push({
          name: "Mini PC ASUS NUC 14 Pro Plus RNUC14RVSU700001I (Ultra 7 155H, Arc Graphics)",
          url: "/mini-pc-asus-nuc-14-pro-plus-rnuc14rvsu700001i-ultra-7-155h-arc-graphics",
          img: "//bizweb.dktcdn.net/thumb/medium/100/543/817/products/mini-pc-asus-nuc-14-pro-plus-ultra7-155h.jpg?v=1764400881927",
          price: "15.990.000₫"
        });

let isSyncing = false;
function syncSwatches() {
    if (isSyncing) return;
    isSyncing = true;
    
    try {
        const selectEl = document.querySelector('.box-variant #product-selectors');
        const hiddenInput = document.querySelector('.box-variant input[name="variantId"]');
        let isSoldOut = !window.mainProductAvailable;
        let priceVal = 0;
        
        const swatchRows = document.querySelectorAll('.swatch');
        if (swatchRows.length > 0) {
            const selectedValues = [];
            swatchRows.forEach(swatchRow => {
                const checkedInput = swatchRow.querySelector('input[type="radio"]:checked');
                if (checkedInput) {
                    selectedValues.push(checkedInput.value.trim());
                    const parent = checkedInput.closest('.swatch-element');
                    if (parent && parent.classList.contains('soldout')) {
                        isSoldOut = true;
                    }
                }
            });
            
            if (selectEl) {
                const options = Array.from(selectEl.options);
                let matchedOption = null;
                
                options.forEach(opt => {
                    const textParts = opt.text.split('-');
                    let titlePart = textParts[0].trim();
                    titlePart = titlePart.replace(/^\d+\s+/, '').trim();
                    
                    const optValues = titlePart.split('/').map(v => v.trim());
                    
                    let isMatch = true;
                    for (let i = 0; i < selectedValues.length; i++) {
                        if (optValues[i] !== selectedValues[i]) {
                            isMatch = false;
                            break;
                        }
                    }
                    if (isMatch) {
                        matchedOption = opt;
                    }
                });
                
                if (matchedOption) {
                    if (selectEl.value !== matchedOption.value) {
                        selectEl.value = matchedOption.value;
                        selectEl.dispatchEvent(new Event('change', { bubbles: true }));
                    }
                    
                    const isAvail = matchedOption.getAttribute('data-available');
                    if (isAvail === 'false') {
                        isSoldOut = true;
                    } else if (isAvail === 'true') {
                        isSoldOut = false;
                    }
                    priceVal = parseInt(matchedOption.getAttribute('data-price') || '0', 10);
                }
            }
        } else {
            // No swatch radio rows on page (fallback to standard dropdown)
            if (selectEl) {
                const activeOption = selectEl.selectedOptions[0] || selectEl.options[selectEl.selectedIndex];
                if (activeOption) {
                    const isAvail = activeOption.getAttribute('data-available');
                    if (isAvail === 'false') {
                        isSoldOut = true;
                    } else if (isAvail === 'true') {
                        isSoldOut = false;
                    }
                    priceVal = parseInt(activeOption.getAttribute('data-price') || '0', 10);
                }
            } else if (hiddenInput) {
                const isAvail = hiddenInput.getAttribute('data-available');
                if (isAvail === 'false') {
                    isSoldOut = true;
                } else if (isAvail === 'true') {
                    isSoldOut = false;
                }
                priceVal = parseInt(hiddenInput.getAttribute('data-price') || '0', 10);
            }
        }
        
        // Fallback: If priceVal is still 0, check if we can retrieve it from #selected-variant-price
        if (priceVal === 0) {
            const mainPriceText = document.getElementById('selected-variant-price')?.textContent;
            if (mainPriceText) {
                priceVal = parsePrice(mainPriceText);
            }
        }
    
    // Update Buy Button UI based on availability and price
    const btnInStock = document.querySelector('.btn-group-instock');
    const btnOutStock = document.querySelector('.btn-group-outstock');
    const statusEl = document.getElementById('availability-status');
    const btnAddToCart = document.getElementById('btn-add-to-cart');
    const btnInstallment = document.getElementById('btn-installment');
    const btnBuyNow = document.getElementById('btn-buy-now');
    
    if (isSoldOut) {
        if (btnInStock) btnInStock.style.display = 'flex';
        if (btnOutStock) btnOutStock.style.display = 'none';
        
        if (statusEl) {
            statusEl.innerText = 'Hết hàng';
            statusEl.style.color = '#ef4444';
        }
        if (btnAddToCart) {
            btnAddToCart.disabled = true;
            btnAddToCart.style.opacity = '0.5';
            btnAddToCart.style.pointerEvents = 'none';
        }
        if (btnInstallment) {
            btnInstallment.disabled = true;
            btnInstallment.style.opacity = '0.5';
            btnInstallment.style.pointerEvents = 'none';
        }
        if (btnBuyNow) {
            btnBuyNow.disabled = true;
            btnBuyNow.innerText = 'HẾT HÀNG';
            btnBuyNow.style.opacity = '0.5';
            btnBuyNow.style.pointerEvents = 'none';
            btnBuyNow.style.setProperty('flex', '1.5', 'important');
        }
    } else {
        if (btnInStock) btnInStock.style.display = 'flex';
        if (btnOutStock) btnOutStock.style.display = 'none';
        
        // Reset disabled states and styles
        if (btnAddToCart) {
            btnAddToCart.disabled = false;
            btnAddToCart.style.opacity = '';
            btnAddToCart.style.pointerEvents = '';
        }
        if (btnInstallment) {
            btnInstallment.disabled = false;
            btnInstallment.style.opacity = '';
            btnInstallment.style.pointerEvents = '';
        }
        if (btnBuyNow) {
            btnBuyNow.disabled = false;
            btnBuyNow.style.opacity = '';
            btnBuyNow.style.pointerEvents = '';
        }
        
        const bsBuyBtn = document.querySelector('.bs-buy-btn');
        const bsAddCartBtn = document.querySelector('.btn-add-cart-bs');
        
        if (priceVal === 0) {
            if (statusEl) {
                statusEl.innerText = 'Liên hệ';
                statusEl.style.color = '#003366';
            }
            if (btnAddToCart) {
                btnAddToCart.disabled = true;
                btnAddToCart.style.background = '#cbd5e1';
                btnAddToCart.style.borderColor = '#cbd5e1';
                btnAddToCart.style.color = '#94a3b8';
                btnAddToCart.style.opacity = '1';
                btnAddToCart.style.pointerEvents = 'none';
            }
            if (btnInstallment) {
                btnInstallment.disabled = true;
                btnInstallment.style.background = '#cbd5e1';
                btnInstallment.style.borderColor = '#cbd5e1';
                btnInstallment.style.color = '#94a3b8';
                btnInstallment.style.opacity = '1';
                btnInstallment.style.pointerEvents = 'none';
            }
            if (btnBuyNow) {
                btnBuyNow.disabled = false;
                btnBuyNow.innerText = 'LIÊN HỆ';
                btnBuyNow.style.background = '#334155';
                btnBuyNow.style.color = 'white';
                btnBuyNow.style.opacity = '1';
                btnBuyNow.style.pointerEvents = 'auto';
                btnBuyNow.style.setProperty('flex', '1.5', 'important');
            }
            if (bsBuyBtn) {
                bsBuyBtn.disabled = false;
                bsBuyBtn.innerText = 'LIÊN HỆ';
                bsBuyBtn.style.background = '#334155';
                bsBuyBtn.style.color = 'white';
                bsBuyBtn.style.opacity = '1';
                bsBuyBtn.style.pointerEvents = 'auto';
            }
            if (bsAddCartBtn) {
                bsAddCartBtn.disabled = true;
                bsAddCartBtn.style.background = '#cbd5e1';
                bsAddCartBtn.style.borderColor = '#cbd5e1';
                bsAddCartBtn.style.color = '#94a3b8';
                bsAddCartBtn.style.opacity = '1';
                bsAddCartBtn.style.pointerEvents = 'none';
            }
        } else {
            if (statusEl) {
                statusEl.innerText = 'Còn hàng';
                statusEl.style.color = '#22c55e';
            }
            if (btnAddToCart) {
                btnAddToCart.disabled = false;
                btnAddToCart.style.background = 'transparent';
                btnAddToCart.style.borderColor = 'var(--primary)';
                btnAddToCart.style.color = 'var(--primary)';
                btnAddToCart.style.opacity = '';
                btnAddToCart.style.pointerEvents = '';
            }
            if (btnInstallment) {
                btnInstallment.disabled = false;
                btnInstallment.style.background = 'transparent';
                btnInstallment.style.borderColor = 'var(--primary)';
                btnInstallment.style.color = 'var(--primary)';
                btnInstallment.style.opacity = '';
                btnInstallment.style.pointerEvents = '';
            }
            if (btnBuyNow) {
                btnBuyNow.disabled = false;
                btnBuyNow.innerText = 'MUA NGAY';
                btnBuyNow.style.background = 'var(--primary)';
                btnBuyNow.style.color = 'white';
                btnBuyNow.style.opacity = '';
                btnBuyNow.style.pointerEvents = '';
                btnBuyNow.style.setProperty('flex', '1.5', 'important');
            }
            if (bsBuyBtn) {
                bsBuyBtn.disabled = false;
                bsBuyBtn.innerText = 'MUA NGAY';
                bsBuyBtn.style.background = 'linear-gradient(90deg, var(--primary), var(--secondary))';
                bsBuyBtn.style.color = 'white';
                bsBuyBtn.style.opacity = '';
                bsBuyBtn.style.pointerEvents = '';
            }
            if (bsAddCartBtn) {
                bsAddCartBtn.disabled = false;
                bsAddCartBtn.style.background = 'var(--bg-gray)';
                bsAddCartBtn.style.borderColor = 'var(--border-color)';
                bsAddCartBtn.style.color = 'var(--primary)';
                bsAddCartBtn.style.opacity = '';
                bsAddCartBtn.style.pointerEvents = '';
            }
        }
    }
    
    // Update bottom sheet price display
    const bsPriceEl = document.getElementById('bs-price');
    if (bsPriceEl) {
        const isFbtActive = !!document.querySelector('frequently-buy-together');
        if (isFbtActive) {
            const fbtTotalEl = document.querySelector('frequently-buy-together span[data-fbt-total]') || document.querySelector('frequently-buy-together [data-fbt-total]');
            if (fbtTotalEl) {
                bsPriceEl.innerText = fbtTotalEl.textContent.trim();
            } else {
                bsPriceEl.innerText = priceVal === 0 ? 'Liên hệ' : formatVietnameseCurrency(priceVal);
            }
        } else {
            bsPriceEl.innerText = priceVal === 0 ? 'Liên hệ' : formatVietnameseCurrency(priceVal);
        }
    }
    
    // Update mobile bottom sticky buy bar
    const mobileBuyBar = document.querySelector('.mobile-bottom-buybar');
    if (mobileBuyBar) {
        if (isSoldOut) {
            mobileBuyBar.innerHTML = `<a href="tel:0972178527" class="bar-buy-now text-center d-flex align-items-center justify-content-center font-weight-bold" style="width: 100%; height: 44px; background: var(--primary); border: none; border-radius: 8px; color: white !important; font-size: 0.88rem; text-decoration: none; text-transform: uppercase; box-shadow: 0 4px 10px rgba(0,51,102,0.15);">LIÊN HỆ ĐẶT TRƯỚC: 0972.178.527</a>`;
        } else if (priceVal === 0) {
            mobileBuyBar.innerHTML = `<a href="tel:0972178527" class="bar-buy-now text-center d-flex align-items-center justify-content-center font-weight-bold" style="width: 100%; height: 44px; background: var(--primary); border: none; border-radius: 8px; color: white !important; font-size: 0.88rem; text-decoration: none; text-transform: uppercase; box-shadow: 0 4px 10px rgba(0,51,102,0.15);">LIÊN HỆ: 0972.178.527</a>`;
        } else {
            const formattedPrice = formatVietnameseCurrency(priceVal);
            mobileBuyBar.innerHTML = `
                <div style="display: flex; flex-direction: column;">
                    <span style="font-size: 0.72rem; color: var(--text-gray); margin-bottom: 2px;">Giá ưu đãi</span>
                    <span id="sticky-price" style="font-size: 1.15rem; font-weight: 900; color: var(--primary);">${formattedPrice}</span>
                </div>
                <div style="display: flex; gap: 8px;">
                    <button class="bar-add-cart" style="background: var(--bg-gray); border: 1px solid var(--border-color); border-radius: 8px; width: 44px; height: 44px; display: flex; align-items: center; justify-content: center; cursor: pointer; color: var(--primary);"><i class="ph-bold ph-shopping-cart-simple" style="font-size: 1.2rem;"></i></button>
                    <button class="bar-buy-now" style="background: var(--primary); border: none; border-radius: 8px; padding: 0 20px; height: 44px; font-weight: 800; font-size: 0.92rem; color: white; cursor: pointer; box-shadow: 0 4px 10px rgba(0,51,102,0.15);">Mua ngay</button>
                </div>
            `;
        }
    }
    
    // Check if we need to show the RAM/SSD configuration nudge
    if (typeof checkRAMSSDPrompt === 'function') {
        checkRAMSSDPrompt();
    }
    } finally {
        isSyncing = false;
    }
}

function checkRAMSSDPrompt() {
    let hasRam = false;
    let hasSsd = false;
    
    document.querySelectorAll('.swatch .header, .swatch-element, .single-option-selector, label, span').forEach(el => {
        const text = el.textContent.toLowerCase();
        if (text.includes('ram') || text.includes('dram')) hasRam = true;
        if (text.includes('ssd') || text.includes('nvme')) hasSsd = true;
    });
    
    if (document.querySelector('[data-dropdown-type="ram"]') || document.querySelector('#ram-selected-text')) hasRam = true;
    if (document.querySelector('[data-dropdown-type="ssd"]') || document.querySelector('#ssd-selected-text')) hasSsd = true;
    
    if (!hasRam && !hasSsd) return;
    
    let isDefaultRam = false;
    let isDefaultSsd = false;
    
    const ramDisplay = document.querySelector('[data-dropdown-type="ram"] .nava-dropdown-selected, #ram-selected-text');
    if (ramDisplay) {
        const text = ramDisplay.textContent.toUpperCase();
        if (text.includes('NO RAM') || /(^|[^0-9])0\s*gb/i.test(text) || text.includes('TRỐNG')) {
            isDefaultRam = true;
        }
    }
    
    const ssdDisplay = document.querySelector('[data-dropdown-type="ssd"] .nava-dropdown-selected, #ssd-selected-text');
    if (ssdDisplay) {
        const text = ssdDisplay.textContent.toUpperCase();
        if (text.includes('NO SSD') || /(^|[^0-9])0\s*gb/i.test(text) || text.includes('TRỐNG')) {
            isDefaultSsd = true;
        }
    }
    
    const selectEl = document.querySelector('.box-variant #product-selectors');
    if (selectEl && selectEl.selectedOptions && selectEl.selectedOptions[0]) {
        const optText = selectEl.selectedOptions[0].text.toUpperCase();
        if (optText.includes('NO RAM') || optText.includes('NO SSD')) {
            isDefaultRam = true;
            isDefaultSsd = true;
        }
    }
    
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
            hideNudgeBanner();
            openBottomSheet();
        });
    }
    
    setTimeout(() => {
        banner.style.transform = 'translateX(-50%) translateY(0)';
        banner.style.opacity = '1';
        if (!isAlreadyVisible) {
            banner.classList.add('nudge-shake-active');
     var isBsOpen = false;

function updateBottomSheetPrice() {
    const bsPriceEl = document.getElementById('bs-price');
    if (!bsPriceEl) return;
    
    let activePriceText = '';
    const isFbtActive = !!document.querySelector('frequently-buy-together');
    if (isFbtActive) {
        const fbtTotalEl = document.querySelector('frequently-buy-together span[data-fbt-total]') || document.querySelector('frequently-buy-together [data-fbt-total]');
        if (fbtTotalEl) {
            activePriceText = fbtTotalEl.textContent.trim();
        }
    }
    if (!activePriceText) {
        const selectedVariantPriceEl = document.getElementById('selected-variant-price');
        if (selectedVariantPriceEl) {
            activePriceText = selectedVariantPriceEl.textContent.trim();
        }
    }
    if (!activePriceText) {
        const stickyPriceEl = document.getElementById('sticky-price');
        if (stickyPriceEl) {
            activePriceText = stickyPriceEl.textContent.trim();
        }
    }
    
    if (activePriceText) {
        bsPriceEl.innerText = activePriceText;
    }
}

function openBottomSheet() {
    const overlay = document.getElementById('nava-bs-overlay');
    const bs = document.getElementById('nava-bottom-sheet');
    const optionsContainer = document.getElementById('nava-bs-options-container');
    const stickyBar = document.querySelector('.mobile-bottom-buybar');
    
    if (overlay && bs && optionsContainer) {
        isBsOpen = true;
        
        // Sync active price into bottom sheet on open
        updateBottomSheetPrice();
        
        // Hide mobile sticky bottom bar when bottom sheet is open
        if (stickyBar) {
            stickyBar.style.setProperty('transform', 'translateY(120%)', 'important');
        }
        
        const isFbtActive = !!document.querySelector('frequently-buy-together');
        if (isFbtActive) {
            const fbtOptions = document.querySelector('.nava-custom-fbt-container');
            if (fbtOptions) {
                optionsContainer.innerHTML = '';
                optionsContainer.appendChild(fbtOptions);
            }
            const fbtQty = document.querySelector('frequently-buy-together .custom-btn-number');
            const bsQtyContainer = document.getElementById('nava-bs-qty-container');
            if (fbtQty && bsQtyContainer) {
                bsQtyContainer.innerHTML = '';
                bsQtyContainer.appendChild(fbtQty);
            }
        } else {
            const productControl = document.querySelector('.product-control');
            if (productControl) {
                optionsContainer.innerHTML = '';
                optionsContainer.appendChild(productControl);
            }
            const qtySelector = document.querySelector('.qty-selector');
            const bsQtyContainer = document.getElementById('nava-bs-qty-container');
            if (qtySelector && bsQtyContainer) {
                bsQtyContainer.innerHTML = '';
                bsQtyContainer.appendChild(qtySelector);
            }
        }
        
        // Display bottom sheet
        overlay.style.display = 'block';
        bs.style.display = 'flex';
        void overlay.offsetWidth;
        void bs.offsetWidth;
        overlay.style.opacity = '1';
        bs.classList.add('open');
        document.body.style.overflow = 'hidden';
        
        // Trigger glow animation for options
        const displays = bs.querySelectorAll('.nava-custom-select-display, .swatch, .nava-dropdown-display');
        displays.forEach(d => {
            d.style.animation = 'none';
            void d.offsetWidth; // Reflow
            d.style.animation = 'bs-glow-attention 1.2s ease-in-out 3';
        });
    }
}

function closeBottomSheet() {
    const overlay = document.getElementById('nava-bs-overlay');
    const bs = document.getElementById('nava-bottom-sheet');
    const stickyBar = document.querySelector('.mobile-bottom-buybar');
    
    if (overlay && bs) {
        isBsOpen = false;
        overlay.style.opacity = '0';
        bs.classList.remove('open');
        
        // Show sticky bar again
        if (stickyBar) {
            stickyBar.style.setProperty('transform', 'translateY(0)', 'important');
        }
        
        setTimeout(() => {
            overlay.style.display = 'none';
            bs.style.display = 'none';
            document.body.style.overflow = '';
            
            const isFbtActive = !!document.querySelector('frequently-buy-together');
            if (isFbtActive) {
                const fbtOptions = document.querySelector('.nava-custom-fbt-container');
                const fbtEl = document.querySelector('frequently-buy-together');
                if (fbtOptions && fbtEl && !fbtEl.contains(fbtOptions)) {
                    const pb3Row = fbtEl.querySelector('.pb-3');
                    if (pb3Row) {
                        fbtEl.insertBefore(fbtOptions, pb3Row);
                    } else {
                        fbtEl.appendChild(fbtOptions);
                    }
                }
                const fbtQty = document.querySelector('.custom-btn-number');
                const pb3Row = document.querySelector('frequently-buy-together .pb-3');
                if (fbtQty && pb3Row && !pb3Row.contains(fbtQty)) {
                    pb3Row.insertBefore(fbtQty, pb3Row.firstChild);
                }
            } else {
                const productControl = document.querySelector('.product-control');
                const form = document.getElementById('nava-product-form');
                const qtyRow = document.querySelector('.qty-price-row');
                if (productControl && form && !form.contains(productControl)) {
                    if (qtyRow) {
                        form.insertBefore(productControl, qtyRow);
                    } else {
                        form.appendChild(productControl);
                    }
                }
                const qtySelector = document.querySelector('.qty-selector');
                const qtyLabelWrap = document.querySelector('.qty-price-row > div:first-child');
                if (qtySelector && qtyLabelWrap && !qtyLabelWrap.contains(qtySelector)) {
                    qtyLabelWrap.appendChild(qtySelector);
                }
            }
        }, 300);
    }
}

function initNavaProductEnforcement() {
    // Handle bottom sheet quick configuration buttons click
    document.addEventListener('click', function(e) {
        if (e.target.closest('.btn-add-cart-bs')) {
            e.preventDefault();
            const isFbtActive = !!document.querySelector('frequently-buy-together');
            if (isFbtActive) {
                const realBtn = document.querySelector('frequently-buy-together button.tg-addcart');
                if (realBtn) {
                    realBtn.click();
                    setTimeout(() => {
                        // Close bottom sheet if not blocked by options check
                        let isDefaultRam = false;
                        let isDefaultSsd = false;
                        document.querySelectorAll('frequently-buy-together select[data-fbt-item-id]').forEach(select => {
                            const val = select.value;
                            const parent = select.closest('[data-fbt-item]');
                            const labelText = parent ? parent.querySelector('label.f-item p')?.textContent.toUpperCase() || '' : '';
                            if ((labelText.includes('RAM') || labelText.includes('DRAM')) && (val === 'no-select' || val === '')) isDefaultRam = true;
                            if ((labelText.includes('SSD') || labelText.includes('NVME')) && (val === 'no-select' || val === '')) isDefaultSsd = true;
                        });
                        
                        let shouldBlock = false;
                        if (window.mainProductAvailable) {
                            if (isDefaultRam || isDefaultSsd) shouldBlock = true;
                        } else {
                            if (isDefaultRam && isDefaultSsd) shouldBlock = true;
                        }
                        
                        if (!shouldBlock) {
                            closeBottomSheet();
                        }
                    }, 100);
                }
            } else {
                const realBtn = document.getElementById('btn-add-to-cart');
                if (realBtn) {
                    realBtn.click();
                    setTimeout(() => {
                        // Close bottom sheet if not blocked by options check
                        let isDefaultRam = false;
                        let isDefaultSsd = false;
                        const ramDisplay = document.querySelector('[data-dropdown-type="ram"] .nava-dropdown-selected, #ram-selected-text');
                        if (ramDisplay && (ramDisplay.textContent.toUpperCase().includes('NO RAM') || /(^|[^0-9])0\s*gb/i.test(ramDisplay.textContent) || ramDisplay.textContent.toUpperCase().includes('TRỐNG'))) isDefaultRam = true;
                        const ssdDisplay = document.querySelector('[data-dropdown-type="ssd"] .nava-dropdown-selected, #ssd-selected-text');
                        if (ssdDisplay && (ssdDisplay.textContent.toUpperCase().includes('NO SSD') || /(^|[^0-9])0\s*gb/i.test(ssdDisplay.textContent) || ssdDisplay.textContent.toUpperCase().includes('TRỐNG'))) isDefaultSsd = true;
                        
                        let shouldBlock = false;
                        if (window.mainProductAvailable) {
                            if (isDefaultRam || isDefaultSsd) shouldBlock = true;
                        } else {
                            if (isDefaultRam && isDefaultSsd) shouldBlock = true;
                        }
                        
                        if (!shouldBlock) {
                            closeBottomSheet();
                        }
                    }, 100);
                }
            }
        }
        if (e.target.closest('.bs-buy-btn')) {
            e.preventDefault();
            const isFbtActive = !!document.querySelector('frequently-buy-together');
            if (isFbtActive) {
                const realBtn = document.querySelector('frequently-buy-together button.tg-buy-now');
                if (realBtn) {
                    realBtn.click();
                }
            } else {
                const realBtn = document.getElementById('btn-buy-now');
                if (realBtn) {
                    realBtn.click();
                }
            }
        }
    });

    // Intercept checkout clicks in capture phase to validate options selection and contact price
    document.addEventListener('click', function(e) {
        const btn = e.target.closest('#btn-add-to-cart, #btn-installment, #btn-buy-now, .bar-add-cart, .bar-buy-now, .js-addToCart, .js-buynow, .btn-add-cart-sticky, .btn-buy-now-sticky, .btn-add-cart-bs, .bs-buy-btn, .tg-addcart, .tg-buy-now, .buy_now');
        if (btn) {
            let isDefaultRam = false;
            let isDefaultSsd = false;
            
            // 1. Check nava custom dropdowns
            const ramDisplay = document.querySelector('[data-dropdown-type="ram"] .nava-dropdown-selected, #ram-selected-text');
            if (ramDisplay) {
                const text = ramDisplay.textContent.toUpperCase();
                if (text.includes('NO RAM') || /(^|[^0-9])0\s*gb/i.test(text) || text.includes('TRỐNG')) {
                    isDefaultRam = true;
                }
            }
            const ssdDisplay = document.querySelector('[data-dropdown-type="ssd"] .nava-dropdown-selected, #ssd-selected-text');
            if (ssdDisplay) {
                const text = ssdDisplay.textContent.toUpperCase();
                if (text.includes('NO SSD') || /(^|[^0-9])0\s*gb/i.test(text) || text.includes('TRỐNG')) {
                    isDefaultSsd = true;
                }
            }
            
            // 2. Check Sapo native/custom selectors
            document.querySelectorAll('.single-option-selector').forEach(select => {
                const val = select.value.toUpperCase();
                const label = select.closest('.selector-wrapper')?.querySelector('label')?.textContent.toUpperCase() || '';
                const isRam = val.includes('RAM') || label.includes('RAM') || label.includes('DRAM');
                const isSsd = val.includes('SSD') || label.includes('SSD') || label.includes('NVME');
                
                if (isRam && (val.includes('NO RAM') || val.includes('TRỐNG') || /(^|[^0-9])0\s*gb/i.test(val) || val.includes('CHƯA CHỌN'))) {
                    isDefaultRam = true;
                }
                if (isSsd && (val.includes('NO SSD') || val.includes('TRỐNG') || /(^|[^0-9])0\s*gb/i.test(val) || val.includes('CHƯA CHỌN'))) {
                    isDefaultSsd = true;
                }
            });
            
            // 3. Check Sapo native swatches
            document.querySelectorAll('.swatch input[type="radio"]:checked').forEach(radio => {
                const val = radio.value.toUpperCase();
                const name = radio.name.toUpperCase();
                if (name.includes('RAM') || val.includes('RAM')) {
                    if (val.includes('NO RAM') || val.includes('TRỐNG') || /(^|[^0-9])0\s*gb/i.test(val)) isDefaultRam = true;
                }
                if (name.includes('SSD') || val.includes('SSD')) {
                    if (val.includes('NO SSD') || val.includes('TRỐNG') || /(^|[^0-9])0\s*gb/i.test(val)) isDefaultSsd = true;
                }
            });
            
            // 4. Check global Sapo selectors state
            const selectEl = document.querySelector('.box-variant #product-selectors');
            if (selectEl && selectEl.selectedOptions && selectEl.selectedOptions[0]) {
                const optText = selectEl.selectedOptions[0].text.toUpperCase();
                if (optText.includes('NO RAM') || optText.includes('NO SSD')) {
                    isDefaultRam = true;
                    isDefaultSsd = true;
                }
            }
 
            // 5. Check Frequently Bought Together select elements
            document.querySelectorAll('frequently-buy-together select[data-fbt-item-id]').forEach(select => {
                const val = select.value;
                const parent = select.closest('[data-fbt-item]');
                const labelText = parent ? parent.querySelector('label.f-item p')?.textContent.toUpperCase() || '' : '';
                const isRam = labelText.includes('RAM') || labelText.includes('DRAM');
                const isSsd = labelText.includes('SSD') || labelText.includes('NVME');
                
                if (isRam && (val === 'no-select' || val === '')) {
                    isDefaultRam = true;
                }
                if (isSsd && (val === 'no-select' || val === '')) {
                    isDefaultSsd = true;
                }
            });
            
            // Block if RAM or SSD options are not configured
            let shouldBlock = false;
            if (window.mainProductAvailable) {
                // In stock: must choose both RAM and SSD
                if (isDefaultRam || isDefaultSsd) shouldBlock = true;
            } else {
                // Out of stock: can buy accessories alone, but must select at least one accessory
                if (isDefaultRam && isDefaultSsd) shouldBlock = true;
            }
            
            if (shouldBlock) {
                e.preventDefault();
                e.stopPropagation();
                
                openBottomSheet();
                const bs = document.getElementById('nava-bottom-sheet');
                if (bs) {
                    bs.classList.remove('bs-shake-active');
                    void bs.offsetWidth; // Reflow
                    bs.classList.add('bs-shake-active');
                }
                return;
            }
            
            // Block if price is contact-only (Liên hệ / 0)
            let isContactPrice = false;
            const priceEl = document.getElementById('selected-variant-price') || document.getElementById('bs-price') || document.getElementById('sticky-price');
            if (priceEl) {
                const priceText = priceEl.textContent.trim().toLowerCase();
                const cleanPriceText = priceText.replace(/[^\d]/g, '');
                if (cleanPriceText === '0' || cleanPriceText === '' || priceText.includes('liên hệ') || priceText.includes('contact')) {
                    isContactPrice = true;
                }
            }
            const fbtTotalEl = document.querySelector('frequently-buy-together [data-fbt-total]') || document.querySelector('.fbt-total-price');
            if (fbtTotalEl) {
                const fbtTotalText = fbtTotalEl.textContent.trim().toLowerCase();
                const cleanFbtText = fbtTotalText.replace(/[^\d]/g, '');
                if (cleanFbtText === '0' || cleanFbtText === '' || fbtTotalText.includes('liên hệ') || fbtTotalText.includes('contact')) {
                    isContactPrice = true;
                }
            }
            if (selectEl && selectEl.selectedOptions && selectEl.selectedOptions[0]) {
                const activeOption = selectEl.selectedOptions[0];
                const rawPrice = parseInt(activeOption.getAttribute('data-price') || '0', 10);
                if (rawPrice === 0) {
                    isContactPrice = true;
                }
            }
            const hiddenInput = document.querySelector('.box-variant input[name="variantId"]');
            if (hiddenInput) {
                const rawPrice = parseInt(hiddenInput.getAttribute('data-price') || '0', 10);
                if (rawPrice === 0) {
                    isContactPrice = true;
                }
            }
            const basePriceVal = parseInt("12990000".replace(/[^\d]/g, ''), 10) || 0;
            const productPriceVal = parseInt("11790000".replace(/[^\d]/g, ''), 10) || 0;
            if (basePriceVal === 0 || productPriceVal === 0) {
                isContactPrice = true;
            }
            
            if (isContactPrice) {
                e.preventDefault();
                e.stopPropagation();
                if (btn.id === 'btn-buy-now' || btn.classList.contains('bs-buy-btn') || btn.classList.contains('bar-buy-now')) {
                    window.location.href = 'tel:0972178527';
                }
                return;
            }
        }
    }, true); // Capture phase is critical to run before other listeners

    // Sync swatches on load
    setTimeout(syncSwatches, 100);
    
    // Initialize gallery zoom and lightbox photo viewer
    initGalleryZoom();
    
    // Render custom FBT instead of formatting native ones
    setTimeout(function() {
        initNavaCustomFbt();
        setupFbtMutationObserver();
    }, 150);
    
    // Setup price ticker observers initially and as fallback
    setTimeout(setupPriceObservers, 200);
    setTimeout(setupPriceObservers, 1000);
    
    // Periodically sync checkboxes initially (handles Sapo async upgrade)
    function syncFbtCheckboxes() {
        document.querySelectorAll('frequently-buy-together [data-fbt-item]').forEach(item => {
            const select = item.querySelector('select[data-fbt-item-id]');
            const checkbox = item.querySelector('.i-check') || item.querySelector('input[type="checkbox"]');
            if (select && checkbox) {
                const isNoSelect = (select.value === 'no-select' || select.value === '');
                checkbox.checked = !isNoSelect;
            }
        });
        // Let Sapo recalculate total
        const fbt = document.querySelector('frequently-buy-together');
        if (fbt && typeof fbt.total !== 'undefined') {
            fbt.total;
        }
    }
    
    setTimeout(syncFbtCheckboxes, 250);
    setTimeout(syncFbtCheckboxes, 1200);

    // Watch swatch radio and other variant selector changes
    document.addEventListener('change', function(e) {
        if (e.target.closest('.swatch-element input') || e.target.closest('.single-option-selector')) {
            syncSwatches();
        }
    });

    // Inject Trả góp 0% button inside FBT buttons row if not present
    const fbt = document.querySelector('frequently-buy-together');
    if (fbt) {
        const btnRow = fbt.querySelector('.gap_6');
        if (btnRow && !btnRow.querySelector('.js-fbt-installment')) {
            const buyNowBtn = btnRow.querySelector('.tg-buy-now');
            if (buyNowBtn) {
                const instBtn = document.createElement('button');
                instBtn.type = 'button';
                instBtn.className = 'btn js-fbt-installment font-weight-bold';
                instBtn.textContent = 'TRẢ GÓP 0%';
                btnRow.insertBefore(instBtn, buyNowBtn);
            }
        }
    }
}

// Handle click event for FBT Installment button
document.addEventListener('click', function(e) {
    if (e.target.closest('.js-fbt-installment')) {
        e.preventDefault();
        const fbtBtn = document.querySelector('.tg-addcart');
        if (fbtBtn) {
            fbtBtn.click();
            setTimeout(function() {
                window.location.href = '/';
            }, 1200);
        }
    }
});

// FBT Submission and cart adding logic
if (typeof jQuery !== 'undefined') {
    jQuery(document).ready(function($) {
        $('frequently-buy-together button:not(.not-submit)').on('click', async function (e) {
            const $btn = $(e.currentTarget);
            if ($btn.hasClass('js-fbt-installment')) return; // Skip installment button handling
            
            const parent = $btn.closest('frequently-buy-together');
            const arrItem = parent[0].trim ? parent[0].trim() : (parent[0].handleArray ? parent[0].handleArray() : []);

            if (!arrItem.length) {
                createToast('error', toastString.toastAddErrorTitle, 'Hãy chọn ít nhất 1 sản phẩm');
                return;
            }

            const sleep = (ms) => new Promise(r => setTimeout(r, ms));
            const isRetryable = (err) => {
                const status = err?.status || err?.response?.status;
                return (
                    status === 429 ||
                    (status >= 500 && status <= 599) ||
                    /network|timeout|fetch/i.test(String(err?.message || err))
                );
            };

            const addItemWithRetry = async (variantId, quantity, maxRetry = 2) => {
                let attempt = 0;
                while (true) {
                    try {
                        return await mewService.addItem(variantId, quantity);
                    } catch (err) {
                        attempt++;
                        if (attempt > maxRetry || !isRetryable(err)) throw err;

                        const wait = 250 * Math.pow(2, attempt - 1) + Math.floor(Math.random() * 150);
                        await sleep(wait);
                    }
                }
            };

            try {
                $btn.addClass('loading');
                const isBuyNow = !!$btn.closest('.buy_now').length;

                if (isBuyNow) {
                    await fetch('/cart/clear.js', { method: 'POST' });
                    await sleep(150);
                }

                const successes = [];
                const failures = [];
                for (const item of arrItem) {
                    try {
                        await addItemWithRetry(item.variantId, item.quantity, 2);
                        successes.push(item);
                        await sleep(80);
                    } catch (err) {
                        failures.push({ item, err });
                    }
                }

                if (successes.length > 0) {
                    $(document).trigger('changeCart');

                    if (isBuyNow) {
                        await sleep(100);
                        window.location.href = '/checkout';
                    } else {
                        createToast('success', toastString.toastAddSuccessTitle,
                            `Thêm ${successes.length}/${arrItem.length} sản phẩm vào giỏ hàng`);
                    }
                }

                if (failures.length > 0) {
                    const errorMessages = failures
                        .map(f => f.err?.message || f.err)
                        .join(', ');

                    createToast('error', toastString.toastAddErrorTitle,
                        `Thất bại khi thêm ${failures.length} sản phẩm: ${errorMessages}`);
                }

            } catch (error) {
                createToast('error', toastString.toastAddErrorTitle, error.message || error);
            } finally {
                $btn.removeClass('loading');
            }
        });
    });
}