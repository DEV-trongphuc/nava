
            window.addEventListener('load', function() {
                const preloader = document.getElementById('nava-preloader');
                if (preloader) {
                    preloader.classList.add('nava-preloader-hidden');
                    setTimeout(() => { preloader.style.display = 'none'; }, 600);
                }
            });
            setTimeout(() => {
                const preloader = document.getElementById('nava-preloader');
                if (preloader && !preloader.classList.contains('nava-preloader-hidden')) {
                    preloader.classList.add('nava-preloader-hidden');
                    setTimeout(() => { preloader.style.display = 'none'; }, 600);
                }
            }, 5000);
        