const fs = require('fs');

const styleFile = 'f:/BAO_SAPO/sapo_new/assets/style.css';
let css = fs.readFileSync(styleFile, 'utf8');

const missingCss = `

/* TASK 2: FAB Menu (Restored) */
.floating-social-wrapper {
    position: fixed;
    bottom: 110px;
    right: 20px;
    z-index: 999999;
    display: flex;
    flex-direction: column-reverse;
    align-items: center;
    gap: 10px;
}

.fab-main {
    width: 50px; height: 50px;
    border-radius: 50%;
    background: var(--bg-white);
    color: var(--primary);
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    box-shadow: 0 5px 15px rgba(0,0,0,0.15);
    transition: 0.3s;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    overflow: hidden;
}

.fab-cycle-img {
    position: absolute;
    width: 35px; height: 35px;
    object-fit: contain;
    opacity: 0;
    transform: scale(0.5);
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}
.fab-cycle-img.active {
    opacity: 1;
    transform: scale(1);
}

.fab-menu {
    display: flex;
    flex-direction: column-reverse;
    gap: 10px;
    opacity: 0;
    visibility: hidden;
    transform: translateY(20px);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.fab-menu.active {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
}

.fab-item {
    width: 44px; height: 44px;
    border-radius: 50%;
    background: var(--bg-white);
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    transition: 0.2s;
    overflow: hidden;
    padding: 0;
}

.fab-item img {
    width: 32px; height: 32px;
    object-fit: contain;
    border-radius: 50%;
}

.fab-item:hover {
    transform: scale(1.1);
}
`;

css += missingCss;

fs.writeFileSync(styleFile, css);
console.log('Restored missing FAB CSS');
