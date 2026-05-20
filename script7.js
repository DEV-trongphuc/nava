
        document.addEventListener('DOMContentLoaded', function() {
            // Hijack login and register links to point to local demo HTMLs
            const authLinks = document.querySelectorAll('a[href^="/account/login"], a[href^="/account/register"]');
            authLinks.forEach(link => {
                link.addEventListener('click', function(e) {
                    e.preventDefault();
                    if (this.getAttribute('href').includes('login')) {
                        window.location.href = 'demo_login.html';
                    } else if (this.getAttribute('href').includes('register')) {
                        window.location.href = 'demo_register.html';
                    }
                });
            });
        });
    