const fs = require('fs');

function processBwt(filename) {
    if (!fs.existsSync(filename)) return;
    let content = fs.readFileSync(filename, 'utf8');

    // 1. Direct iframe for first video
    const oldFirstVideo = `<a href="https://www.youtube.com/watch?v=Syk0rwciis4" target="_blank" class="video-card-link">
                    <div class="video-thumb" id="first-video-thumb">
                        <img src="https://img.youtube.com/vi/Syk0rwciis4/maxresdefault.jpg" alt="Lại một em Mini PC đến từ nhà GMKtec | Review GMKtec M7 cùng Nava" loading="lazy" decoding="async">
                        <div class="play-btn"><i class="ph-fill ph-play"></i></div>
                    </div>`;
                    
    const newFirstVideo = `<a href="https://www.youtube.com/watch?v=Syk0rwciis4" target="_blank" class="video-card-link" style="pointer-events: none;">
                    <div class="video-thumb" style="padding-top: 56.25%; position: relative;">
                        <iframe width="100%" height="100%" src="https://www.youtube.com/embed/Syk0rwciis4?autoplay=1&mute=1&controls=1&rel=0&loop=1&playlist=Syk0rwciis4" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen style="position:absolute; top:0; left:0; width:100%; height:100%; pointer-events: auto; border-radius: 8px 8px 0 0;"></iframe>
                    </div>`;

    if (content.includes('id="first-video-thumb"')) {
        content = content.replace(oldFirstVideo, newFirstVideo);
    } else {
        // Fallback if ID was not found somehow
        const fallbackOld = `<a href="https://www.youtube.com/watch?v=Syk0rwciis4" target="_blank" class="video-card-link">
                    <div class="video-thumb">
                        <img src="https://img.youtube.com/vi/Syk0rwciis4/maxresdefault.jpg" alt="Lại một em Mini PC đến từ nhà GMKtec | Review GMKtec M7 cùng Nava" loading="lazy" decoding="async">
                        <div class="play-btn"><i class="ph-fill ph-play"></i></div>
                    </div>`;
        content = content.replace(fallbackOld, newFirstVideo);
    }

    // Restore pointer events on the video-info so title is clickable
    const oldVideoInfo = `<div class="video-info">
                        <h3>Lại một em Mini PC đến từ nhà GMKtec | Review GMKtec M7 cùng Nava</h3>`;
    const newVideoInfo = `<div class="video-info" style="pointer-events: auto;">
                        <h3>Lại một em Mini PC đến từ nhà GMKtec | Review GMKtec M7 cùng Nava</h3>`;
    content = content.replace(oldVideoInfo, newVideoInfo);


    // 2. Remove the IntersectionObserver script for autoplay
    content = content.replace(/<!-- Auto-play first video -->[\s\S]*?<\/script>/, '');

    fs.writeFileSync(filename, content);
    console.log(filename + ' updated.');
}

processBwt('index.bwt');
processBwt('index.html');
processBwt('update_index_bwt.js');
