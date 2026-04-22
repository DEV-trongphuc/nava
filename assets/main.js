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
        root: null,
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

    // 3. STICKY HEADER LOGIC (SMART SHOW/HIDE)
    const header = document.querySelector('.header');
    let lastScroll = 0;

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 150) {
            if (currentScroll > lastScroll) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        } else {
            header.classList.remove('scrolled');
        }
        
        lastScroll = currentScroll;
    });
});
