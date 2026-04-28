const fs = require('fs');

function processFile(filename) {
    if (!fs.existsSync(filename)) return;
    let content = fs.readFileSync(filename, 'utf8');

    // Add id to the first video thumb
    const targetHtml = `<div class="video-thumb">
                        <img src="https://img.youtube.com/vi/Syk0rwciis4/maxresdefault.jpg"`;
    const replacementHtml = `<div class="video-thumb" id="first-video-thumb">
                        <img src="https://img.youtube.com/vi/Syk0rwciis4/maxresdefault.jpg"`;
    
    if (content.includes(targetHtml)) {
        content = content.replace(targetHtml, replacementHtml);
    }

    // Add Intersection Observer script at the end of the file before </body>
    const observerScript = `
    <!-- Auto-play first video -->
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const firstVideoThumb = document.getElementById('first-video-thumb');
            if (firstVideoThumb) {
                const observer = new IntersectionObserver((entries) => {
                    if(entries[0].isIntersecting) {
                        firstVideoThumb.innerHTML = '<iframe width="100%" height="100%" src="https://www.youtube.com/embed/Syk0rwciis4?autoplay=1&mute=1&controls=1&rel=0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen style="position:absolute; top:0; left:0; width:100%; height:100%; z-index: 10;"></iframe>';
                        observer.disconnect();
                    }
                }, { threshold: 0.5 });
                observer.observe(firstVideoThumb);
            }
        });
    </script>
</body>`;

    if (!content.includes('Auto-play first video')) {
        content = content.replace('</body>', observerScript);
    }

    fs.writeFileSync(filename, content);
    console.log(filename + ' updated.');
}

processFile('index.html');
processFile('index.bwt');
processFile('update_index_bwt.js');
