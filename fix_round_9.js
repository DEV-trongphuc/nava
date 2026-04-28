const fs = require('fs');

function injectTiltScript() {
    const filename = 'index.bwt';
    if (!fs.existsSync(filename)) return;
    let content = fs.readFileSync(filename, 'utf8');

    const tiltScript = `
        <!-- Dynamic 3D Tilt Script for Benefit Cards -->
        <script>
            (function() {
                function initTilt() {
                    const cards = document.querySelectorAll('.benefit-card-mini, .policy-card');
                    if (cards.length === 0) return; // Prevent errors if elements don't exist yet
                    
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
                            // Use setProperty with important to ensure it overrides any other CSS
                            card.style.setProperty('transform', \`perspective(1000px) rotateX(\${rotateX}deg) rotateY(\${rotateY}deg) scale3d(1.02, 1.02, 1.02)\`, 'important');
                        });
                        
                        card.addEventListener('mouseleave', () => {
                            card.style.transition = 'transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease';
                            card.style.setProperty('transform', 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)', 'important');
                        });
                    });
                }
                
                // Run immediately
                initTilt();
                // Also run on DOMContentLoaded just in case
                if (document.readyState === 'loading') {
                    document.addEventListener('DOMContentLoaded', initTilt);
                }
            })();
        </script>
        `;

    if (!content.includes('Dynamic 3D Tilt Script')) {
        // Append to the end of the file
        content += '\\n' + tiltScript;
        fs.writeFileSync(filename, content);
        console.log('Tilt script injected at the end of the file!');
    } else {
        console.log('Script already exists.');
    }
}

injectTiltScript();
