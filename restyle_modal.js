const fs = require('fs');
let css = fs.readFileSync('assets/style.css', 'utf8');

const oldBlockCSS = `.warranty-block {
    margin-bottom: 30px;
}

.warranty-block h3 {
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--text-dark);
    margin-bottom: 15px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.warranty-block ul {
    list-style: none;
    padding-left: 20px;
}

.warranty-block ul li {
    position: relative;
    color: var(--text-gray);
    margin-bottom: 10px;
    line-height: 1.6;
}

.warranty-block ul > li::before {
    content: "•";
    position: absolute;
    left: -15px;
    color: var(--primary);
    font-weight: bold;
}

.warranty-block ul ul {
    margin-top: 10px;
    margin-bottom: 10px;
    padding-left: 15px;
}

.warranty-block ul ul li::before {
    content: "-";
    color: var(--text-gray);
}`;

const newBlockCSS = `.warranty-modal-content {
    background: var(--bg-gray) !important;
}

.modal-header {
    background: var(--bg-white);
    border-radius: var(--radius-lg) var(--radius-lg) 0 0;
}

.warranty-block {
    background: var(--bg-white);
    padding: 30px;
    border-radius: var(--radius-md);
    border: 1px solid var(--border-color);
    box-shadow: var(--shadow-sm);
    margin-bottom: 25px;
    transition: 0.3s;
}

.warranty-block:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
    border-color: rgba(0, 51, 102, 0.2);
}

.warranty-block h3 {
    font-size: 1.3rem;
    font-weight: 800;
    color: var(--text-dark);
    margin-bottom: 25px;
    display: flex;
    align-items: center;
    gap: 15px;
    padding-bottom: 15px;
    border-bottom: 2px dashed var(--border-color);
    width: 100%;
}

.warranty-block h3 i {
    font-size: 1.8rem;
    background: var(--bg-gray);
    padding: 12px;
    border-radius: 50%;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
}

.warranty-block ul {
    list-style: none;
    padding-left: 0;
}

.warranty-block ul li {
    position: relative;
    color: var(--text-gray);
    margin-bottom: 16px;
    line-height: 1.6;
    padding-left: 35px;
    font-weight: 500;
    font-size: 1.05rem;
}

.warranty-block ul > li::before {
    content: "\\2713";
    position: absolute;
    left: 0;
    top: 3px;
    color: var(--primary);
    font-weight: 900;
    font-size: 0.9rem;
    background: rgba(0, 51, 102, 0.1);
    width: 22px;
    height: 22px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
}

.warranty-block:nth-child(3) ul > li::before {
    content: "\\2715";
    color: #ef4444;
    background: rgba(239, 68, 68, 0.1);
}

.warranty-block ul ul {
    margin-top: 15px;
    margin-bottom: 15px;
    padding-left: 0;
    background: var(--bg-gray);
    padding: 20px;
    border-radius: var(--radius-sm);
    border: 1px solid var(--border-color);
}

.warranty-block ul ul li {
    padding-left: 20px;
    margin-bottom: 10px;
    font-size: 0.95rem;
}

.warranty-block ul ul li:last-child { margin-bottom: 0; }

.warranty-block ul ul li::before {
    content: "\\2023";
    background: none;
    color: var(--primary);
    font-size: 1.5rem;
    top: -4px;
    width: auto; height: auto;
}`;

// I need to be careful not to replace it if it's already replaced
if (css.includes('.warranty-block ul ul li::before {\\n    content: "-";')) {
    css = css.replace(oldBlockCSS, newBlockCSS);
    fs.writeFileSync('assets/style.css', css);
    console.log('done replacing css');
} else {
    // maybe whitespace issue, try splitting by `.warranty-block {`
    const parts = css.split('.warranty-block {');
    if (parts.length > 1) {
        // find where the old css ends
        const endIndex = css.indexOf('.note-block {');
        if (endIndex !== -1) {
            const start = css.indexOf('.warranty-block {');
            const before = css.substring(0, start);
            const after = css.substring(endIndex);
            fs.writeFileSync('assets/style.css', before + newBlockCSS + '\n\n' + after);
            console.log('done replacing css with split');
        } else {
            console.log('note-block not found');
        }
    } else {
        console.log('warranty-block not found');
    }
}
