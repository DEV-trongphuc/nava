const fs = require('fs');
let script = fs.readFileSync('update_index_bwt.js', 'utf8');
const preloaderInject = `
// Inject Preloader
bodyContent = bodyContent.replace(
    /<!-- MASTER SAPO ESCAPE WRAPPER -->\\s*<div id="nava-master-wrapper">/i,
    \`<!-- MASTER SAPO ESCAPE WRAPPER -->
    <div id="nava-master-wrapper">
        <!-- PRELOADER -->
        <style>
            #nava-preloader {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100vh;
                background: #ffffff;
                z-index: 999999;
                display: flex;
                justify-content: center;
                align-items: center;
                transition: opacity 0.5s ease, visibility 0.5s ease;
            }
            [data-theme="dark"] #nava-preloader {
                background: #0f172a;
            }
            .nava-spinner {
                width: 40px;
                height: 40px;
                border: 3px solid rgba(0, 51, 102, 0.2);
                border-top-color: #003366;
                border-radius: 50%;
                animation: nava-spin 0.8s linear infinite;
            }
            [data-theme="dark"] .nava-spinner {
                border-color: rgba(51, 133, 255, 0.2);
                border-top-color: #3385ff;
            }
            @keyframes nava-spin {
                to { transform: rotate(360deg); }
            }
            .nava-preloader-hidden {
                opacity: 0;
                visibility: hidden;
            }
        </style>
        <div id="nava-preloader">
            <div class="nava-spinner"></div>
        </div>
        <script>
            window.addEventListener('load', function() {
                const preloader = document.getElementById('nava-preloader');
                if (preloader) {
                    preloader.classList.add('nava-preloader-hidden');
                    setTimeout(() => { preloader.style.display = 'none'; }, 500);
                }
            });
            
            // Fallback: Nếu mạng quá chậm
            setTimeout(() => {
                const preloader = document.getElementById('nava-preloader');
                if (preloader && !preloader.classList.contains('nava-preloader-hidden')) {
                    preloader.classList.add('nava-preloader-hidden');
                    setTimeout(() => { preloader.style.display = 'none'; }, 500);
                }
            }, 5000);
        </script>\`
);

`;
script = script.replace('fs.writeFileSync', preloaderInject + 'fs.writeFileSync');
fs.writeFileSync('update_index_bwt.js', script);
console.log('Updated update_index_bwt.js');
