const fs = require('fs');

function fixTilt() {
    const filename = 'index.bwt';
    if (!fs.existsSync(filename)) return;
    let content = fs.readFileSync(filename, 'utf8');

    // 1. Remove static transform from :hover
    content = content.replace(
        /transform: rotateX\(8deg\) rotateY\(-8deg\) !important;/g,
        ''
    );

    // 2. Add dynamic tilt JS at the end of the file, just before </div> <!-- /MASTER SAPO ESCAPE WRAPPER -->
    const tiltScript = `
        <!-- Dynamic 3D Tilt Script for Benefit Cards -->
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                const cards = document.querySelectorAll('.benefit-card-mini, .policy-card');
                
                cards.forEach(card => {
                    // Set smooth transition for return to center
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
                        
                        // Remove transition while moving for instant follow, but keep a tiny ease to prevent jitter
                        card.style.transition = 'transform 0.1s ease-out, box-shadow 0.4s ease';
                        card.style.transform = \`perspective(1000px) rotateX(\${rotateX}deg) rotateY(\${rotateY}deg) scale3d(1.02, 1.02, 1.02)\`;
                    });
                    
                    card.addEventListener('mouseleave', () => {
                        // Restore smooth transition when mouse leaves
                        card.style.transition = 'transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease';
                        card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
                    });
                });
            });
        </script>
        `;

    // Only inject if not already injected
    if (!content.includes('Dynamic 3D Tilt Script')) {
        content = content.replace(
            /<\/div>\s*<!-- \/MASTER SAPO ESCAPE WRAPPER -->/,
            tiltScript + '\n        </div>\n         <!-- /MASTER SAPO ESCAPE WRAPPER -->'
        );
    }

    fs.writeFileSync(filename, content);
    console.log(filename + ' updated with dynamic tilt.');
}

fixTilt();
