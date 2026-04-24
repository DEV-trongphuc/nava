const fs = require('fs');

// 1. Inject HTML
const htmlPath = 'f:/BAO_SAPO/sapo_new/index.html';
let html = fs.readFileSync(htmlPath, 'utf8');

const aiHtml = `    <!-- ===== AI CORE SECTION ===== -->
    <section class="ai-core-section">
        <div class="ai-container">
            <div class="ai-orb-wrapper reveal">
                <div class="ai-orb" id="aiOrb">
                    <div class="ai-orb-core"></div>
                    <div class="ai-orb-glow"></div>
                    <div class="ai-orb-ring ring-1"></div>
                    <div class="ai-orb-ring ring-2"></div>
                </div>
                <div class="ai-content">
                    <div class="bench-badge"><i class="ph-fill ph-cpu"></i> SỨC MẠNH NPU</div>
                    <h2 class="ai-title cyber-glitch" data-text="LÕI NĂNG LƯỢNG AI">LÕI NĂNG LƯỢNG AI</h2>
                    <p class="ai-desc">Trí tuệ nhân tạo được tích hợp sâu vào kiến trúc phần cứng. Xử lý lên đến 50+ TOPS, sẵn sàng cho mọi tác vụ Machine Learning hạng nặng ngay trên bàn làm việc của bạn.</p>
                    <a href="https://navastore.vn/" class="btn-glass ai-btn">Khám phá sức mạnh <i class="ph-bold ph-arrow-right"></i></a>
                </div>
            </div>
        </div>
    </section>
`;

html = html.replace('    <footer class="footer">', aiHtml + '\n    <footer class="footer">');

// Update cache busting
html = html.replace('assets/style.css?v=20260423i', 'assets/style.css?v=20260423k');
fs.writeFileSync(htmlPath, html);

// 2. Append CSS
const cssAppends = `
/* ============================================
   AI CORE SECTION
   ============================================ */
.ai-core-section {
    position: relative;
    padding: 100px 0;
    background: #050505;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
    border-top: 1px solid rgba(0, 210, 255, 0.1);
}

.ai-container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    position: relative;
    z-index: 2;
    display: flex;
    justify-content: center;
}

.ai-orb-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 40px;
    text-align: center;
}

.ai-content {
    max-width: 600px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.ai-title {
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 15px;
    background: linear-gradient(90deg, #00d2ff, #3a7bd5, #b224ef);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.ai-desc {
    color: var(--text-gray);
    font-size: 1.1rem;
    line-height: 1.6;
    margin-bottom: 30px;
}

/* Orb Design */
.ai-orb {
    position: relative;
    width: 250px;
    height: 250px;
    display: flex;
    justify-content: center;
    align-items: center;
    transition: transform 0.15s ease-out;
}

.ai-orb-core {
    width: 100px;
    height: 100px;
    background: radial-gradient(circle, #fff 0%, #00d2ff 40%, transparent 80%);
    border-radius: 50%;
    box-shadow: 0 0 50px #00d2ff, inset 0 0 20px #fff;
    animation: pulse-core 2s infinite alternate;
    z-index: 5;
}

.ai-orb-glow {
    position: absolute;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle, rgba(0, 210, 255, 0.4) 0%, rgba(178, 36, 239, 0.2) 40%, transparent 70%);
    border-radius: 50%;
    filter: blur(20px);
    mix-blend-mode: screen;
    animation: pulse-glow 4s infinite alternate;
    z-index: 1;
}

.ai-orb-ring {
    position: absolute;
    border-radius: 50%;
    border: 2px solid rgba(0, 210, 255, 0.3);
    border-top-color: #00d2ff;
    border-bottom-color: #b224ef;
    z-index: 2;
}

.ring-1 {
    width: 180px;
    height: 180px;
    animation: rotate-ring 6s linear infinite;
}

.ring-2 {
    width: 220px;
    height: 220px;
    border-width: 1px;
    border-left-color: #00d2ff;
    border-right-color: transparent;
    border-top-color: transparent;
    border-bottom-color: transparent;
    animation: rotate-ring 10s linear infinite reverse;
}

@keyframes pulse-core {
    0% { transform: scale(0.9); box-shadow: 0 0 30px #00d2ff; }
    100% { transform: scale(1.1); box-shadow: 0 0 80px #00d2ff, 0 0 20px #fff; }
}

@keyframes pulse-glow {
    0% { transform: scale(0.8); opacity: 0.5; }
    100% { transform: scale(1.2); opacity: 1; }
}

@keyframes rotate-ring {
    0% { transform: rotate(0deg) scale(1) rotateX(60deg) rotateY(10deg); }
    50% { transform: rotate(180deg) scale(1.1) rotateX(60deg) rotateY(10deg); }
    100% { transform: rotate(360deg) scale(1) rotateX(60deg) rotateY(10deg); }
}

[data-theme="light"] .ai-core-section {
    background: #f5f7fa;
    border-top: 1px solid rgba(0, 210, 255, 0.2);
}
[data-theme="light"] .ai-title {
    background: linear-gradient(90deg, #0056b3, #b224ef);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
`;
fs.appendFileSync('f:/BAO_SAPO/sapo_new/assets/style.css', '\n' + cssAppends);

// 3. Update JS
const jsPath = 'f:/BAO_SAPO/sapo_new/assets/main.js';
let js = fs.readFileSync(jsPath, 'utf8');

const jsAppends = `
    // ============================================
    // 13. AI CORE ORB INTERACTION
    // ============================================
    const aiSection = document.querySelector('.ai-core-section');
    const aiOrb = document.getElementById('aiOrb');
    
    if (aiSection && aiOrb && typeof isTouchDevice !== 'undefined' && !isTouchDevice) {
        aiSection.addEventListener('mousemove', (e) => {
            const rect = aiSection.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const moveX = (x - centerX) / centerX;
            const moveY = (y - centerY) / centerY;
            
            aiOrb.style.transform = \`translate(\${moveX * 30}px, \${moveY * 30}px)\`;
        });
        
        aiSection.addEventListener('mouseleave', () => {
            aiOrb.style.transform = \`translate(0px, 0px)\`;
        });
    }
`;

js = js.replace('\n});\n', jsAppends + '\n});\n');
fs.writeFileSync(jsPath, js);

console.log('AI Core section injected successfully.');
