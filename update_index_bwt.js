const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

// Extract the body content
const bodyMatch = html.match(/<body>([\s\S]*?)<\/body>/i);
if (!bodyMatch) {
    console.error("Could not find <body> tag in index.html");
    process.exit(1);
}
let bodyContent = bodyMatch[1];

// Replace News Section
const newsRegex = /<!-- News Section -->[\s\S]*?<\/section>/i;
const newsLiquid = `
<!-- News Section -->
{% assign blog_news = blogs["tin-tuc"] %}
<section id="news" class="news-section">
    <div class="container">
        <div class="section-header">
            <h2 class="section-title">{{ blog_news.name | default: 'TIN TỨC CÔNG NGHỆ' }}</h2>
            <a href="/blogs/tin-tuc" class="view-all-link">Xem tất cả <i class="ph ph-arrow-right"></i></a>
        </div>
        {% if blog_news.articles_count > 0 %}
        <div class="news-flex">
            <!-- Featured Article -->
            {% assign featured_article = blog_news.articles.first %}
            <div class="news-featured reveal">
                <div class="featured-img">
                    <img src="{{ featured_article.image.src }}" alt="{{ featured_article.title }}" loading="lazy" decoding="async">
                    <div class="news-date">{{ featured_article.published_on | date: "%d/%m" }}</div>
                </div>
                <div class="featured-content">
                    <h3><a href="{{ featured_article.url }}" style="color: inherit; text-decoration: none;">{{ featured_article.title }}</a></h3>
                    <p>{{ featured_article.content | strip_html | truncatewords: 25 }}</p>
                    <a href="{{ featured_article.url }}" class="read-more">Đọc tiếp <i class="ph ph-caret-double-right"></i></a>
                </div>
            </div>
            <!-- News List -->
            <div class="news-list">
                {% for article in blog_news.articles offset: 1 limit: 5 %}
                <div class="news-item reveal delay-{{ forloop.index }}">
                    <div class="item-img">
                        <img src="{{ article.image.src }}" alt="{{ article.title }}" loading="lazy" decoding="async">
                    </div>
                    <div class="item-content">
                        <h4><a href="{{ article.url }}" style="color: inherit; text-decoration: none;">{{ article.title }}</a></h4>
                        <span class="item-date">{{ article.published_on | date: "%d/%m/%Y" }}</span>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
        {% else %}
        <div class="text-center" style="padding: 40px; color: var(--text-gray);">
            <p>Chưa có bài viết nào.</p>
        </div>
        {% endif %}
    </div>
</section>
`;
bodyContent = bodyContent.replace(newsRegex, newsLiquid);

// Replace Video Section
const videoRegex = /<!-- Video Review Section -->[\s\S]*?<\/section>/i;
const videoLiquid = `
<!-- Video Review Section -->
<style>
.video-card-link {
    display: block;
    color: inherit;
    text-decoration: none;
    height: 100%;
}
.video-card-link:hover {
    color: inherit;
    text-decoration: none;
}
.video-card-link .play-btn i {
    margin-left: 2px !important; /* Fix off-center play button */
}
</style>
<section id="video" class="video-section">
    <div class="container">
        <div class="section-header">
            <h2 class="section-title">VIDEO REVIEW TRỰC QUAN</h2>
            <a href="https://www.youtube.com/@NAVAStore-MiniPC-eGPU" target="_blank" class="view-all-link">Xem tất cả <i class="ph ph-youtube-logo"></i></a>
        </div>
        <div class="video-grid">
            <!-- Video 1 -->
            <div class="video-card reveal">
                <a href="https://www.youtube.com/watch?v=Syk0rwciis4" target="_blank" class="video-card-link">
                    <div class="video-thumb">
                        <img src="https://img.youtube.com/vi/Syk0rwciis4/maxresdefault.jpg" alt="Lại một em Mini PC đến từ nhà GMKtec | Review GMKtec M7 cùng Nava" loading="lazy" decoding="async">
                        <div class="play-btn"><i class="ph-fill ph-play"></i></div>
                    </div>
                    <div class="video-info">
                        <h3>Lại một em Mini PC đến từ nhà GMKtec | Review GMKtec M7 cùng Nava</h3>
                    </div>
                </a>
            </div>
            
            <!-- Video 2 -->
            <div class="video-card reveal delay-1">
                <a href="https://www.youtube.com/watch?v=X_BmTM2T9gY" target="_blank" class="video-card-link">
                    <div class="video-thumb">
                        <img src="https://img.youtube.com/vi/X_BmTM2T9gY/maxresdefault.jpg" alt="Lý do nào bạn nên sở hữu Mini PC?| Nava Store" loading="lazy" decoding="async">
                        <div class="play-btn"><i class="ph-fill ph-play"></i></div>
                    </div>
                    <div class="video-info">
                        <h3>Lý do nào bạn nên sở hữu Mini PC?| Nava Store</h3>
                    </div>
                </a>
            </div>
            
            <!-- Video 3 -->
            <div class="video-card reveal delay-2">
                <a href="https://www.youtube.com/watch?v=RPZbRVCAImo" target="_blank" class="video-card-link">
                    <div class="video-thumb">
                        <img src="https://img.youtube.com/vi/RPZbRVCAImo/maxresdefault.jpg" alt="Mini PC mang tính đột phá của thương hiệu Beelink ? | Review Beelink Ser8" loading="lazy" decoding="async">
                        <div class="play-btn"><i class="ph-fill ph-play"></i></div>
                    </div>
                    <div class="video-info">
                        <h3>Mini PC mang tính đột phá của thương hiệu Beelink ? | Review Beelink Ser8</h3>
                    </div>
                </a>
            </div>
        </div>
    </div>
</section>
`;
bodyContent = bodyContent.replace(videoRegex, videoLiquid);

// Set main.js to Vercel absolute URL
bodyContent = bodyContent.replace(/src="assets\/main\.js\?[^"]+"/g, 'src="https://nava-one.vercel.app/assets/main.js?v=20260426_v1"');

// Ensure any local assets (like assets/icon) in index.html are pointing to the vercel demo
// (In index.html they were already pointing to https://nava-one.vercel.app but just to be safe: )
bodyContent = bodyContent.replace(/src="assets\/([^"]+)"/g, 'src="https://nava-one.vercel.app/assets/$1"');


// Inject Liquid for Cart Badge
bodyContent = bodyContent.replace(
    /<span class="cart-count-badge" id="cart-count-badge" style="display: none;">0<\/span>/g,
    '<span class="cart-count-badge" id="cart-count-badge" {% if cart.item_count > 0 %}style="display: flex;"{% else %}style="display: none;"{% endif %}>{{ cart.item_count }}</span>'
);


// Inject Preloader
bodyContent = bodyContent.replace(
    /<!-- MASTER SAPO ESCAPE WRAPPER -->\s*<div id="nava-master-wrapper">/i,
    `<!-- MASTER SAPO ESCAPE WRAPPER -->
    <div id="nava-master-wrapper">
        <!-- SEO H1 -->
        <h1 style="position:absolute; width:1px; height:1px; padding:0; margin:-1px; overflow:hidden; clip:rect(0,0,0,0); border:0;">NAVA STORE - Mini PC & eGPU</h1>
        <!-- PRELOADER -->
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
            <div class="preloader-text">NAVA STORE</div>
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
        </script>`
);


// Inject Shopee Mobile Slider CSS
bodyContent = bodyContent.replace(
    /<!-- Shopee Reviews Section -->/i,
    `<!-- Mobile CSS Fixes (Cart + Shopee) -->
<style>
@media (max-width: 768px) {
    /* Fix hidden cart icon on mobile */
    .top-actions .cart-btn .cart-icon-wrapper {
        display: block !important;
    }
    .top-actions .cart-btn {
        font-size: 0 !important; /* Hide 'Giỏ hàng' text */
        padding: 6px 10px;
    }
    .top-actions .cart-btn i {
        font-size: 1.6rem !important;
    }
    .cart-count-badge {
        font-size: 10px !important;
    }
    .floating-social-wrapper {
        bottom: -235px !important;
    }
}

    /* Shopee Desktop Grid */
    @media (min-width: 769px) {
        .shopee-comments-list {
            display: grid !important;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        .shopee-comment-item {
            border-bottom: none !important;
            border: 1px solid var(--border-color, #e2e8f0);
            border-radius: 12px;
            padding: 20px;
            background: var(--bg-card, #ffffff);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            height: 100%;
        }
    }
    
    /* Policy 3D Hover & Slower Track */
    .policy-card {
        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease !important;
        transform-style: preserve-3d;
        perspective: 1000px;
    }
    .policy-card:hover {
        transform: translateY(-8px) rotateX(4deg) rotateY(-4deg) scale(1.03) !important;
        box-shadow: -5px 15px 30px rgba(0, 51, 102, 0.15) !important;
        z-index: 10;
    }
    .policy-track {
        animation-duration: 45s !important;
        will-change: transform;
    }
    
</style>
<!-- Shopee Reviews Mobile Slider CSS -->
<style>
@media (max-width: 768px) {
    .shopee-comments-list {
        flex-direction: row;
        overflow-x: auto;
        scroll-snap-type: x mandatory;
        padding-bottom: 20px;
        gap: 15px;
        scrollbar-width: none;
    }
    .shopee-comments-list::-webkit-scrollbar {
        display: none;
    }
    .shopee-comment-item {
        flex: 0 0 85%;
        scroll-snap-align: center;
        border-bottom: none;
        border: 1px solid var(--border-color, #e2e8f0);
        border-radius: 12px;
        padding: 20px;
        background: var(--bg-card, #ffffff);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
}
</style>
<!-- Shopee Reviews Section -->`
);

fs.writeFileSync('index.bwt', bodyContent, 'utf8');
console.log("index.bwt regenerated successfully.");
