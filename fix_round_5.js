const fs = require('fs');

function fixAll() {
    const filename = 'index.bwt';
    if (!fs.existsSync(filename)) return;
    let content = fs.readFileSync(filename, 'utf8');

    // 1. Benefit slider vertical slide
    content = content.replace(
        /transform: translateX\(100%\);/g,
        'transform: translateY(100%);'
    );
    content = content.replace(
        /transform: translateX\(0\);/g,
        'transform: translateY(0);'
    );
    content = content.replace(
        /transform: translateX\(-100%\);/g,
        'transform: translateY(-100%);'
    );
    
    // 2. Fix social wrapper position (add !important)
    content = content.replace(
        /\.floating-social-wrapper \{\s*position: fixed;\s*bottom: 20px;\s*right: 20px;/g,
        '.floating-social-wrapper {\n            position: fixed !important;\n            bottom: 20px !important;\n            right: 20px !important;'
    );

    // 3. First Video Iframe
    // Because white space varies, I'll use regex to match the first video card block
    const videoRegex = /<div class="video-card reveal">\s*<a href="https:\/\/www\.youtube\.com\/watch\?v=Syk0rwciis4" target="_blank" class="video-card-link">\s*<div class="video-thumb"[^>]*>\s*<img src="https:\/\/img\.youtube\.com\/vi\/Syk0rwciis4\/maxresdefault\.jpg"[^>]*>\s*<div class="play-btn"><i class="ph-fill ph-play"><\/i><\/div>\s*<\/div>\s*<div class="video-info">\s*<h3>Lại một em Mini PC đến từ nhà GMKtec \| Review GMKtec M7 cùng Nava<\/h3>\s*<\/div>\s*<\/a>\s*<\/div>/;

    const newFirstVideo = `<div class="video-card reveal">
                <div class="video-thumb" style="padding-top: 56.25%; position: relative;">
                    <iframe width="100%" height="100%" src="https://www.youtube.com/embed/Syk0rwciis4?autoplay=1&mute=1&controls=1&rel=0&loop=1&playlist=Syk0rwciis4" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen style="position:absolute; top:0; left:0; width:100%; height:100%; border-radius: 8px 8px 0 0;"></iframe>
                </div>
                <a href="https://www.youtube.com/watch?v=Syk0rwciis4" target="_blank" class="video-card-link" style="display: block;">
                    <div class="video-info">
                        <h3>Lại một em Mini PC đến từ nhà GMKtec | Review GMKtec M7 cùng Nava</h3>
                    </div>
                </a>
            </div>`;

    if (videoRegex.test(content)) {
        content = content.replace(videoRegex, newFirstVideo);
    } else {
        console.log("Could not find the first video card to replace.");
    }

    fs.writeFileSync(filename, content);
    console.log(filename + ' updated.');
}

fixAll();
