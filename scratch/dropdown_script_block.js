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

                function toggleStickyBar(e) {
                    const stickyBar = document.getElementById('sticky-cart-bar');
                    if (!stickyBar) return;
                    
                    const threshold = window.innerWidth <= 768 ? 200 : 600;
                    let scrollY = window.scrollY || document.documentElement.scrollTop || document.body.scrollTop || 0;
                    
                    if (scrollY === 0) {
                        const wrappers = document.querySelectorAll('.bodywrap, .wrapper, #wrapper, .page-body, main, #main, #nava-master-wrapper');
                        for (let i=0; i<wrappers.length; i++) {
                            if (wrappers[i].scrollTop > scrollY) scrollY = wrappers[i].scrollTop;
                        }
                    }
                    
                    if (e && e.target && e.target.scrollTop > scrollY) {
                        if (e.target.clientHeight && e.target.clientHeight > window.innerHeight * 0.5) {
                            scrollY = e.target.scrollTop;
                        }
                    }
                    
                    if (scrollY > threshold && !isBsOpen) {
                        stickyBar.style.setProperty('transform', 'translateY(0)', 'important');
                        stickyBar.style.setProperty('display', 'block', 'important');
                    } else {
                        stickyBar.style.setProperty('transform', 'translateY(120%)', 'important');
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
                        if (window.innerWidth <= 768 && !isBsOpen) {
                            openBottomSheet();
                            return;
                        }
                        closeBottomSheet();
                        triggerCartOpen(e);
                    };

                    window.triggerCheckout = (e) => {
                        if (e) e.preventDefault();
                        if (window.innerWidth <= 768 && !isBsOpen) {
                            openBottomSheet();
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
            