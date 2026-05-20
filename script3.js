
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
            