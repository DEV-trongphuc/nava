const fs = require('fs');

let html = fs.readFileSync('f:/BAO_SAPO/sapo_new/index.html', 'utf8');

// The HTML block we want to move
const fabBlockRegex = /<!-- Floating Social Button -->[\s\S]*?<\/div>(\s*<script>[\s\S]*?<\/script>)?/;
const match = html.match(fabBlockRegex);

if (match) {
    // Remove it from its current place
    html = html.replace(match[0], '');
    
    // Find the end of #nava-master-wrapper
    // The previous script showed it ends with:
    // </div> <!-- /MASTER SAPO ESCAPE WRAPPER -->
    // Let's insert it right before that.
    html = html.replace('    </div> <!-- /MASTER SAPO ESCAPE WRAPPER -->', 
        match[0] + '\n    </div> <!-- /MASTER SAPO ESCAPE WRAPPER -->');
        
    fs.writeFileSync('f:/BAO_SAPO/sapo_new/index.html', html);
    console.log('Moved FAB inside master wrapper');
} else {
    console.log('FAB block not found!');
}
