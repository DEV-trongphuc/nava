const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

const oldHtml = `<div class="header-callout-pill" style="display: flex; align-items: center; gap: 15px; background: white; padding: 12px 25px; border-radius: 9999px; border: 1px dashed var(--border-color); box-shadow: 0 4px 15px rgba(0,0,0,0.03); max-width: 500px; text-align: left;">
                    <div style="background: rgba(0, 51, 102, 0.08); padding: 10px; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                        <i class="ph-fill ph-target" style="font-size: 1.4rem; color: var(--primary);"></i>
                    </div>
                    <p style="margin: 0; font-size: 0.95rem; color: var(--text-gray); line-height: 1.5;">Các giải pháp chuyên biệt từ <strong style="color: var(--primary); font-weight: 800;">NAVA STORE</strong> đáp ứng hoàn hảo hai nhóm nhu cầu lớn nhất.</p>
                </div>`;

const newHtml = `<div class="header-callout-pill">
                    <div class="callout-icon">
                        <i class="ph-fill ph-target"></i>
                    </div>
                    <p>Các giải pháp chuyên biệt từ <strong>NAVA STORE</strong> đáp ứng hoàn hảo hai nhóm nhu cầu lớn nhất.</p>
                </div>`;

if (html.includes(oldHtml)) {
    html = html.replace(oldHtml, newHtml);
    fs.writeFileSync('index.html', html);
    console.log('replaced html');
} else {
    console.log('could not find old html');
}

let css = fs.readFileSync('assets/style.css', 'utf8');

const calloutCss = `

/* Header Callout Pill */
.header-callout-pill {
    display: flex;
    align-items: center;
    gap: 15px;
    background: white;
    padding: 12px 25px;
    border-radius: 9999px;
    border: 1px dashed var(--border-color);
    box-shadow: 0 4px 15px rgba(0,0,0,0.03);
    max-width: 500px;
    text-align: left;
}

.header-callout-pill .callout-icon {
    background: rgba(0, 51, 102, 0.08);
    padding: 10px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.header-callout-pill .callout-icon i {
    font-size: 1.4rem;
    color: var(--primary);
}

.header-callout-pill p {
    margin: 0;
    font-size: 0.95rem;
    color: var(--text-gray);
    line-height: 1.5;
}

.header-callout-pill strong {
    color: var(--primary);
    font-weight: 800;
}
`;

if (!css.includes('.header-callout-pill {')) {
    css += calloutCss;
    fs.writeFileSync('assets/style.css', css);
    console.log('appended css');
}

const mediaQueryTarget = `.section-header {
        flex-direction: column;
        text-align: center;
        gap: 10px;
        margin-bottom: 30px;
    }`;

const responsiveCss = `
    .section-header {
        flex-direction: column;
        text-align: center;
        gap: 20px;
        margin-bottom: 30px;
    }

    .header-callout-pill {
        flex-direction: column;
        text-align: center;
        padding: 20px;
        border-radius: var(--radius-lg);
        gap: 10px;
    }`;

if (css.includes(mediaQueryTarget) && !css.includes('flex-direction: column;\n        text-align: center;\n        padding: 20px;')) {
    css = css.replace(mediaQueryTarget, responsiveCss);
    fs.writeFileSync('assets/style.css', css);
    console.log('added responsive css');
}
