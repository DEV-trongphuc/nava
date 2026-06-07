
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
                let activeRamName = 'NO RAM';
                let activeSsdName = 'NO SSD';
                
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
                            if (window.innerWidth <= 768) {
                                hideNudgeBanner();
                                openBottomSheet();
                            } else {
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

                // Show sticky bar on scroll
                // Show sticky bar on scroll
                // Show sticky bar on scroll
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
                            
                            const threshold = window.innerWidth <= 768 ? 400 : 600;
                            let scrollY = window.scrollY || document.documentElement.scrollTop || document.body.scrollTop || 0;
                            
                            if (scrollY === 0) {
                                if (!cachedWrappers) {
                                    cachedWrappers = document.querySelectorAll('.bodywrap, .wrapper, #wrapper, .page-body, main, #main');
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
                            
                            if (scrollY > threshold) {
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

                document.addEventListener('DOMContentLoaded', function() {
                    const stickyBar = document.getElementById('sticky-cart-bar');
                    if (stickyBar) {
                        stickyBar.style.setProperty('z-index', '2147483647', 'important');
                        if (stickyBar.parentNode !== document.body) {
                            document.body.appendChild(stickyBar);
                        }
                    }
                    toggleStickyBar(); // Check immediately on load
 
                    // Call checkRAMSSDPrompt on load
                    setTimeout(checkRAMSSDPrompt, 100);

                    // Toggle dropdowns on click for mobile/touch
                    document.querySelectorAll('.nava-dropdown-display').forEach(display => {
                        display.addEventListener('click', function(e) {
                            e.stopPropagation();
                            const wrapper = this.closest('.nava-dropdown-wrapper');
                            const wasActive = wrapper.classList.contains('active');

                            // Close all dropdowns first
                            document.querySelectorAll('.nava-dropdown-wrapper').forEach(w => w.classList.remove('active'));

                            if (!wasActive) {
                                wrapper.classList.add('active');
                            }
                        });
                    });

                    // Close dropdowns on clicking outside
                    document.addEventListener('click', function() {
                        document.querySelectorAll('.nava-dropdown-wrapper').forEach(w => w.classList.remove('active'));
                    });
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
                
                window.openLightbox = function() {
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
            