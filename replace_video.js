const fs = require('fs');

const filename = 'index.bwt';
let content = fs.readFileSync(filename, 'utf8');

const targetHtml = `            <div class="video-card reveal">
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

const newHtml = `            <div class="video-card reveal">
                <div class="video-thumb" style="padding-top: 56.25%; position: relative;">
                    <iframe width="100%" height="100%" src="https://www.youtube.com/embed/Syk0rwciis4?autoplay=1&mute=1&controls=1&rel=0&loop=1&playlist=Syk0rwciis4" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen style="position:absolute; top:0; left:0; width:100%; height:100%; border-radius: 8px 8px 0 0;"></iframe>
                </div>
                <a href="https://www.youtube.com/watch?v=Syk0rwciis4" target="_blank" class="video-card-link" style="display: block;">
                    <div class="video-info">
                        <h3>Lại một em Mini PC đến từ nhà GMKtec | Review GMKtec M7 cùng Nava</h3>
                    </div>
                </a>
            </div>`;

if (content.includes('id="first-video-thumb"')) {
    content = content.replace(targetHtml, newHtml);
    fs.writeFileSync(filename, content);
    console.log('Replaced successfully');
} else {
    console.log('Could not find target html');
}
