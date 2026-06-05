// =========================================================================
// NAVA PRE-LOAD INTERCEPTORS & FALLBACKS (PAGESPEED INSIGHTS OPTIMIZATION)
// =========================================================================

(function() {
    // 1. Suppress platform-level and third-party warnings from Console logs
    const originalConsoleError = console.error;
    console.error = function (...args) {
        const msg = args.join(' ');
        if (msg.includes('FedCM') || msg.includes('GoogleOneTap') || msg.includes('RecentProducts') || msg.includes('recentCompare')) {
            return;
        }
        originalConsoleError.apply(console, args);
    };

    // 2. Intercept iframe creation to block Google One Tap dynamic injection (fixes cookie warnings and network DNS errors)
    const originalCreateElement = document.createElement;
    document.createElement = function (tagName) {
        const el = originalCreateElement.call(document, tagName);
        if (tagName.toLowerCase() === 'iframe') {
            const originalSetAttribute = el.setAttribute;
            el.setAttribute = function (name, value) {
                if (name === 'src' && value && value.includes('GoogleOneTap')) {
                    // Block third-party cookie source
                    return;
                }
                originalSetAttribute.call(el, name, value);
            };
            Object.defineProperty(el, 'src', {
                set: function (val) {
                    if (val && val.includes('GoogleOneTap')) {
                        return;
                    }
                    el.setAttribute('src', val);
                },
                get: function () {
                    return el.getAttribute('src');
                }
            });
        }
        return el;
    };
})();

// 3. Fallback definition to prevent ReferenceError: RecentProducts is not defined
if (typeof window.RecentProducts === 'undefined') {
    window.RecentProducts = class {
        constructor() {
            // Mock constructor to prevent Sapo layout script crashes
        }
        init() {
            // Mock init to prevent TypeError: recentCompare.init is not a function
        }
    };
}

document.addEventListener('DOMContentLoaded', () => {
    // ============================================
    // 0. AUTO-INJECT MASTER WRAPPER (SAPO RESCUE)
    // ============================================
    let masterWrapper = document.getElementById('nava-master-wrapper');

    // Always force masterWrapper to be a direct child of body to escape Sapo's CSS `transform` or `filter` stacking contexts
    if (masterWrapper && masterWrapper.parentNode !== document.body) {
        document.body.appendChild(masterWrapper);
    } else if (!masterWrapper) {
        const header = document.querySelector('.header');
        if (header && header.parentElement) {
            const containerNode = header.parentElement;
            masterWrapper = document.createElement('div');
            masterWrapper.id = 'nava-master-wrapper';
            // Move all children except scripts to masterWrapper
            const children = Array.from(containerNode.childNodes);
            children.forEach(child => {
                if (child.nodeName !== 'SCRIPT') {
                    masterWrapper.appendChild(child);
                }
            });
            document.body.appendChild(masterWrapper);
        }
    }

    // Force-hide Sapo's layout completely now that we are safe in the body
    const sapoBody = document.querySelector('.page-body');
    if (sapoBody && sapoBody !== masterWrapper.parentNode) {
        sapoBody.style.display = 'none';
    }

    // Force-hide any floating widgets
    const floatingWidgets = document.querySelectorAll('.isocial_bubble, .fix-phone, .zalo-chat-widget');
    floatingWidgets.forEach(widget => {
        widget.style.display = 'none';
    });

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

    // 1.5 MAKE STAT CARDS CLICKABLE
    const allStatCards = document.querySelectorAll('.stat-card');
    allStatCards.forEach(card => {
        const label = card.querySelector('.stat-label');
        if (label) {
            card.style.cursor = 'pointer';
            card.onclick = () => {
                if (label.textContent.includes('Sản phẩm')) {
                    window.open('https://navastore.vn/tat-ca-san-pham', '_blank');
                } else if (label.textContent.includes('Điểm đánh giá')) {
                    const reviewSection = document.querySelector('.shopee-reviews-section');
                    if (reviewSection) {
                        reviewSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }
                } else {
                    // For Khách hàng and 15 Năm kinh nghiệm
                    window.open('https://shopee.vn/navastore.vn', '_blank');
                }
            };
        }
    });

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

    let isTicking = false;
    scrollTarget.addEventListener('scroll', () => {
        if (!isTicking) {
            window.requestAnimationFrame(() => {
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
                isTicking = false;
            });
            isTicking = true;
        }
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
    const searchToggle = document.querySelector('.mobile-search-toggle');
    const searchBox = document.querySelector('.search-box');

    if (searchToggle && searchBox) {
        searchToggle.addEventListener('click', () => {
            searchBox.classList.toggle('active');
            if (searchBox.classList.contains('active')) {
                searchBox.querySelector('input').focus();
            }
        });
    }
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
            i1: 'ph-fill ph-game-controller', l1: 'ROG NUC', s1: 'Sức mạnh tuyệt đối',
            i2: 'https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/logo_openclaw.png', l2: 'Openclaw', s2: 'Sức mạnh vượt trội'
        },
        {
            i1: 'ph-fill ph-cpu', l1: 'Core Ultra 9', s1: 'Xử lý đỉnh cao',
            i2: 'ph-fill ph-lightning', l2: 'AI NPU', s2: 'Tích hợp sẵn'
        },
        {
            i1: 'ph-fill ph-game-controller', l1: 'ROG Gaming', s1: 'Hiệu năng đỉnh',
            i2: 'https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/logo_openclaw.png', l2: 'Openclaw', s2: 'Sức mạnh vượt trội'
        },
        {
            i1: 'ph-fill ph-graphics-card', l1: 'RTX 5090', s1: 'Sức mạnh đồ họa',
            i2: 'ph-fill ph-usb', l2: 'USB4 / TB4', s2: 'Kết nối siêu tốc'
        },
        {
            i1: 'ph-fill ph-memory', l1: 'LPDDR5X 6400', s1: 'Băng thông đỉnh',
            i2: 'ph-fill ph-hard-drive', l2: 'NVMe PCIe 4.0', s2: '7,400 MB/s'
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
        const activeSlide = heroSlides[heroCurrentSlide];
        activeSlide.classList.add('active');
        if (heroDots[heroCurrentSlide]) heroDots[heroCurrentSlide].classList.add('active');

        // Lazy load current slide image
        const activeImg = activeSlide.querySelector('img[data-src]');
        if (activeImg) {
            activeImg.src = activeImg.getAttribute('data-src');
            activeImg.removeAttribute('data-src');
        }

        // Preload next slide's image in advance
        const nextSlide = heroSlides[(heroCurrentSlide + 1) % heroSlides.length];
        if (nextSlide) {
            const nextImg = nextSlide.querySelector('img[data-src]');
            if (nextImg) {
                nextImg.src = nextImg.getAttribute('data-src');
                nextImg.removeAttribute('data-src');
            }
        }

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
            }, { passive: true });

            heroImageContainer.addEventListener('touchend', e => {
                endX = e.changedTouches[0].screenX;
                handleHeroSwipe();
            }, { passive: true });

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
        { cls: '', html: '<span class="t-prompt">$</span> <span class="t-cmd">run benchmark --device asus-nuc-ai-350</span>' },
        { cls: 't-out', html: '[INFO] Model: NUC AI 350 (PN54)' },
        { cls: 't-out', html: '[INFO] CPU: AMD Ryzen AI 7 350 8C/16T max 5.0Ghz' },
        { cls: 't-out', html: '[INFO] RAM: 2x DDR5 5600 tối đa 128GB' },
        { cls: 't-out', html: '[INFO] GPU: AMD Radeon™ 860M' },
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
    const themeToggleBtns = document.querySelectorAll('.theme-toggle-btn, #theme-toggle');
    if (themeToggleBtns.length > 0) {
        themeToggleBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const currentTheme = document.documentElement.getAttribute('data-theme');
                if (currentTheme === 'dark') {
                    document.documentElement.removeAttribute('data-theme');
                    localStorage.setItem('nava-theme', 'light');
                } else {
                    document.documentElement.setAttribute('data-theme', 'dark');
                    localStorage.setItem('nava-theme', 'dark');
                }
            });
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

    // ============================================
    // 14. CART DRAWER LOGIC
    // ============================================
    const cartBtn = document.getElementById('header-cart-btn');
    const cartDrawer = document.getElementById('cart-drawer');
    const cartOverlay = document.getElementById('cart-drawer-overlay');
    const cartCloseBtn = document.getElementById('cart-close-btn');
    const cartCountBadge = document.getElementById('cart-count-badge');
    const cartEmptyState = document.getElementById('cart-empty-state');
    const cartLoadingState = document.getElementById('cart-loading-state');
    const cartItemsList = document.getElementById('cart-items-list');
    const cartFooter = document.getElementById('cart-drawer-footer');
    const cartTotalPrice = document.getElementById('cart-total-price');

    const toggleCartDrawer = (show) => {
        if (show) {
            cartDrawer.classList.add('active');
            cartOverlay.classList.add('active');
            document.body.style.overflow = 'hidden';
            loadCartData();
        } else {
            cartDrawer.classList.remove('active');
            cartOverlay.classList.remove('active');
            document.body.style.overflow = '';
        }
    };

    if (cartBtn) {
        cartBtn.addEventListener('click', (e) => {
            e.preventDefault();
            toggleCartDrawer(true);
        });
    }

    if (cartCloseBtn) cartCloseBtn.addEventListener('click', () => toggleCartDrawer(false));
    if (cartOverlay) cartOverlay.addEventListener('click', () => toggleCartDrawer(false));

    // Format currency
    const formatMoney = (amount) => {
        return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(amount);
    };

    const updateCartUI = (cart) => {
        cartLoadingState.style.display = 'none';

        if (!cart || !cart.items || cart.items.length === 0) {
            cartEmptyState.style.display = 'flex';
            cartItemsList.innerHTML = '';
            cartFooter.style.display = 'none';
            if (cartCountBadge) {
                cartCountBadge.style.display = 'none';
                cartCountBadge.textContent = '0';
            }
            return;
        }

        // Has items
        cartEmptyState.style.display = 'none';
        cartFooter.style.display = 'block';

        // Update badge
        if (cartCountBadge) {
            cartCountBadge.style.display = 'flex';
            cartCountBadge.textContent = cart.item_count || cart.items.length;
        }

        // Update total
        if (cartTotalPrice) {
            cartTotalPrice.textContent = formatMoney(cart.total_price);
        }

        // Render items
        cartItemsList.innerHTML = '';
        cart.items.forEach(item => {
            const itemEl = document.createElement('div');
            itemEl.className = 'cart-item';

            // Get proper image or placeholder
            let imgUrl = item.image || 'https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/logo.png';
            if (imgUrl.startsWith('//')) imgUrl = 'https:' + imgUrl;

            itemEl.innerHTML = `
                <img src="${imgUrl}" alt="${item.title}" class="cart-item-img" onerror="this.src='https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/logo.png'">
                <div class="cart-item-info">
                    <div class="cart-item-title">${item.title}</div>
                    <div class="cart-item-price">${formatMoney(item.price)}</div>
                    <div class="cart-item-actions">
                        <span class="cart-qty">SL: ${item.quantity}</span>
                    </div>
                </div>
            `;
            cartItemsList.appendChild(itemEl);
        });
    };

    const loadCartData = () => {
        cartLoadingState.style.display = 'flex';
        cartEmptyState.style.display = 'none';
        cartItemsList.innerHTML = '';
        cartFooter.style.display = 'none';

        fetch('/cart.js')
            .then(res => res.json())
            .then(cart => {
                updateCartUI(cart);
            })
            .catch(err => {
                console.error('Error fetching cart:', err);
                // Fallback to empty if failed
                updateCartUI(null);
            });
    };

    // Initial check on page load if token exists in localStorage
    if (localStorage.getItem('cart')) {
        fetch('/cart.js')
            .then(res => res.json())
            .then(cart => {
                if (cart && cart.item_count > 0 && cartCountBadge) {
                    cartCountBadge.style.display = 'flex';
                    cartCountBadge.textContent = cart.item_count;
                }
            })
            .catch(err => console.error('Error fetching initial cart data:', err));
    }

    // ----------------------------------------------------
    // NAVA FLY TO CART ANIMATION & BADGE REFRESH
    // ----------------------------------------------------
    document.addEventListener('click', function(e) {
        const btn = e.target.closest('.js-addToCart');
        if (!btn) return;
        
        const productImg = document.getElementById('main-product-image') || document.querySelector('.main-image-container img') || document.querySelector('.product-gallery img');
        const cartBtn = document.getElementById('header-cart-btn');
        
        if (productImg && cartBtn) {
            // Create flying cloned image
            const clone = productImg.cloneNode(true);
            const rectImg = productImg.getBoundingClientRect();
            const rectCart = cartBtn.getBoundingClientRect();
            
            clone.style.position = 'fixed';
            clone.style.zIndex = '999999';
            clone.style.top = rectImg.top + 'px';
            clone.style.left = rectImg.left + 'px';
            clone.style.width = rectImg.width + 'px';
            clone.style.height = rectImg.height + 'px';
            clone.style.borderRadius = '50%';
            clone.style.objectFit = 'cover';
            clone.style.pointerEvents = 'none';
            clone.style.transition = 'all 0.9s cubic-bezier(0.42, 0, 0.58, 1)';
            
            document.body.appendChild(clone);
            
            // Trigger transition
            requestAnimationFrame(() => {
                clone.style.top = (rectCart.top + rectCart.height / 2 - 15) + 'px';
                clone.style.left = (rectCart.left + rectCart.width / 2 - 15) + 'px';
                clone.style.width = '30px';
                clone.style.height = '30px';
                clone.style.opacity = '0.2';
            });
            
            // Wobble cart icon when reached and update local badge immediately
            setTimeout(() => {
                clone.remove();
                
                // Add wobble animation class
                cartBtn.classList.add('nava-wobble');
                setTimeout(() => {
                    cartBtn.classList.remove('nava-wobble');
                }, 600);
                
                // Optimistically increment badge count
                if (cartCountBadge) {
                    cartCountBadge.style.display = 'flex';
                    const qtyInput = document.getElementById('qtym');
                    const qtyVal = qtyInput ? parseInt(qtyInput.value) || 1 : 1;
                    const currentCount = parseInt(cartCountBadge.textContent) || 0;
                    cartCountBadge.textContent = currentCount + qtyVal;
                }
            }, 900);
        }
    });

    // Listen to MewTheme's add-to-cart events to fetch Sapo's real cart data and open drawer
    const handleCartChangedEvent = () => {
        fetch('/cart.js')
            .then(res => res.json())
            .then(cart => {
                updateCartUI(cart);
                // Open drawer automatically
                toggleCartDrawer(true);
            })
            .catch(err => console.error('Error reloading cart data:', err));
    };

    document.addEventListener('changeCart', handleCartChangedEvent);
    if (window.jQuery || window.$) {
        $(document).on('changeCart', handleCartChangedEvent);
    }




// ============================================
// 11. SHOPEE REVIEWS REALTIME API
// ============================================
const shopeeList = document.getElementById('shopeeCommentsList');
if (shopeeList) {
    const shopeeApiUrl = 'https://automation.ideas.edu.vn/meta_report/shopee_proxy.php?type=reviews&limit=6';

    const shopeeSummaryUrl = 'https://automation.ideas.edu.vn/meta_report/shopee_proxy.php?type=summary';
    const summaryEl = document.getElementById('shopeeRatingSummary');

    async function fetchShopeeReviews() {
        try {
            // Fetch reviews and summary concurrently
            const [resReviews, resSummary] = await Promise.all([
                fetch(shopeeApiUrl, { headers: { 'Accept': 'application/json' } }).catch(() => null),
                fetch(shopeeSummaryUrl, { headers: { 'Accept': 'application/json' } }).catch(() => null)
            ]);

            if (resSummary && resSummary.ok) {
                const dataSum = await resSummary.json();
                if (dataSum && dataSum.data && dataSum.data.seller_rating_summary) {
                    renderShopeeSummary(dataSum.data.seller_rating_summary);
                }
            } else {
                throw new Error("Summary fetch failed");
            }

            if (resReviews && resReviews.ok) {
                const dataRev = await resReviews.json();
                if (dataRev && dataRev.data && dataRev.data.items) {
                    renderShopeeReviews(dataRev.data.items);
                }
            } else {
                throw new Error("Reviews fetch failed");
            }
        } catch (error) {
            console.warn("Shopee API blocked by CORS or error. Using fallback data.", error);
            renderShopeeSummary(getMockShopeeSummary());
            renderShopeeReviews(getMockShopeeData());
        }
    }

    function renderShopeeSummary(summary) {
        if (!summaryEl) return;
        const total = summary.rating_total || 2419;
        const starStr = Number(summary.rating_star || 4.97).toFixed(1);
        // array mapping to 1, 2, 3, 4, 5 stars
        const counts = summary.rating_count || [3, 1, 7, 23, 2385];

        // Update realtime customer stat in hero section
        const realtimeCustomerCountEl = document.getElementById('realtime-customer-count');
        if (realtimeCustomerCountEl) {
            realtimeCustomerCountEl.dataset.target = total;
            // If it already animated (text content is not 0), update the text content
            if (realtimeCustomerCountEl.textContent !== '0') {
                realtimeCustomerCountEl.textContent = total.toLocaleString('vi-VN');
            }
        }

        // Update realtime rating stat in hero section
        const statCards = document.querySelectorAll('.stat-card');
        statCards.forEach(card => {
            const label = card.querySelector('.stat-label');
            if (label && label.textContent.includes('Điểm đánh giá trung bình')) {
                const numberEl = card.querySelector('.stat-number');
                const suffixEl = card.querySelector('.stat-suffix');
                if (numberEl && suffixEl) {
                    const [intPart, decPart] = starStr.split('.');
                    numberEl.dataset.target = intPart;
                    if (numberEl.textContent !== '0') {
                        numberEl.textContent = intPart;
                    }
                    suffixEl.textContent = `.${decPart}★`;
                }
            }
        });

        // Build bars (from 5 down to 1)
        let barsHtml = '';
        for (let i = 5; i >= 1; i--) {
            const count = counts[i - 1] || 0;
            const percent = total > 0 ? (count / total) * 100 : 0;
            barsHtml += `
                <div class="sr-bar-row">
                    <span class="sr-star-label">${i} <i class="ph-fill ph-star"></i></span>
                    <div class="sr-progress"><div class="sr-fill" style="width: ${percent}%"></div></div>
                    <span class="sr-count">${count}</span>
                </div>`;
        }

        // Overview stars
        const scoreNum = parseFloat(starStr);
        let starsHtml = '';
        for (let i = 1; i <= 5; i++) {
            if (i <= scoreNum) {
                starsHtml += '<i class="ph-fill ph-star"></i>';
            } else if (i - 0.5 <= scoreNum) {
                starsHtml += '<i class="ph-fill ph-star-half"></i>';
            } else {
                starsHtml += '<i class="ph ph-star"></i>'; // empty star
            }
        }

        summaryEl.innerHTML = `
                <div class="sr-overview-card" style="cursor: pointer;" onclick="window.open(window.innerWidth <= 768 ? 'https://shopee.vn/navastore.vn' : 'https://shopee.vn/buyer/65858058/rating?shop_id=65856601', '_blank')">
                    <div class="sr-card-title">ĐIỂM TRUNG BÌNH</div>
                    <div class="sr-score">${starStr}</div>
                    <div class="sr-stars">${starsHtml}</div>
                    <div class="sr-total">${total.toLocaleString()} đánh giá</div>
                </div>
                <div class="sr-bars-card" style="cursor: pointer;" onclick="window.open(window.innerWidth <= 768 ? 'https://shopee.vn/navastore.vn' : 'https://shopee.vn/buyer/65858058/rating?shop_id=65856601', '_blank')">
                    <div class="sr-card-title">PHÂN BỐ ĐÁNH GIÁ</div>
                    <div class="sr-bars">
                        ${barsHtml}
                    </div>
                </div>
            `;
        summaryEl.style.display = 'flex';
    }

    function getMockShopeeSummary() {
        return {
            rating_total: 2419,
            rating_count: [3, 1, 7, 23, 2385],
            rating_star: 4.9791485664639445
        };
    }


    function renderShopeeReviews(items) {
        shopeeList.innerHTML = '';

        // Only show 4-star and 5-star reviews
        const goodItems = items.filter(item => (item.rating_star || 5) >= 4);

        goodItems.forEach(item => {
            const username = item.author_username || 'Khách hàng';
            const portrait = item.author_portrait;
            let avatarHtml = `<i class="ph-fill ph-user"></i>`;
            if (portrait) {
                avatarHtml = `<img src="https://cf.shopee.vn/file/${portrait}_tn" alt="${username}">`;
            }

            const date = new Date((item.ctime || item.submit_time || Date.now() / 1000) * 1000);
            const dateStr = date.toISOString().replace('T', ' ').substring(0, 16);

            const product = (item.product_items && item.product_items[0]) || {};
            const pName = product.name || '';
            const pImg = product.image ? `https://cf.shopee.vn/file/${product.image}` : '';
            const pModel = product.model_name || '';
            const pLink = (product.shopid && product.itemid) ? `https://shopee.vn/product-i.${product.shopid}.${product.itemid}` : '#';

            const reply = item.ItemRatingReply;
            let replyHtml = '';
            if (reply && reply.comment) {
                replyHtml = `
                    <div class="sc-reply-box">
                        <div class="sc-reply-title">Phản Hồi Của Người Bán</div>
                        <div class="sc-reply-text">${reply.comment}</div>
                    </div>`;
            }

            let productCardHtml = '';
            if (pName) {
                productCardHtml = `
                    <div class="sc-product-card" style="display: flex;">
                        <img src="${pImg}" alt="Product">
                        <div class="sc-product-info">
                            <span class="sc-product-name">${pName}</span>
                            <span class="sc-product-variant">Phân loại hàng: ${pModel}</span>
                        </div>
                    </div>`;
            }

            const starsHtml = '<i class="ph-fill ph-star"></i>'.repeat(item.rating_star || 5);

            // Parse review comments
            let commentHtml = '';
            if (item.comment && item.comment.trim()) {
                commentHtml = `<div class="sc-comment">${item.comment}</div>`;
            }

            // Parse review images/medias
            let reviewImages = [];
            if (item.images && item.images.length > 0) {
                reviewImages = item.images;
            } else if (item.medias && item.medias.length > 0) {
                item.medias.forEach(media => {
                    if (media.image && media.image.image_id) {
                        reviewImages.push(media.image.image_id);
                    }
                });
            }

            let imagesHtml = '';
            if (reviewImages && reviewImages.length > 0) {
                imagesHtml = `<div class="sc-comment-images">`;
                reviewImages.forEach(imgId => {
                    const imgUrl = `https://cf.shopee.vn/file/${imgId}`;
                    imagesHtml += `
                        <div class="sc-comment-image-wrap" onclick="event.stopPropagation(); window.open('${imgUrl}', '_blank')">
                            <img src="${imgUrl}_tn" alt="Review photo">
                        </div>`;
                });
                imagesHtml += `</div>`;
            }

            const div = document.createElement('div');
            div.className = 'shopee-comment-item';
            if (pLink && pLink !== '#') {
                div.style.cursor = 'pointer';
                div.onclick = function () { window.open(pLink, '_blank'); };
            }
            div.innerHTML = `
                    <div class="sc-avatar">${avatarHtml}</div>
                    <div class="sc-content">
                        <div class="sc-username">${username}</div>
                        <div class="sc-stars">${starsHtml}</div>
                        <div class="sc-meta">${dateStr} | Phân loại hàng: ${pModel}</div>
                        ${commentHtml}
                        ${imagesHtml}
                        ${productCardHtml}
                        ${replyHtml}
                    </div>
                `;
            shopeeList.appendChild(div);
        });

        if (typeof reveal === 'function') reveal();
    }

    function getMockShopeeData() {
        return [
            {
                author_username: "vanthangmtd", author_portrait: "", rating_star: 5, submit_time: 1777342939,
                comment: "Đế dựng bằng kim loại rất chắc chắn, sơn tĩnh điện đẹp mắt. Mini PC đặt lên vừa vặn, tăng diện tích trống cho bàn làm việc rất nhiều. Giao hàng nhanh và đóng gói cẩn thận.",
                product_items: [{ name: "Đế dựng đa năng cho máy tính Mini PC, điều chỉnh được, nhỏ gọn, tinh tế cho bàn làm việc", image: "vn-11134207-820l4-mir6bh17pj4426", model_name: "⑴ Đế Dựng Nhỏ" }]
            },
            {
                author_username: "vanthangmtd", author_portrait: "", rating_star: 5, submit_time: 1777342933,
                comment: "Máy trạm MS01 quá đỉnh, lắp thêm card mạng 10Gbps chạy rất mát. Shop hỗ trợ kỹ thuật cài đặt Proxmox cực kỳ nhiệt tình. Xứng đáng 5 sao.",
                product_items: [{ name: "Workstation Server Minisforum MS01 SFP+ 10Gbps MS-01 băng thông 10GB Máy trạm / chủ", image: "vn-11134207-820l4-metdd3xjbwg2d8", model_name: "i5 12600H 4.5Ghz 16T,NO RAM - NO SSD" }]
            },
            {
                author_username: "vutuannn", author_portrait: "vn-11134233-7ras8-m4enw6q4rdu792", rating_star: 5, submit_time: 1777273594,
                comment: "RAM Laptop DDR5 Micron bus 5600 chuẩn hãng. Máy nhận ngay đủ bus không cần cấu hình gì thêm. Đóng gói hộp xốp rất an tâm.",
                product_items: [{ name: "RAM Laptop 16GB DDR5 5600 MHz - Samsung, Crucial, SK Hynix, Micron", image: "vn-11134207-81ztc-mn2d789xy1ae0a", model_name: "CRUCIAL,16GB Single" }],
                ItemRatingReply: { comment: "Cảm ơn Quý khách vutuannn đã tin tưởng và ủng hộ NavaStore. Shop hy vọng sản phẩm sẽ đem lại nhiều cảm hứng và hiệu quả cho công việc của Quý khách ạ! ☺️" }
            },
            {
                author_username: "ukshop12345", author_portrait: "c95ab40a615612b04ff68211d7c30fb8", rating_star: 5, submit_time: 1777208515,
                comment: "SSD GM7000 tốc độ bàn thờ, cài win load game siêu nhanh. Có sẵn lá tản nhiệt đi kèm rất tiện lợi. Rất hài lòng với dịch vụ của shop.",
                product_items: [{ name: "SSD Predator GM7000 1TB 2TB 4TB NVMe Gen 4 PCIe Có DRAM Tốc độ Cao", image: "vn-11134207-81ztc-mmtu6wrm7kzkb4", model_name: "New FullBox - 2TB" }],
                ItemRatingReply: { comment: "Cảm ơn Quý khách ukshop12345 đã tin tưởng và ủng hộ NavaStore. Shop hy vọng sản phẩm sẽ đem lại nhiều cảm hứng và hiệu quả cho công việc của Quý khách ạ! ☺️" }
            }
        ];
    }

    // ============================================
    // 15. AUTO-UPGRADE YOUTUBE IFRAMES TO LITE-YOUTUBE
    // ============================================
    function upgradeYoutubeIframes() {
        const iframes = document.querySelectorAll('iframe[src*="youtube.com/embed/"], iframe[src*="youtu.be/"]');
        iframes.forEach(iframe => {
            if (iframe.closest('lite-youtube')) return;

            const src = iframe.src || iframe.getAttribute('data-src');
            if (!src) return;

            const match = src.match(/(?:embed\/|v=)([a-zA-Z0-9_-]{11})/);
            if (match && match[1]) {
                const videoId = match[1];
                const liteYt = document.createElement('lite-youtube');
                liteYt.setAttribute('videoid', videoId);

                liteYt.style.width = '100%';
                liteYt.style.maxWidth = iframe.style.maxWidth || '100%';
                liteYt.style.aspectRatio = '16/9';
                liteYt.style.borderRadius = iframe.style.borderRadius || '8px';
                liteYt.setAttribute('data-bg', `https://img.youtube.com/vi/${videoId}/maxresdefault.jpg`);

                if (iframe.title) {
                    liteYt.setAttribute('title', iframe.title);
                }

                iframe.parentNode.replaceChild(liteYt, iframe);
            }
        });
    }
    upgradeYoutubeIframes();
    setTimeout(upgradeYoutubeIframes, 1500);

    // ============================================
    // 16. LAZY LOAD BACKGROUND IMAGES (INTERSECTION OBSERVER)
    // ============================================
    const lazyBgObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                const bgUrl = el.getAttribute('data-bg');
                if (bgUrl) {
                    el.style.backgroundImage = `url('${bgUrl}')`;
                    el.removeAttribute('data-bg');
                }
                observer.unobserve(el);
            }
        });
    }, { rootMargin: '200px 0px' });

    function observeLazyBg() {
        document.querySelectorAll('[data-bg]').forEach(el => {
            lazyBgObserver.observe(el);
        });
    }

    observeLazyBg();
    // Observe dynamic/upgraded elements
    setTimeout(observeLazyBg, 500);
    setTimeout(observeLazyBg, 2000);

    // ============================================
    // 17. FIX ACCESSIBILITY FOR DYNAMIC IFRAMES (e.g. Google One Tap)
    // ============================================
    function fixDynamicIframeTitles() {
        const iframe = document.getElementById('iframe-google-one-tap');
        if (iframe && !iframe.hasAttribute('title')) {
            iframe.setAttribute('title', 'Google One Tap Login');
        }
    }
    fixDynamicIframeTitles();
    setInterval(fixDynamicIframeTitles, 2000);

    // Dynamic injection of Compare Bar & Modal HTML if missing
    if (!document.getElementById('compare-bar')) {
        const compareBarHtml = `
            <div id="compare-bar" style="position: fixed; bottom: 0; left: 0; right: 0; z-index: 999999; background: var(--bg-white, #ffffff); border-top: 1px solid var(--border-color, #e2e8f0); box-shadow: 0 -5px 25px rgba(0,0,0,0.1); padding: 15px 20px; display: none;">
                <div style="max-width: 1200px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; gap: 20px; flex-wrap: wrap;">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <i class="ph-bold ph-arrows-left-right" style="font-size: 1.5rem; color: var(--primary, #003366);"></i>
                        <h4 style="margin: 0; font-size: 1.1rem; font-weight: 800; color: var(--text-dark, #0f172a);">So sánh sản phẩm</h4>
                    </div>
                    <div id="compare-slots" style="display: flex; gap: 15px; flex: 1; max-width: 700px; min-width: 300px;"></div>
                    <div style="display: flex; gap: 10px;">
                        <button id="compare-clear" onclick="clearCompare()" style="background: transparent; border: 1px solid var(--border-color); border-radius: 8px; padding: 10px 18px; font-weight: 700; color: var(--text-gray); cursor: pointer; font-size: 0.9rem;">Xóa hết</button>
                        <button id="compare-expand" onclick="executeCompare(true)" style="background: transparent; border: 1px solid var(--primary); border-radius: 8px; padding: 10px 18px; font-weight: 700; color: var(--primary); cursor: pointer; font-size: 0.9rem;" disabled>Mở rộng</button>
                        <button id="compare-submit" onclick="executeCompare()" style="background: var(--primary, #003366); border: none; border-radius: 8px; padding: 10px 22px; font-weight: 700; color: white; cursor: pointer; font-size: 0.9rem;" disabled>So sánh ngay</button>
                    </div>
                </div>
            </div>
            <div id="compare-modal" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: 9999999; background: rgba(15,23,42,0.6); backdrop-filter: blur(4px); display: none; align-items: center; justify-content: center; opacity: 0; transition: opacity 0.3s ease;">
                <div id="compare-modal-content" style="background: var(--bg-white, #ffffff); border-radius: 16px; width: 95%; max-width: 1100px; max-height: 90vh; display: flex; flex-direction: column; overflow: hidden; transform: scale(0.95); transition: transform 0.3s ease; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);">
                    <div style="padding: 20px 25px; border-bottom: 1px solid var(--border-color); display: flex; align-items: center; justify-content: space-between; background: var(--bg-gray, #f8fafc);">
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <i class="ph-bold ph-arrows-left-right" style="font-size: 1.4rem; color: var(--primary, #003366);"></i>
                            <h3 style="margin: 0; font-size: 1.25rem; font-weight: 800; color: var(--text-dark);">So sánh chi tiết</h3>
                        </div>
                        <button onclick="closeCompareModal()" style="background: transparent; border: none; font-size: 1.5rem; color: var(--text-gray); cursor: pointer; display: flex; align-items: center; justify-content: center; width: 36px; height: 36px; border-radius: 50%;" onmouseover="this.style.background='rgba(0,0,0,0.05)'" onmouseout="this.style.background='transparent'"><i class="ph-bold ph-x"></i></button>
                    </div>
                    <div style="flex: 1; overflow-y: auto; padding: 25px;" id="compare-modal-body">
                        <div id="compare-loading" style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 50px 0; gap: 15px;">
                            <div style="width: 40px; height: 40px; border: 4px solid var(--border-color); border-top-color: var(--primary); border-radius: 50%; animation: ai-spin 0.8s linear infinite;"></div>
                            <div style="font-weight: 700; color: var(--text-gray);">Đang phân tích cấu hình...</div>
                        </div>
                        <div id="compare-result" style="display: none;"></div>
                    </div>
                </div>
            </div>
        `;
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = compareBarHtml;
        while (tempDiv.firstChild) {
            document.body.appendChild(tempDiv.firstChild);
        }
    }

    fetchShopeeReviews();
}
});

// =========================================================================
// NAVA COMPARE SYSTEM GLOBAL FUNCTIONS
// =========================================================================
window.compareList = [];

window.toggleCompare = function(btn, name, img, price) {
    console.log('--- toggleCompare called ---');
    
    if (window.currentProductData) {
        window.compareList = [{
            name: window.currentProductData.name,
            img: window.currentProductData.img,
            price: window.currentProductData.price,
            url: window.currentProductData.url
        }];
        
        if (btn) {
            btn.style.background = 'var(--primary, #003366)';
            btn.style.color = 'white';
            const icon = btn.querySelector('i');
            if (icon) icon.className = 'ph-bold ph-check';
        }
        
        window.showCompareSelectDropdown(null);
        window.updateCompareBar();
        return;
    }
    
    const idx = window.compareList.findIndex(p => p.name === name);
    if (idx > -1) {
        window.compareList.splice(idx, 1);
        if (btn) {
            btn.style.background = 'var(--bg-white, #ffffff)';
            btn.style.color = 'var(--text-dark, #0f172a)';
            const icon = btn.querySelector('i');
            if (icon) icon.className = 'ph ph-arrows-left-right';
        }
    } else {
        if (window.compareList.length >= 2) {
            alert('Chỉ có thể so sánh tối đa 2 sản phẩm cùng lúc!');
            return;
        }
        window.compareList.push({ name, img, price, url: btn ? btn.getAttribute('data-url') || window.location.pathname : window.location.pathname });
        if (btn) {
            btn.style.background = 'var(--primary, #003366)';
            btn.style.color = 'white';
            const icon = btn.querySelector('i');
            if (icon) icon.className = 'ph-bold ph-check';
        }
    }
    window.updateCompareBar();
};

window.removeCompare = function(name) {
    window.compareList = window.compareList.filter(p => p.name !== name);
    document.querySelectorAll('.compare-btn, .compare-btn-wrap').forEach(btn => {
        const btnName = btn.getAttribute('data-name');
        if (btnName === name || (window.currentProductData && window.currentProductData.name === name)) {
            btn.style.background = 'var(--bg-white, #ffffff)';
            btn.style.color = 'var(--text-dark, #0f172a)';
            const icon = btn.querySelector('i');
            if (icon) icon.className = 'ph ph-arrows-left-right';
        }
    });
    window.updateCompareBar();
};

window.clearCompare = function() {
    window.compareList = [];
    document.querySelectorAll('.compare-btn, .compare-btn-wrap').forEach(btn => {
        btn.style.background = 'var(--bg-white, #ffffff)';
        btn.style.color = 'var(--text-dark, #0f172a)';
        const icon = btn.querySelector('i');
        if (icon) icon.className = 'ph ph-arrows-left-right';
    });
    window.updateCompareBar();
};

window.hideCompareBar = function() {
    const bar = document.getElementById('compare-bar');
    if (bar) bar.style.setProperty('display', 'none', 'important');
};

window.updateCompareBar = function() {
    const bar = document.getElementById('compare-bar');
    const slots = document.getElementById('compare-slots');
    const submitBtn = document.getElementById('compare-submit');
    const expandBtn = document.getElementById('compare-expand');
    if (!bar || !slots) return;
    
    if (window.compareList.length > 0) {
        bar.style.setProperty('display', 'block', 'important');
    } else {
        bar.style.setProperty('display', 'none', 'important');
    }
    
    if (window.compareList.length === 2) {
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.style.cursor = 'pointer';
            submitBtn.style.opacity = '1';
        }
        if (expandBtn) {
            expandBtn.disabled = false;
            expandBtn.style.cursor = 'pointer';
            expandBtn.style.opacity = '1';
        }
    } else {
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.style.cursor = 'not-allowed';
            submitBtn.style.opacity = '0.5';
        }
        if (expandBtn) {
            expandBtn.disabled = true;
            expandBtn.style.cursor = 'not-allowed';
            expandBtn.style.opacity = '0.5';
        }
    }
    
    let html = '';
    for (let i = 0; i < 2; i++) {
        if (i < window.compareList.length) {
            const p = window.compareList[i];
            html += `
                <div class="compare-slot-item" style="display: flex; align-items: center; gap: 15px; background: var(--bg-gray, #f8fafc); padding: 10px 15px; border-radius: 12px; border: 1px solid var(--border-color, #e2e8f0); flex: 1; position: relative; font-family: inherit;">
                    <img src="${p.img}" style="width: 55px; height: 55px; object-fit: contain; background: var(--bg-white, #ffffff); border-radius: 6px; padding: 3px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                    <div style="flex: 1; min-width: 0;">
                        <div style="font-size: 0.95rem; font-weight: 700; color: var(--text-dark, #0f172a); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-bottom: 4px;">${p.name}</div>
                        <div style="font-size: 1.05rem; font-weight: 800; color: var(--primary, #003366);">${p.price}</div>
                    </div>
                    <button onclick="removeCompare('${p.name.replace(/'/g, "\\'")}')" style="background: none; border: none; color: var(--text-gray, #64748b); cursor: pointer; padding: 5px; display: flex; font-size: 1.2rem; transition: color 0.2s;" onmouseover="this.style.color='#ef4444'" onmouseout="this.style.color='var(--text-gray, #64748b)'"><i class="ph-bold ph-x"></i></button>
                </div>
            `;
        } else {
            html += `
                <div class="compare-slot-item" style="display: flex; align-items: center; justify-content: center; gap: 10px; background: transparent; padding: 10px 15px; border-radius: 12px; border: 1px dashed var(--border-color, #e2e8f0); flex: 1; color: var(--text-gray, #64748b); font-size: 0.95rem; font-family: inherit;">
                    <div style="width: 45px; height: 45px; border-radius: 50%; background: var(--bg-gray, #f8fafc); display: flex; align-items: center; justify-content: center;"><i class="ph ph-plus" style="font-size: 1.2rem;"></i></div>
                    Thêm sản phẩm
                </div>
            `;
        }
    }
    slots.innerHTML = html;
};

window.showCompareSelectDropdown = function(event) {
    if (event) event.stopPropagation();
    const modal = document.getElementById('compare-select-modal');
    const modalContent = document.getElementById('compare-select-dropdown');
    const searchInput = document.getElementById('compare-search-input');
    if (searchInput) searchInput.value = '';
    
    if (modal && modalContent) {
        modal.style.setProperty('display', 'flex', 'important');
        void modal.offsetWidth;
        modal.style.opacity = '1';
        modalContent.style.transform = 'scale(1)';
    }
    
    window.filterCompareProducts();
    
    setTimeout(() => {
        if (searchInput) searchInput.focus();
    }, 100);
};

window.hideCompareSelectDropdown = function() {
    const modal = document.getElementById('compare-select-modal');
    const modalContent = document.getElementById('compare-select-dropdown');
    if (modal && modalContent) {
        modal.style.opacity = '0';
        modalContent.style.transform = 'scale(0.95)';
        setTimeout(() => {
            modal.style.setProperty('display', 'none', 'important');
        }, 250);
    }
};

window.filterCompareProducts = function() {
    const query = document.getElementById('compare-search-input')?.value.toLowerCase().trim() || '';
    const listContainer = document.getElementById('compare-select-list');
    if (!listContainer) return;
    
    const products = window.currentCollectionProducts || [];
    let available = products.filter(p => !window.compareList.some(item => item.name === p.name));
    
    if (query) {
        available = available.filter(p => p.name.toLowerCase().includes(query));
    }
    
    let html = '';
    available.forEach(p => {
        const escapedName = p.name.replace(/'/g, "\\'").replace(/"/g, '&quot;');
        html += `
            <div onclick="selectProductForCompare('${escapedName}', '${p.img}', '${p.price}', '${p.url}')" style="display: flex; align-items: center; gap: 10px; padding: 8px; border: 1px solid var(--border-color, #e2e8f0); border-radius: 8px; cursor: pointer; transition: all 0.2s;" onmouseover="this.style.borderColor='var(--primary)'; this.style.background='var(--bg-gray, #f8fafc)';" onmouseout="this.style.borderColor='var(--border-color, #e2e8f0)'; this.style.background='transparent';">
                <img src="${p.img}" style="width: 40px; height: 40px; object-fit: contain; background: white; border-radius: 4px; padding: 2px;">
                <div style="flex: 1; min-width: 0; text-align: left;">
                    <div style="font-size: 0.85rem; font-weight: 700; color: var(--text-dark, #0f172a); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${p.name}</div>
                    <div style="font-size: 0.9rem; font-weight: 800; color: var(--primary, #003366);">${p.price}</div>
                </div>
            </div>
        `;
    });
    
    if (available.length === 0) {
        html = '<div style="font-size: 0.85rem; color: var(--text-gray, #64748b); text-align: center; padding: 15px;">Không tìm thấy sản phẩm phù hợp</div>';
    }
    
    listContainer.innerHTML = html;
};

window.selectProductForCompare = function(name, img, price, url) {
    if (window.compareList.length >= 2) return;
    window.compareList.push({ name, img, price, url });
    window.updateCompareBar();
    window.hideCompareSelectDropdown();
    
    if (window.compareList.length === 2) {
        window.executeCompare();
    }
};

window.executeCompare = function(isFullScreen = false) {
    const modal = document.getElementById('compare-modal');
    const modalContent = document.getElementById('compare-modal-content');
    const loading = document.getElementById('compare-loading');
    const result = document.getElementById('compare-result');
    if (!modal || !modalContent) return;
    
    modal.style.setProperty('display', 'flex', 'important');
    
    if (isFullScreen) {
        modalContent.style.width = '100%';
        modalContent.style.maxWidth = '100%';
        modalContent.style.height = '100vh';
        modalContent.style.maxHeight = '100vh';
        modalContent.style.borderRadius = '0';
        modalContent.style.transform = 'translateY(100vh)';
        
        void modal.offsetWidth;
        
        modalContent.style.transition = 'transform 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
        modal.style.opacity = '1';
        modalContent.style.transform = 'translateY(0)';
    } else {
        modalContent.style.width = '95%';
        modalContent.style.maxWidth = '1100px';
        modalContent.style.height = 'auto';
        modalContent.style.maxHeight = '90vh';
        modalContent.style.borderRadius = '16px';
        modalContent.style.transform = 'scale(0.95)';
        
        void modal.offsetWidth;
        
        modalContent.style.transition = 'transform 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
        modal.style.opacity = '1';
        modalContent.style.transform = 'scale(1)';
    }
    
    if (loading) loading.style.display = 'flex';
    if (result) result.style.display = 'none';
    
    const p1 = window.compareList[0];
    const p2 = window.compareList[1];
    if (!p1 || !p2) {
        if (loading) loading.style.display = 'none';
        if (result) {
            result.innerHTML = '<div style="padding: 20px; text-align: center; color: var(--text-gray);">Cần tối thiểu 2 sản phẩm để đối chiếu.</div>';
            result.style.display = 'block';
        }
        return;
    }
    
    Promise.all([
        fetch(p1.url.includes('?') ? p1.url + '&view=data' : p1.url + '?view=data').then(res => res.json()).catch(err => {
            console.error('Fetch p1 error:', err);
            return { infor: { name: p1.name, thumbnail: p1.img, price: p1.price, url: p1.url }, spec: {} };
        }),
        fetch(p2.url.includes('?') ? p2.url + '&view=data' : p2.url + '?view=data').then(res => res.json()).catch(err => {
            console.error('Fetch p2 error:', err);
            return { infor: { name: p2.name, thumbnail: p2.img, price: p2.price, url: p2.url }, spec: {} };
        })
    ]).then(([data1, data2]) => {
        if (loading) loading.style.display = 'none';
        
        let tableHtml = `
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 30px;">
                <div style="text-align: center; padding: 20px; border: 1px solid var(--border-color, #e2e8f0); border-radius: 12px; background: var(--bg-gray, #f8fafc);">
                    <img src="${data1.infor.thumbnail || p1.img}" style="width: 120px; height: 120px; object-fit: contain; margin-bottom: 15px; background: var(--bg-white, #ffffff); border-radius: 8px; padding: 10px; border: 1px solid var(--border-color, #e2e8f0);">
                    <h4 style="margin: 0 0 10px 0; font-size: 1rem; color: var(--text-dark, #0f172a); font-weight: 800; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; height: 2.8em; line-height: 1.4;">${data1.infor.name || p1.name}</h4>
                    <div style="color: var(--primary, #003366); font-weight: 800; font-size: 1.2rem;">${data1.infor.price || p1.price}</div>
                </div>
                <div style="text-align: center; padding: 20px; border: 1px solid var(--border-color, #e2e8f0); border-radius: 12px; background: var(--bg-gray, #f8fafc);">
                    <img src="${data2.infor.thumbnail || p2.img}" style="width: 120px; height: 120px; object-fit: contain; margin-bottom: 15px; background: var(--bg-white, #ffffff); border-radius: 8px; padding: 10px; border: 1px solid var(--border-color, #e2e8f0);">
                    <h4 style="margin: 0 0 10px 0; font-size: 1rem; color: var(--text-dark, #0f172a); font-weight: 800; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; height: 2.8em; line-height: 1.4;">${data2.infor.name || p2.name}</h4>
                    <div style="color: var(--primary, #003366); font-weight: 800; font-size: 1.2rem;">${data2.infor.price || p2.price}</div>
                </div>
            </div>
            
            <div style="background: var(--bg-white, #ffffff); border: 1px solid var(--border-color, #e2e8f0); border-radius: 12px; overflow: hidden; font-family: inherit;">
        `;
        
        const specsMap1 = {};
        const specsMap2 = {};
        
        if (data1.spec) {
            Object.values(data1.spec).forEach(group => {
                if (group.content) {
                    group.content.forEach(item => {
                        if (item.name && item.infor) {
                            specsMap1[item.name.trim()] = item.infor;
                        }
                    });
                }
            });
        }
        
        if (data2.spec) {
            Object.values(data2.spec).forEach(group => {
                if (group.content) {
                    group.content.forEach(item => {
                        if (item.name && item.infor) {
                            specsMap2[item.name.trim()] = item.infor;
                        }
                    });
                }
            });
        }
        
        const allKeys = Array.from(new Set([
            ...Object.keys(specsMap1),
            ...Object.keys(specsMap2)
        ]));
        
        if (allKeys.length === 0) {
            tableHtml += `
                <div style="padding: 30px; text-align: center; color: var(--text-gray, #64748b);">
                    Chưa có thông số chi tiết cấu hình để so sánh.
                </div>
            `;
        } else {
            allKeys.forEach((key, index) => {
                const val1 = specsMap1[key] || '-';
                const val2 = specsMap2[key] || '-';
                const bg = index % 2 === 0 ? 'var(--bg-gray, #f8fafc)' : 'var(--bg-white, #ffffff)';
                
                tableHtml += `
                    <div style="display: grid; grid-template-columns: 140px 1fr 1fr; border-bottom: 1px solid var(--border-color, #e2e8f0); background: ${bg}; font-size: 0.9rem;">
                        <div style="padding: 12px 15px; font-weight: 800; color: var(--text-gray, #64748b); border-right: 1px solid var(--border-color, #e2e8f0); display: flex; align-items: center;">${key}</div>
                        <div style="padding: 12px 15px; border-right: 1px solid var(--border-color, #e2e8f0); font-weight: 600; color: var(--text-dark, #0f172a); line-height: 1.4;">${val1}</div>
                        <div style="padding: 12px 15px; font-weight: 600; color: var(--text-dark, #0f172a); line-height: 1.4;">${val2}</div>
                    </div>
                `;
            });
        }
        
        tableHtml += `
            </div>
            
            <div style="margin-top: 30px; padding: 20px; background: linear-gradient(135deg, rgba(0,51,102,0.05), rgba(15,23,42,0.02)); border-radius: 12px; border: 1px solid rgba(0,51,102,0.2); display: flex; gap: 15px;">
                <i class="ph-fill ph-storefront" style="color: var(--primary, #003366); font-size: 2rem;"></i>
                <div>
                    <h4 style="margin: 0 0 5px 0; color: var(--text-dark, #0f172a); font-weight: 800;">Đề xuất từ Nava Store</h4>
                    <p style="margin: 0; color: var(--text-gray, #64748b); line-height: 1.5; font-size: 0.9rem;">Nếu bạn ưu tiên hiệu năng mạnh mẽ để chơi game hoặc làm đồ họa nặng, hãy chọn sản phẩm có cấu hình cao hơn. Cả hai sản phẩm đều được phân phối chính hãng và hỗ trợ trả góp 0% tại Nava Store.</p>
                </div>
            </div>
        `;
        
        if (result) {
            result.innerHTML = tableHtml;
            result.style.display = 'block';
        }
    }).catch(err => {
        console.error('Specs fetch error:', err);
        if (loading) loading.style.display = 'none';
        if (result) {
            result.innerHTML = '<div style="padding: 20px; text-align: center; color: var(--text-gray);">Có lỗi xảy ra khi tải dữ liệu so sánh.</div>';
            result.style.display = 'block';
        }
    });
};

window.closeCompareModal = function() {
    const modal = document.getElementById('compare-modal');
    const modalContent = document.getElementById('compare-modal-content');
    if (!modal || !modalContent) return;
    
    modal.style.opacity = '0';
    if (modalContent.style.width === '100%') {
        modalContent.style.transform = 'translateY(100vh)';
    } else {
        modalContent.style.transform = 'scale(0.95)';
    }
    setTimeout(() => {
        modal.style.setProperty('display', 'none', 'important');
    }, 300);
};




