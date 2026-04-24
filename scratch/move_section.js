const fs = require('fs');

const path = 'f:/BAO_SAPO/sapo_new/index.html';
const lines = fs.readFileSync(path, 'utf8').split('\n');

let benchStart = -1;
let benchEnd = -1;
let statsStart = -1;

for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes('<!-- ===== PERFORMANCE BENCHMARK SECTION ===== -->')) {
        benchStart = i;
    }
    if (lines[i].includes('<!-- ===== TECH STATS COUNTER SECTION ===== -->')) {
        statsStart = i;
    }
}

if (benchStart !== -1) {
    for (let i = benchStart + 1; i < lines.length; i++) {
        if (lines[i].includes('</section>')) {
            benchEnd = i;
            break;
        }
    }
}

if (benchStart !== -1 && benchEnd !== -1 && statsStart !== -1) {
    // extract block
    const block = lines.splice(benchStart, benchEnd - benchStart + 1);
    
    // adjust statsStart since we removed lines before it
    if (benchStart < statsStart) {
        statsStart -= block.length;
    }
    
    // insert block before statsStart
    lines.splice(statsStart, 0, ...block);
    
    fs.writeFileSync(path, lines.join('\n'));
    console.log('Moved benchmark section successfully');
} else {
    console.log('Could not find sections', {benchStart, benchEnd, statsStart});
}
