document.addEventListener('DOMContentLoaded', () => {
    // ============================================
    // 0. AUTO-INJECT MASTER WRAPPER (SAPO RESCUE)
    // ============================================
    let masterWrapper = document.getElementById('nava-master-wrapper');
    if (!masterWrapper) {
        const header = document.querySelector('.header');
        if (header && header.parentElement) {
            const containerNode = header.parentElement;
            masterWrapper = document.createElement('div');
            masterWrapper.id = 'nava-master-wrapper';
            
            // Move all children except scripts to masterWrapper to avoid re-executing scripts
            const children = Array.from(containerNode.childNodes);
            children.forEach(child => {
                if (child.nodeName !== 'SCRIPT') {
                    masterWrapper.appendChild(child);
                }
            });
            containerNode.prepend(masterWrapper);
        }
    }

    // 1. INTERSECTION OBSERVER FOR SCROLL ANIMATIONS
    const revealElements = document.querySelectorAll('.reveal');

    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                observer.unobserve(entry.target);
            }
        });
    }, {
        root: document.getElementById('nava-master-wrapper') || null, 
        threshold: 0.15, 
        rootMargin: "0px 0px -50px 0px"
    });

    revealElements.forEach(el => revealObserver.observe(el));

    // 2. MOUSE PARALLAX EFFECT FOR HERO SECTION
    const heroSection = document.querySelector('.hero-3d');
    const floatingPC = document.querySelector('.floating-pc');
    const energyRing = document.querySelector('.energy-ring');

    if (heroSection && floatingPC && energyRing) {
        heroSection.addEventListener('mousemove', (e) => {
            const x = (window.innerWidth - e.pageX * 2) / 90;
            const y = (window.innerHeight - e.pageY * 2) / 90;
            floatingPC.style.transform = `translateX(${x}px) translateY(${y}px)`;
            energyRing.style.transform = `translateX(${x * 0.5}px) translateY(${y * 0.5}px) rotate(${e.pageX / 10}deg)`;
        });

        heroSection.addEventListener('mouseleave', () => {
            floatingPC.style.transform = `translateX(0) translateY(0)`;
            energyRing.style.transform = `translateX(0) translateY(0) rotate(0deg)`;
        });
    }

    // 3. SMART STICKY HEADER & SCROLL PROGRESS & BACK TO TOP
    const header = document.querySelector('.header');

    // Dynamic top-bar height calculation for sticky header
    const updateTopBarHeight = () => {
        const topBar = document.querySelector('.top-bar');
        if (topBar && header) {
            header.style.setProperty('--top-bar-height', `${topBar.offsetHeight}px`);
        }
    };
    updateTopBarHeight();
    window.addEventListener('resize', updateTopBarHeight);

    const progressBar = document.getElementById("myBar");
    const progressContainer = document.getElementById("progressContainer");
    const backToTopBtn = document.getElementById("backToTop");
    let lastScroll = 0;
    let isScrolling = false;

    // Use master wrapper if it exists (for Sapo), else fallback to window
    // masterWrapper was already declared at the top of the file
    masterWrapper = document.getElementById('nava-master-wrapper');
    const scrollTarget = masterWrapper || window;

    scrollTarget.addEventListener('scroll', () => {
        const currentScroll = masterWrapper ? masterWrapper.scrollTop : (window.pageYOffset || document.documentElement.scrollTop);

        // Header Sticky Logic: hide on scroll down, show on scroll up
        if (currentScroll > 150) {
            if (currentScroll > lastScroll + 5) {
                // Scrolling DOWN (with 5px threshold to avoid flicker)
                header.classList.add('scrolled');
            } else if (currentScroll < lastScroll - 5) {
                // Scrolling UP → show header immediately
                header.classList.remove('scrolled');
            }
            if (progressContainer) progressContainer.classList.add('active');
        } else {
            // Near top → always show header
            header.classList.remove('scrolled');
            if (progressContainer) progressContainer.classList.remove('active');
        }

        // Calculate Scroll Percentage
        const scrollHeight = masterWrapper ? masterWrapper.scrollHeight : document.documentElement.scrollHeight;
        const clientHeight = masterWrapper ? masterWrapper.clientHeight : document.documentElement.clientHeight;
        const height = scrollHeight - clientHeight;
        const scrollPercentage = (height > 0) ? (currentScroll / height) * 100 : 0;

        // Back To Top Button Logic
        if (backToTopBtn) {
            if (scrollPercentage > 50) {
                backToTopBtn.classList.add('show');
            } else {
                backToTopBtn.classList.remove('show');
            }
        }

        // Progress Bar Logic
        if (progressBar) {
            progressBar.style.width = scrollPercentage + "%";
        }

        lastScroll = currentScroll <= 0 ? 0 : currentScroll;
    }, { passive: true });

    if (backToTopBtn) {
        backToTopBtn.addEventListener('click', () => {
            if (masterWrapper) {
                masterWrapper.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            } else {
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            }
        });
    }

    // 4. MOBILE SIDEBAR LOGIC
    const menuToggle = document.querySelector('.mobile-menu-toggle');
    const sidebarDrawer = document.querySelector('.sidebar-drawer');
    const sidebarOverlay = document.querySelector('.sidebar-overlay');
    const sidebarClose = document.querySelector('.sidebar-close');
    const mobileNavContainer = document.querySelector('.mobile-nav');
    const mainNavItems = document.querySelectorAll('.main-nav .nav-item');

    if (mobileNavContainer && mobileNavContainer.children.length === 0) {
        mainNavItems.forEach(item => {
            const clone = item.cloneNode(true);
            const dropdown = clone.querySelector('.dropdown-menu');
            if (dropdown) {
                const parentText = clone.querySelector('a > span')?.innerText || '';
                const header = document.createElement('div');
                header.className = 'mobile-submenu-header';
                header.innerHTML = `<h3>${parentText}</h3>`;
                dropdown.prepend(header);
            }
            mobileNavContainer.appendChild(clone);
        });
    }

    const toggleSidebar = (state) => {
        if (state) {
            sidebarDrawer.classList.add('active');
            sidebarOverlay.classList.add('active');
            document.body.style.overflow = 'hidden';
            
            if (mobileNavContainer) {
                const hasOpen = mobileNavContainer.querySelector('.nav-item.open');
                if (!hasOpen) {
                    const dropdowns = mobileNavContainer.querySelectorAll('.nav-item.has-dropdown');
                    let targetDropdown = dropdowns[0];
                    dropdowns.forEach(d => {
                        if (d.textContent.includes('Mini PC')) {
                            targetDropdown = d;
                        }
                    });
                    if (targetDropdown) {
                        targetDropdown.classList.add('open');
                    }
                }
            }
        } else {
            sidebarDrawer.classList.remove('active');
            sidebarOverlay.classList.remove('active');
            document.body.style.overflow = '';
        }
    };

    if (menuToggle) menuToggle.addEventListener('click', () => toggleSidebar(true));
    if (sidebarClose) sidebarClose.addEventListener('click', () => toggleSidebar(false));
    if (sidebarOverlay) sidebarOverlay.addEventListener('click', () => toggleSidebar(false));

    // Mobile sidebar: toggle submenu on click for items with dropdown
    if (mobileNavContainer) {
        mobileNavContainer.querySelectorAll('.nav-item.has-dropdown > a').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const navItem = link.closest('.nav-item');
                const isOpen = navItem.classList.contains('open');
                // Close all others
                mobileNavContainer.querySelectorAll('.nav-item.open').forEach(el => el.classList.remove('open'));
                if (!isOpen) navItem.classList.add('open');
            });
        });
    }

    // 5. PRODUCT SLIDER DOTS LOGIC (MOBILE)
    const productGrid = document.querySelector('.product-grid');
    const dotsContainer = document.querySelector('.slider-dots');

    if (productGrid && dotsContainer && window.innerWidth <= 991) {
        const cards = productGrid.querySelectorAll('.product-card');

        cards.forEach((_, index) => {
            const dot = document.createElement('div');
            dot.classList.add('dot');
            if (index === 0) dot.classList.add('active');
            dot.addEventListener('click', () => {
                productGrid.scrollTo({
                    left: cards[index].offsetLeft - (productGrid.offsetWidth - cards[index].offsetWidth) / 2,
                    behavior: 'smooth'
                });
            });
            dotsContainer.appendChild(dot);
        });

        productGrid.addEventListener('scroll', () => {
            const scrollLeft = productGrid.scrollLeft;
            const cardWidth = cards[0].offsetWidth + 20;
            const activeIndex = Math.round(scrollLeft / cardWidth);

            const dots = dotsContainer.querySelectorAll('.dot');
            dots.forEach((dot, index) => {
                dot.classList.toggle('active', index === activeIndex);
            });
        });
    }

    // 6. FLOATING CONTACT TOGGLE
    const contactWrapper = document.querySelector('.floating-contact');
    const contactMainBtn = document.querySelector('.main-contact-btn');

    if (contactMainBtn && contactWrapper) {
        contactMainBtn.addEventListener('click', () => {
            contactWrapper.classList.toggle('active');
        });

        // Close when clicking outside
        document.addEventListener('click', (e) => {
            if (!contactWrapper.contains(e.target)) {
                contactWrapper.classList.remove('active');
            }
        });
    }

    // Removed duplicate scroll progress bar logic

    // ============================================
    // 7. HERO PRODUCT SLIDER
    // ============================================
    const heroSlides = document.querySelectorAll('.hero-slide');
    const heroDots = document.querySelectorAll('.h-dot');
    const floatLabel1 = document.getElementById('floatLabel1');
    const floatSub1 = document.getElementById('floatSub1');
    const floatIcon1 = document.getElementById('floatIcon1');
    const floatLabel2 = document.getElementById('floatLabel2');
    const floatSub2 = document.getElementById('floatSub2');
    const floatIcon2 = document.getElementById('floatIcon2');
    const floatItem1 = document.getElementById('floatItem1');
    const floatItem2 = document.getElementById('floatItem2');

    // Data per slide: [icon-class, label, sub, icon2-class, label2, sub2]
    const heroSlideData = [
        {
            i1: 'ph-fill ph-cpu', l1: 'Core Ultra 9', s1: 'Xử lý đỉnh cao',
            i2: 'ph-fill ph-lightning', l2: 'AI NPU', s2: 'Tích hợp sẵn'
        },
        {
            i1: 'ph-fill ph-game-controller', l1: 'ROG Gaming', s1: 'Hiệu năng đỉnh',
            i2: 'https://images.seeklogo.com/logo-png/66/1/openclaw-logo-png_seeklogo-665449.png', l2: 'Openclaw', s2: 'Sức mạnh vượt trội'
        },
        {
            i1: 'ph-fill ph-graphics-card', l1: 'RTX 5090', s1: 'Sức mạnh đồ họa',
            i2: 'ph-fill ph-usb', l2: 'USB4 / TB4', s2: 'Kết nối siêu tốc'
        },
        {
            i1: 'ph-fill ph-memory', l1: 'LPDDR5X 6400', s1: 'Băng thông đỉnh',
            i2: 'ph-fill ph-hard-drive', l2: 'NVMe PCIe 4.0', s2: '7,400 MB/s'
        },
        {
            i1: 'ph-fill ph-game-controller', l1: 'ROG NUC', s1: 'Sức mạnh tuyệt đối',
            i2: 'https://images.seeklogo.com/logo-png/66/1/openclaw-logo-png_seeklogo-665449.png', l2: 'Openclaw', s2: 'Sức mạnh vượt trội'
        },
    ];

    let heroCurrentSlide = 0;
    let heroAutoPlay;

    function goToHeroSlide(index) {
        // Remove active from all
        heroSlides.forEach(s => s.classList.remove('active', 'exit'));
        heroDots.forEach(d => d.classList.remove('active'));

        // Set new active
        heroCurrentSlide = (index + heroSlides.length) % heroSlides.length;
        heroSlides[heroCurrentSlide].classList.add('active');
        if (heroDots[heroCurrentSlide]) heroDots[heroCurrentSlide].classList.add('active');

        // Animate floating items out then update
        if (floatItem1 && floatItem2) {
            floatItem1.classList.add('float-exit');
            floatItem2.classList.add('float-exit');
            setTimeout(() => {
                const d = heroSlideData[heroCurrentSlide];

                const setIcon = (el, iconVal) => {
                    if (iconVal.startsWith('http')) {
                        el.className = '';
                        el.style.backgroundImage = `url(${iconVal})`;
                        el.style.backgroundSize = 'contain';
                        el.style.backgroundRepeat = 'no-repeat';
                        el.style.backgroundPosition = 'center';
                        el.style.width = '24px';
                        el.style.height = '24px';
                        el.style.display = 'inline-block';
                    } else {
                        el.style.backgroundImage = '';
                        el.style.width = '';
                        el.style.height = '';
                        el.style.display = '';
                        el.className = iconVal;
                    }
                };

                setIcon(floatIcon1, d.i1);
                floatLabel1.textContent = d.l1;
                floatSub1.textContent = d.s1;
                setIcon(floatIcon2, d.i2);
                floatLabel2.textContent = d.l2;
                floatSub2.textContent = d.s2;
                floatItem1.classList.remove('float-exit');
                floatItem2.classList.remove('float-exit');
                floatItem1.classList.add('float-enter');
                floatItem2.classList.add('float-enter');
                setTimeout(() => {
                    floatItem1.classList.remove('float-enter');
                    floatItem2.classList.remove('float-enter');
                }, 500);
            }, 300);
        }
    }

    function startHeroAutoPlay() {
        heroAutoPlay = setInterval(() => {
            goToHeroSlide(heroCurrentSlide + 1);
        }, 3500);
    }

    if (heroSlides.length > 0) {
        startHeroAutoPlay();
        heroDots.forEach(dot => {
            dot.addEventListener('click', () => {
                clearInterval(heroAutoPlay);
                goToHeroSlide(parseInt(dot.dataset.slide));
                startHeroAutoPlay();
            });
        });

        const heroSliderEl = document.getElementById('heroSlider');
        const heroPrevBtn = document.getElementById('heroPrevBtn');
        const heroNextBtn = document.getElementById('heroNextBtn');

        if (heroPrevBtn) heroPrevBtn.addEventListener('click', () => {
            clearInterval(heroAutoPlay);
            goToHeroSlide(heroCurrentSlide - 1);
            startHeroAutoPlay();
        });

        if (heroNextBtn) heroNextBtn.addEventListener('click', () => {
            clearInterval(heroAutoPlay);
            goToHeroSlide(heroCurrentSlide + 1);
            startHeroAutoPlay();
        });

        const heroImageContainer = document.querySelector('.hero-image');
        if (heroImageContainer) {
            let startX = 0;
            let endX = 0;
            
            heroImageContainer.addEventListener('touchstart', e => {
                startX = e.changedTouches[0].screenX;
            }, {passive: true});

            heroImageContainer.addEventListener('touchend', e => {
                endX = e.changedTouches[0].screenX;
                handleHeroSwipe();
            }, {passive: true});

            heroImageContainer.addEventListener('mousedown', e => {
                startX = e.screenX;
            });

            heroImageContainer.addEventListener('mouseup', e => {
                endX = e.screenX;
                handleHeroSwipe();
            });

            function handleHeroSwipe() {
                const threshold = 50;
                if (endX < startX - threshold) {
                    clearInterval(heroAutoPlay);
                    goToHeroSlide(heroCurrentSlide + 1);
                    startHeroAutoPlay();
                } else if (endX > startX + threshold) {
                    clearInterval(heroAutoPlay);
                    goToHeroSlide(heroCurrentSlide - 1);
                    startHeroAutoPlay();
                }
            }
        }
    }

    // ============================================
    // 8. STATS COUNTER ANIMATION (on scroll in)
    // ============================================
    const statNumbers = document.querySelectorAll('.stat-number[data-target]');

    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                const target = parseInt(el.dataset.target);
                const duration = 2000;
                const frames = 60;
                const stepTime = duration / frames;
                let currentFrame = 0;

                const timer = setInterval(() => {
                    currentFrame++;
                    if (currentFrame >= frames) {
                        el.textContent = target.toLocaleString('vi-VN');
                        clearInterval(timer);
                    } else {
                        // Ease out cubic
                        const progress = currentFrame / frames;
                        const easeOut = 1 - Math.pow(1 - progress, 3);
                        const currentVal = Math.floor(target * easeOut);
                        el.textContent = currentVal.toLocaleString('vi-VN');
                    }
                }, stepTime);
                counterObserver.unobserve(el);
            }
        });
    }, { 
        root: masterWrapper || null,
        threshold: 0.5 
    });

    statNumbers.forEach(el => counterObserver.observe(el));

    // ============================================
    // 9. BENCHMARK BAR ANIMATION (on scroll in)
    // ============================================
    const benchFills = document.querySelectorAll('.bench-fill[data-width]');

    const benchObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                el.style.width = el.dataset.width + '%';
                benchObserver.unobserve(el);
            }
        });
    }, { 
        root: masterWrapper || null,
        threshold: 0.3 
    });

    benchFills.forEach(el => benchObserver.observe(el));

    // ============================================
    // 10. TERMINAL TYPING ANIMATION (on scroll in)
    // ============================================
    const terminalLines = [
        { cls: '', html: '<span class="t-prompt">$</span> <span class="t-cmd">run benchmark --device minisforum-um890</span>' },
        { cls: 't-out', html: '[INFO] CPU: AMD Ryzen 9 8945HX @ 5.2GHz' },
        { cls: 't-out', html: '[INFO] RAM: 64GB LPDDR5X-6400' },
        { cls: 't-out', html: '[INFO] GPU: Radeon 890M iGPU' },
        { cls: 't-success', html: '[PASS] Cinebench R24 Multi: <b>24,819 pts</b>' },
        { cls: 't-success', html: '[PASS] CrystalDisk Read: <b>7,412 MB/s</b>' },
        { cls: 't-success', html: '[PASS] LLM Inference: <b>42 tok/s</b>' },
        { cls: 't-warn', html: '[TEMP] Peak Temp: 74°C ✓ Under threshold' },
        { cls: 't-success', html: '[PASS] Total Power Draw: <b>28W</b> ✅' },
        { cls: 't-success', html: '[PASS] Size (Space Saving): <b>2000%</b> ✨' },
        { cls: 't-blink', html: '<span class="t-cursor">█</span> Benchmark complete — Score: <span class="t-highlight">ELITE</span>' },
    ];

    const terminalBody = document.getElementById('terminalOutput');
    let terminalStarted = false;

    function runTerminalAnimation() {
        if (terminalStarted || !terminalBody) return;
        terminalStarted = true;
        terminalBody.innerHTML = '';

        terminalLines.forEach((lineData, i) => {
            const div = document.createElement('div');
            div.className = 't-line' + (lineData.cls ? ' ' + lineData.cls : '');
            div.innerHTML = lineData.html;
            terminalBody.appendChild(div);

            setTimeout(() => {
                div.classList.add('visible');
            }, i * 380);
        });
    }

    const terminalEl = document.getElementById('benchTerminal');
    if (terminalEl) {
        const termObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    runTerminalAnimation();
                    termObserver.unobserve(entry.target);
                }
            });
        }, { 
            root: masterWrapper || null,
            threshold: 0.3 
        });
        termObserver.observe(terminalEl);
    }

    // ============================================
    // 11. THEME TOGGLE
    // ============================================
    const themeToggleBtn = document.getElementById('theme-toggle');
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            if (currentTheme === 'dark') {
                document.documentElement.removeAttribute('data-theme');
                localStorage.setItem('nava-theme', 'light');
            } else {
                document.documentElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('nava-theme', 'dark');
            }
        });
    }
    // ============================================
    // 12. 3D TILT EFFECT & MAGNETIC BUTTONS (Tech Animations)
    // ============================================
    const isTouchDevice = window.matchMedia("(pointer: coarse)").matches;

    if (!isTouchDevice) {
        // A. 3D Tilt for product cards & bento boxes
        const tiltElements = document.querySelectorAll('.product-card, .bento-box');

        tiltElements.forEach(el => {
            el.addEventListener('mousemove', (e) => {
                const rect = el.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;

                const centerX = rect.width / 2;
                const centerY = rect.height / 2;

                const rotateX = ((y - centerY) / centerY) * -5;
                const rotateY = ((x - centerX) / centerX) * 5;

                el.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;

                let glare = el.querySelector('.glare');
                if (!glare) {
                    glare = document.createElement('div');
                    glare.className = 'glare';
                    el.appendChild(glare);
                    el.style.position = 'relative';
                    el.style.overflow = 'hidden';
                }
                const percentX = (x / rect.width) * 100;
                const percentY = (y / rect.height) * 100;
                glare.style.background = `radial-gradient(circle at ${percentX}% ${percentY}%, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0) 60%)`;
                glare.style.opacity = '1';
            });

            el.addEventListener('mouseleave', () => {
                el.style.transform = `perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)`;
                const glare = el.querySelector('.glare');
                if (glare) glare.style.opacity = '0';
            });
        });

        // B. Magnetic Hover for CTA buttons
        const magneticBtns = document.querySelectorAll('.hero-cta .btn-pill, .social-btn');

        magneticBtns.forEach(btn => {
            btn.addEventListener('mousemove', (e) => {
                const rect = btn.getBoundingClientRect();
                const x = e.clientX - rect.left - rect.width / 2;
                const y = e.clientY - rect.top - rect.height / 2;
                btn.style.transform = `translate(${x * 0.2}px, ${y * 0.2}px)`;
            });

            btn.addEventListener('mouseleave', () => {
                btn.style.transform = 'translate(0px, 0px)';
            });
        });
    }


    // 12. WARRANTY MODAL
    const openWarrantyBtn = document.getElementById('open-warranty-modal');
    const openWarrantyBtnFooter = document.getElementById('open-warranty-modal-footer');
    const openWarrantyBtnHeader = document.getElementById('open-warranty-modal-header');
    const warrantyModal = document.getElementById('warranty-modal');
    const closeWarrantyBtn = document.getElementById('close-warranty-modal');

    if (warrantyModal && closeWarrantyBtn) {
        const openModal = (e) => {
            e.preventDefault();
            warrantyModal.classList.add('active');
            document.body.style.overflow = 'hidden';
        };

        if (openWarrantyBtn) openWarrantyBtn.addEventListener('click', openModal);
        if (openWarrantyBtnFooter) openWarrantyBtnFooter.addEventListener('click', openModal);
        
        document.querySelectorAll('#open-warranty-modal-header').forEach(btn => {
            btn.addEventListener('click', (e) => {
                openModal(e);
                const sidebarDrawer = document.querySelector('.sidebar-drawer');
                const sidebarOverlay = document.querySelector('.sidebar-overlay');
                if (sidebarDrawer) sidebarDrawer.classList.remove('active');
                if (sidebarOverlay) sidebarOverlay.classList.remove('active');
            });
        });

        closeWarrantyBtn.addEventListener('click', () => {
            warrantyModal.classList.remove('active');
            document.body.style.overflow = '';
        });

        warrantyModal.addEventListener('click', (e) => {
            if (e.target === warrantyModal) {
                warrantyModal.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    }
    // 13. TESTIMONIAL SLIDER REBORN
    const testiTrack = document.querySelector('.testimonial-track');
    const testiCards = document.querySelectorAll('.testimonial-card');
    const testiDotsContainer = document.querySelector('.testi-dots');

    if (testiTrack && testiCards.length > 0 && testiDotsContainer) {
        let currentIndex = 0;
        let cardsPerView = 3;
        let testiAutoPlay;

        function updateLayout() {
            if (window.innerWidth <= 768) cardsPerView = 1;
            else if (window.innerWidth <= 1024) cardsPerView = 2;
            else cardsPerView = 3;
            
            buildDots();
            goToSlide(0);
        }

        function buildDots() {
            testiDotsContainer.innerHTML = '';
            const numDots = Math.max(1, testiCards.length - cardsPerView + 1);
            for (let i = 0; i < numDots; i++) {
                const dot = document.createElement('div');
                dot.className = 'testi-dot' + (i === 0 ? ' active' : '');
                dot.addEventListener('click', () => {
                    goToSlide(i);
                    resetAutoPlay();
                });
                testiDotsContainer.appendChild(dot);
            }
        }

        function goToSlide(index) {
            const numDots = Math.max(1, testiCards.length - cardsPerView + 1);
            if (index >= numDots) index = 0;
            if (index < 0) index = numDots - 1;
            
            currentIndex = index;
            
            const cardWidth = testiCards[0].offsetWidth;
            const gap = 30; // From CSS
            const translation = -(currentIndex * (cardWidth + gap));
            
            testiTrack.style.transform = `translateX(${translation}px)`;
            
            const dots = document.querySelectorAll('.testi-dot');
            dots.forEach((dot, i) => {
                dot.classList.toggle('active', i === currentIndex);
            });
        }

        function resetAutoPlay() {
            clearInterval(testiAutoPlay);
            testiAutoPlay = setInterval(() => {
                goToSlide(currentIndex + 1);
            }, 4000);
        }

        window.addEventListener('resize', () => {
            updateLayout();
        });

        // Initialize
        updateLayout();
        resetAutoPlay();
        
        testiTrack.parentElement.addEventListener('mouseenter', () => clearInterval(testiAutoPlay));
        testiTrack.parentElement.addEventListener('mouseleave', resetAutoPlay);
    }

});
