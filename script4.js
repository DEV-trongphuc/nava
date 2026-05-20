
        document.addEventListener('DOMContentLoaded', function() {
            // Cycle FAB images
            setInterval(() => {
                const imgs = document.querySelectorAll('.fab-cycle-img');
                if (imgs.length > 0) {
                    let activeIdx = -1;
                    imgs.forEach((img, idx) => {
                        if (img.classList.contains('active')) activeIdx = idx;
                        img.classList.remove('active');
                    });
                    if (activeIdx !== -1) {
                        const nextIdx = (activeIdx + 1) % imgs.length;
                        imgs[nextIdx].classList.add('active');
                    } else {
                        imgs[0].classList.add('active');
                    }
                }
            }, 2500);

            // Toggle FAB menu
            const fabMainBtn = document.getElementById('fabMainBtn');
            if(fabMainBtn) {
                fabMainBtn.addEventListener('click', function () {
                    const fabMenu = document.getElementById('fabMenu');
                    if(fabMenu) fabMenu.classList.toggle('active');
                });
            }

            document.addEventListener('click', function (e) {
                if (!e.target.closest('.floating-social-wrapper')) {
                    const fabMenu = document.getElementById('fabMenu');
                    if(fabMenu) fabMenu.classList.remove('active');
                }
            });
        });
        