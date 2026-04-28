import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_html = """                        <div class="terminal-box" id="benchTerminal">
                            <div class="terminal-header">
                                <span class="t-dot red"></span>
                                <span class="t-dot yellow"></span>
                                <span class="t-dot green"></span>
                                <span class="t-title">nava_benchmark.sh</span>
                            </div>
                            <div class="terminal-body" id="terminalOutput"></div>
                        </div>"""

new_html = """                        <div class="specs-box">
                            <div class="specs-header">
                                <i class="ph-fill ph-cpu"></i> Thông số kỹ thuật Asus NUC AI 350
                            </div>
                            <div class="specs-body">
                                <table class="specs-table">
                                    <tbody>
                                        <tr><td>Thương hiệu</td><td>Asus</td></tr>
                                        <tr><td>Model</td><td>NUC AI 350 (PN54)</td></tr>
                                        <tr><td>Tình trạng</td><td>Mới 100%</td></tr>
                                        <tr><td>Kích thước</td><td>130x130x34mm</td></tr>
                                        <tr><td>CPU</td><td>AMD Ryzen AI 7 350 8C/16T max 5.0Ghz<br><small>CPU Mark: 30.000</small></td></tr>
                                        <tr><td>GPU</td><td>AMD Radeon™ 860M<br><small>G3D Mark: 8.500</small></td></tr>
                                        <tr><td>Ram</td><td>2x DDR5 5600 tối đa 128GB</td></tr>
                                        <tr><td>SSD</td><td>2x M.2 2280 NVMe</td></tr>
                                        <tr><td>Kết nối không dây</td><td>Wi-Fi 6E (Gig+) 2x2 + Bluetooth® 5.4</td></tr>
                                        <tr><td>Cổng IO</td><td>1x USB 4<br>1x USB 3.2 Gen2 Type A (10G)<br>1x USB 2.0 Type A (5G)<br>1x HDMI2.1(FRL6)<br>2x DisplayPort 1.4<br>1x 2.5G RJ45 LAN<br>1x DC in</td></tr>
                                        <tr><td>Power</td><td>DC 120W</td></tr>
                                        <tr><td>Tính năng đặc biệt</td><td>Vân tay, Copilot+, lên đến 66 TOPS</td></tr>
                                        <tr><td>OS</td><td>Win 11 Pro, Office 2021</td></tr>
                                        <tr><td>Bảo hành</td><td>36 tháng</td></tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>"""

html_regex = re.compile(re.escape(old_html).replace(r'\n', r'\r?\n'))
content = html_regex.sub(new_html, content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Now append CSS to style.css
css_to_append = """

/* --- SPECS BOX REDESIGN --- */
.specs-box {
    background: var(--bg-white);
    border-radius: var(--radius-md);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
    border: 1px solid var(--border-color);
    overflow: hidden;
    height: 100%;
}
.specs-header {
    background: #f8fafc;
    padding: 15px 20px;
    font-weight: 800;
    font-size: 1.1rem;
    color: var(--text-dark);
    display: flex;
    align-items: center;
    gap: 10px;
    border-bottom: 1px solid var(--border-color);
}
.specs-header i {
    color: var(--primary);
    font-size: 1.5rem;
}
.specs-body {
    padding: 20px;
}
.specs-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9rem;
}
.specs-table td {
    padding: 8px 0;
    border-bottom: 1px dashed var(--border-color);
    vertical-align: top;
    line-height: 1.4;
}
.specs-table tr:last-child td {
    border-bottom: none;
}
.specs-table td:first-child {
    font-weight: 600;
    color: var(--text-dark);
    width: 35%;
    padding-right: 15px;
}
.specs-table td:last-child {
    color: var(--text-gray);
}
.specs-table small {
    display: inline-block;
    color: #ef4444; /* red/orange for benchmark */
    font-weight: 600;
    margin-top: 2px;
    background: rgba(239, 68, 68, 0.1);
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.75rem;
}

[data-theme="dark"] .specs-box {
    background: #111827;
    border-color: rgba(255, 255, 255, 0.05);
}
[data-theme="dark"] .specs-header {
    background: #1e293b;
    color: #f1f5f9;
    border-color: rgba(255, 255, 255, 0.05);
}
[data-theme="dark"] .specs-table td {
    border-color: rgba(255, 255, 255, 0.05);
}
[data-theme="dark"] .specs-table td:first-child {
    color: #e2e8f0;
}
[data-theme="dark"] .specs-table td:last-child {
    color: #94a3b8;
}
"""

with open('assets/style.css', 'a', encoding='utf-8') as f:
    f.write(css_to_append)

print("Specs applied successfully!")
