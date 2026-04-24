const fs = require('fs');
const cssAppends = `
/* ============================================
   TECH ANIMATIONS & CYBER EFFECTS
   ============================================ */

/* 1. 3D Tilt & Glare */
.glare {
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.3s ease;
    z-index: 10;
}

.product-card, .bento-box {
    transition: transform 0.15s cubic-bezier(0.25, 0.46, 0.45, 0.94), box-shadow 0.3s ease;
    transform-style: preserve-3d;
}

/* 2. Magnetic Buttons */
.hero-cta .btn-pill, .social-btn {
    transition: transform 0.15s cubic-bezier(0.25, 0.46, 0.45, 0.94), background-color 0.3s, box-shadow 0.3s;
}

/* 3. Cyber Grid */
.cyber-grid {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
      linear-gradient(to right, rgba(0, 210, 255, 0.05) 1px, transparent 1px),
      linear-gradient(to bottom, rgba(0, 210, 255, 0.05) 1px, transparent 1px);
    background-size: 50px 50px;
    transform: perspective(500px) rotateX(60deg) translateY(-100px) scale(3);
    transform-origin: bottom;
    animation: grid-move 5s linear infinite;
    pointer-events: none;
    z-index: 0;
}
@keyframes grid-move {
    0% { background-position: 0 0; }
    100% { background-position: 0 50px; }
}
[data-theme="dark"] .cyber-grid {
    background-image: 
      linear-gradient(to right, rgba(0, 210, 255, 0.1) 1px, transparent 1px),
      linear-gradient(to bottom, rgba(0, 210, 255, 0.1) 1px, transparent 1px);
}

/* 4. Cyber Glitch Text */
.cyber-glitch {
    position: relative;
    display: inline-block;
}
.cyber-glitch::before, .cyber-glitch::after {
    content: attr(data-text);
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: transparent;
    opacity: 0;
    pointer-events: none;
}
.cyber-glitch:hover::before {
    animation: glitch-anim-1 0.3s infinite linear alternate-reverse;
    left: -2px;
    color: #00d2ff;
    opacity: 0.8;
}
.cyber-glitch:hover::after {
    animation: glitch-anim-2 0.3s infinite linear alternate-reverse;
    left: 2px;
    color: #f43f5e;
    opacity: 0.8;
}

@keyframes glitch-anim-1 {
    0% { clip-path: inset(20% 0 80% 0); }
    20% { clip-path: inset(60% 0 10% 0); }
    40% { clip-path: inset(40% 0 50% 0); }
    60% { clip-path: inset(80% 0 5% 0); }
    80% { clip-path: inset(10% 0 70% 0); }
    100% { clip-path: inset(30% 0 20% 0); }
}
@keyframes glitch-anim-2 {
    0% { clip-path: inset(10% 0 60% 0); }
    20% { clip-path: inset(30% 0 20% 0); }
    40% { clip-path: inset(70% 0 10% 0); }
    60% { clip-path: inset(20% 0 50% 0); }
    80% { clip-path: inset(50% 0 30% 0); }
    100% { clip-path: inset(5% 0 80% 0); }
}
`;
fs.appendFileSync('f:/BAO_SAPO/sapo_new/assets/style.css', '\n' + cssAppends);
console.log("Appended CSS successfully");
