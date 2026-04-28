const fs = require('fs');

function injectTiltScript() {
    const filename = 'index.bwt';
    if (!fs.existsSync(filename)) return;
    let content = fs.readFileSync(filename, 'utf8');

    // Make sure we remove any empty transform lines
    content = content.replace(/\.benefit-card-mini:hover\s*\{\s*box-shadow/g, '.benefit-card-mini:hover {\n    box-shadow');
    content = content.replace(/\.policy-card:hover\s*\{\s*box-shadow/g, '.policy-card:hover {\n    box-shadow');

    const tiltScript = `
        <!-- Dynamic 3D Tilt Script for Benefit Cards -->
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                const cards = document.querySelectorAll('.benefit-card-mini, .policy-card');
                
                cards.forEach(card => {
                    card.style.transition = 'transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease';
                    
                    card.addEventListener('mousemove', e => {
                        const rect = card.getBoundingClientRect();
                        const x = e.clientX - rect.left;
                        const y = e.clientY - rect.top;
                        
                        const centerX = rect.width / 2;
                        const centerY = rect.height / 2;
                        
                        // Calculate rotation based on mouse position
                        const rotateX = ((y - centerY) / centerY) * -12; // Max 12 deg tilt
                        const rotateY = ((x - centerX) / centerX) * 12;
                        
                        card.style.transition = 'transform 0.1s ease-out, box-shadow 0.4s ease';
                        card.style.transform = \`perspective(1000px) rotateX(\${rotateX}deg) rotateY(\${rotateY}deg) scale3d(1.02, 1.02, 1.02)\`;
                    });
                    
                    card.addEventListener('mouseleave', () => {
                        card.style.transition = 'transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease';
                        card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
                    });
                });
            });
        </script>
        `;

    if (!content.includes('Dynamic 3D Tilt Script')) {
        content = content.replace(
            /<\/div>\s*<!-- \/MASTER SAPO ESCAPE WRAPPER -->/,
            tiltScript + '\n        </div>\n         <!-- /MASTER SAPO ESCAPE WRAPPER -->'
        );
        fs.writeFileSync(filename, content);
        console.log('Tilt script injected!');
    } else {
        console.log('Script already exists.');
    }
}

injectTiltScript();
