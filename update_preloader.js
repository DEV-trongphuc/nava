const fs = require('fs');
let script = fs.readFileSync('update_index_bwt.js', 'utf8');

const oldPreloaderRegex = /<!-- PRELOADER -->[\s\S]*?<\/script>/;
const newPreloader = `<!-- PRELOADER -->
        <style>
            #nava-preloader {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100vh;
                background: #0a0f1c;
                z-index: 999999;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                transition: opacity 0.6s cubic-bezier(0.8, 0, 0.2, 1), visibility 0.6s, transform 0.6s ease;
            }
            .preloader-brand {
                position: relative;
                display: flex;
                justify-content: center;
                align-items: center;
                margin-bottom: 30px;
                width: 100px;
                height: 100px;
            }
            .preloader-ring {
                position: absolute;
                width: 100%;
                height: 100%;
                border-radius: 50%;
                border: 2px solid transparent;
                border-top-color: #3b82f6;
                border-right-color: rgba(59, 130, 246, 0.3);
                animation: spin-ring 1.5s linear infinite;
            }
            .preloader-ring::before {
                content: '';
                position: absolute;
                top: -6px; left: -6px; right: -6px; bottom: -6px;
                border-radius: 50%;
                border: 2px solid transparent;
                border-bottom-color: #10b981;
                animation: spin-ring 2s linear infinite reverse;
            }
            .preloader-logo {
                width: 45px;
                height: auto;
                animation: pulse-logo 2s ease-in-out infinite;
                z-index: 2;
                border-radius: 8px;
            }
            .preloader-text {
                font-family: 'Inter', sans-serif;
                font-size: 13px;
                font-weight: 600;
                letter-spacing: 4px;
                color: #64748b;
                text-transform: uppercase;
                position: relative;
                overflow: hidden;
            }
            .preloader-text::after {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.8), transparent);
                animation: shimmer-text 2s infinite;
            }
            @keyframes spin-ring {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            @keyframes pulse-logo {
                0%, 100% { transform: scale(1); opacity: 0.8; filter: drop-shadow(0 0 5px rgba(59,130,246,0.5)); }
                50% { transform: scale(1.1); opacity: 1; filter: drop-shadow(0 0 15px rgba(59,130,246,0.8)); }
            }
            @keyframes shimmer-text {
                100% { left: 100%; }
            }
            .nava-preloader-hidden {
                opacity: 0;
                visibility: hidden;
                transform: scale(1.05);
            }
        </style>
        <div id="nava-preloader">
            <div class="preloader-brand">
                <div class="preloader-ring"></div>
                <img src="https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/favicon.png?1775454528082" alt="Nava Store" class="preloader-logo">
            </div>
            <div class="preloader-text">Khởi động hệ thống...</div>
        </div>
        <script>
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
        </script>`;

script = script.replace(oldPreloaderRegex, newPreloader);
fs.writeFileSync('update_index_bwt.js', script);
console.log('Updated update_index_bwt.js with premium preloader');
