document.addEventListener('DOMContentLoaded', () => {
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
        root: null, threshold: 0.15, rootMargin: "0px 0px -50px 0px"
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
    const progressBar = document.getElementById("myBar");
    const progressContainer = document.getElementById("progressContainer");
    const backToTopBtn = document.getElementById("backToTop");
    let lastScroll = 0;
    let isScrolling = false;

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset || document.documentElement.scrollTop;

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
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
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
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
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
            mobileNavContainer.appendChild(clone);
        });
    }

    const toggleSidebar = (state) => {
        if (state) {
            sidebarDrawer.classList.add('active');
            sidebarOverlay.classList.add('active');
            document.body.style.overflow = 'hidden';
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
    const heroSlides    = document.querySelectorAll('.hero-slide');
    const heroDots      = document.querySelectorAll('.h-dot');
    const floatLabel1   = document.getElementById('floatLabel1');
    const floatSub1     = document.getElementById('floatSub1');
    const floatIcon1    = document.getElementById('floatIcon1');
    const floatLabel2   = document.getElementById('floatLabel2');
    const floatSub2     = document.getElementById('floatSub2');
    const floatIcon2    = document.getElementById('floatIcon2');
    const floatItem1    = document.getElementById('floatItem1');
    const floatItem2    = document.getElementById('floatItem2');

    // Data per slide: [icon-class, label, sub, icon2-class, label2, sub2]
    const heroSlideData = [
        { i1: 'ph-fill ph-cpu',          l1: 'Core Ultra 9',   s1: 'Xử lý đỉnh cao',
          i2: 'ph-fill ph-lightning',    l2: 'AI NPU',          s2: 'Tích hợp sẵn' },
        { i1: 'ph-fill ph-game-controller', l1: 'ROG Gaming',   s1: 'Hiệu năng đỉnh',
          i2: 'ph-fill ph-plugs-connected', l2: 'OCuLink 40G',  s2: 'eGPU tốc độ cao' },
        { i1: 'ph-fill ph-graphics-card',   l1: 'RTX 4090',     s1: 'Sức mạnh đồ họa',
          i2: 'ph-fill ph-usb',             l2: 'USB4 / TB4',   s2: 'Kết nối siêu tốc' },
        { i1: 'ph-fill ph-memory',          l1: 'LPDDR5X 6400', s1: 'Băng thông đỉnh',
          i2: 'ph-fill ph-hard-drive',      l2: 'NVMe PCIe 4.0',s2: '7,400 MB/s' },
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
                floatIcon1.className = d.i1;
                floatLabel1.textContent = d.l1;
                floatSub1.textContent   = d.s1;
                floatIcon2.className = d.i2;
                floatLabel2.textContent = d.l2;
                floatSub2.textContent   = d.s2;
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
                const duration = 1800;
                const step = Math.ceil(target / (duration / 16));
                let current = 0;
                const timer = setInterval(() => {
                    current = Math.min(current + step, target);
                    el.textContent = current.toLocaleString('vi-VN');
                    if (current >= target) clearInterval(timer);
                }, 16);
                counterObserver.unobserve(el);
            }
        });
    }, { threshold: 0.5 });

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
    }, { threshold: 0.3 });

    benchFills.forEach(el => benchObserver.observe(el));

    // ============================================
    // 10. TERMINAL TYPING ANIMATION (on scroll in)
    // ============================================
    const terminalLines = [
        { cls: '',          html: '<span class="t-prompt">$</span> <span class="t-cmd">run benchmark --device minisforum-um890</span>' },
        { cls: 't-out',     html: '[INFO] CPU: AMD Ryzen 9 8945HX @ 5.2GHz' },
        { cls: 't-out',     html: '[INFO] RAM: 64GB LPDDR5X-6400' },
        { cls: 't-out',     html: '[INFO] GPU: Radeon 890M iGPU' },
        { cls: 't-success', html: '[PASS] Cinebench R24 Multi: <b>24,819 pts</b>' },
        { cls: 't-success', html: '[PASS] CrystalDisk Read: <b>7,412 MB/s</b>' },
        { cls: 't-success', html: '[PASS] LLM Inference: <b>42 tok/s</b>' },
        { cls: 't-warn',    html: '[TEMP] Peak Temp: 74°C ✓ Under threshold' },
        { cls: 't-success', html: '[PASS] Total Power Draw: <b>28W</b> ✅' },
        { cls: 't-blink',   html: '<span class="t-cursor">█</span> Benchmark complete — Score: <span class="t-highlight">ELITE</span>' },
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
        }, { threshold: 0.3 });
        termObserver.observe(terminalEl);
    }

});
