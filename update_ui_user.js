const fs = require('fs');

function processFile(filename) {
    if (!fs.existsSync(filename)) return;
    let content = fs.readFileSync(filename, 'utf8');

    // Remove Testimonial Section (watch out for exact string match)
    // We will just remove from "<!-- Testimonial Section -->" to the next "</section>"
    content = content.replace(/<!-- Testimonial Section -->[\s\S]*?<\/section>/gi, '');

    fs.writeFileSync(filename, content);
    console.log(filename + ' updated.');
}

processFile('index.html');
processFile('index.bwt');
processFile('update_index_bwt.js');

console.log('Removed Testimonial Section successfully!');
