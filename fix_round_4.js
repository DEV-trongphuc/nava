const fs = require('fs');

function fixBwt() {
    const filename = 'index.bwt';
    if (!fs.existsSync(filename)) return;
    let content = fs.readFileSync(filename, 'utf8');

    // 1. Benefit Card Hover
    content = content.replace(
        /transform: translateY\(-8px\) rotateX\(4deg\) rotateY\(-4deg\) scale\(1\.03\) !important;/g,
        'transform: rotateX(8deg) rotateY(-8deg) !important;'
    );

    // 2. Social wrapper bottom position and fade
    content = content.replace(
        /\.floating-social-wrapper \{\s*position: fixed;\s*bottom: 30px;\s*right: 20px;/g,
        '.floating-social-wrapper {\n            position: fixed;\n            bottom: 20px;\n            right: 20px;'
    );
    
    // Replace fab-menu transition
    const oldFabMenu = `        .fab-menu {
            position: absolute;
            bottom: 60px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            opacity: 0;
            visibility: hidden;
            transform: translateY(20px);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            pointer-events: none;
        }
        .fab-menu.active {
            opacity: 1;
            visibility: visible;
            transform: translateY(0);
            pointer-events: auto;
        }`;
        
    const newFabMenu = `        .fab-menu {
            position: absolute;
            bottom: 60px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.3s ease, visibility 0.3s ease;
            pointer-events: none;
        }
        .fab-menu.active {
            opacity: 1;
            visibility: visible;
            pointer-events: auto;
        }`;
    content = content.replace(oldFabMenu, newFabMenu);


    // 3. First Video Iframe
    const oldFirstVideo = `<div class="video-card reveal">
                <a href="https://www.youtube.com/watch?v=Syk0rwciis4" target="_blank" class="video-card-link">
                    <div class="video-thumb" id="first-video-thumb">
                        <img src="https://img.youtube.com/vi/Syk0rwciis4/maxresdefault.jpg" alt="Lại một em Mini PC đến từ nhà GMKtec | Review GMKtec M7 cùng Nava" loading="lazy" decoding="async">
                        <div class="play-btn"><i class="ph-fill ph-play"></i></div>
                    </div>
                    <div class="video-info">
                        <h3>Lại một em Mini PC đến từ nhà GMKtec | Review GMKtec M7 cùng Nava</h3>
                    </div>
                </a>
            </div>`;
            
    const newFirstVideo = `<div class="video-card reveal">
                <a href="https://www.youtube.com/watch?v=Syk0rwciis4" target="_blank" class="video-card-link" style="pointer-events: none;">
                    <div class="video-thumb" style="padding-top: 56.25%; position: relative;">
                        <iframe width="100%" height="100%" src="https://www.youtube.com/embed/Syk0rwciis4?autoplay=1&mute=1&controls=1&rel=0&loop=1&playlist=Syk0rwciis4" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen style="position:absolute; top:0; left:0; width:100%; height:100%; pointer-events: auto; border-radius: 8px 8px 0 0;"></iframe>
                    </div>
                    <div class="video-info" style="pointer-events: auto;">
                        <h3>Lại một em Mini PC đến từ nhà GMKtec | Review GMKtec M7 cùng Nava</h3>
                    </div>
                </a>
            </div>`;

    if (content.includes('id="first-video-thumb"')) {
        content = content.replace(oldFirstVideo, newFirstVideo);
    }

    fs.writeFileSync(filename, content);
    console.log(filename + ' updated.');
}

fixBwt();
