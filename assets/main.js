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
        if (!isScrolling) {
            window.requestAnimationFrame(() => {
                const currentScroll = window.pageYOffset;
                
                // Header Sticky Logic
                if (currentScroll > 150) {
                    if (currentScroll > lastScroll) {
                        header.classList.add('scrolled');
                    } else {
                        header.classList.remove('scrolled');
                    }
                    if (progressContainer) progressContainer.classList.add('active');
                } else {
                    header.classList.remove('scrolled');
                    if (progressContainer) progressContainer.classList.remove('active');
                }
                lastScroll = currentScroll;

                // Back To Top Button Logic
                if (backToTopBtn) {
                    if (currentScroll > 500) {
                        backToTopBtn.classList.add('show');
                    } else {
                        backToTopBtn.classList.remove('show');
                    }
                }

                // Progress Bar Logic
                if (progressBar) {
                    const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
                    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
                    const scrolled = (height > 0) ? (winScroll / height) * 100 : 0;
                    progressBar.style.width = scrolled + "%";
                }

                isScrolling = false;
            });
            isScrolling = true;
        }
    });

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
});
