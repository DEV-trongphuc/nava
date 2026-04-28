import re

with open('assets/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

old_array = """    const terminalLines = [
        { cls: '', html: '<span class="t-prompt">$</span> <span class="t-cmd">run benchmark --device asus-nuc-15-pro</span>' },
        { cls: 't-out', html: '[INFO] CPU: Intel Core Ultra 5 225H' },
        { cls: 't-out', html: '[INFO] RAM: DDR5 5600MHz SODIMM' },
        { cls: 't-out', html: '[INFO] GPU: Intel Arc Graphics' },
        { cls: 't-success', html: '[PASS] Cinebench R24 Multi: <b>24,819 pts</b>' },
        { cls: 't-success', html: '[PASS] CrystalDisk Read: <b>7,412 MB/s</b>' },
        { cls: 't-success', html: '[PASS] LLM Inference: <b>42 tok/s</b>' },
        { cls: 't-warn', html: '[TEMP] Peak Temp: 74°C ✓ Under threshold' },
        { cls: 't-success', html: '[PASS] Total Power Draw: <b>28W</b> ✅' },
        { cls: 't-success', html: '[PASS] Size (Space Saving): <b>2000%</b> ✨' },
        { cls: 't-blink', html: '<span class="t-cursor">█</span> Benchmark complete — Score: <span class="t-highlight">ELITE</span>' },
    ];"""

new_array = """    const terminalLines = [
        { cls: '', html: '<span class="t-prompt">$</span> <span class="t-cmd">fetch-specs --device asus-nuc-ai-350</span>' },
        { cls: 't-out', html: '[INFO] Model: Asus NUC AI 350 (PN54) | Mới 100%' },
        { cls: 't-out', html: '[INFO] CPU: AMD Ryzen AI 7 350 8C/16T max 5.0Ghz' },
        { cls: 't-success', html: '[PASS] CPU Mark: <b>30,000 pts</b>' },
        { cls: 't-out', html: '[INFO] GPU: AMD Radeon™ 860M' },
        { cls: 't-success', html: '[PASS] G3D Mark: <b>8,500 pts</b>' },
        { cls: 't-out', html: '[INFO] RAM: 2x DDR5 5600 (Max 128GB) | SSD: 2x M.2 NVMe' },
        { cls: 't-out', html: '[INFO] IO: USB 4, 10G Type-A, HDMI 2.1, 2x DP 1.4, 2.5G LAN' },
        { cls: 't-out', html: '[INFO] Kết nối: Wi-Fi 6E (Gig+) 2x2 + Bluetooth® 5.4' },
        { cls: 't-out', html: '[INFO] Tính năng: Vân tay, Copilot+, NPU 66 TOPS ✨' },
        { cls: 't-success', html: '[PASS] Bảo hành: <b>36 tháng chính hãng</b> ✅' },
        { cls: 't-blink', html: '<span class="t-cursor">█</span> Specs loaded — Status: <span class="t-highlight">READY</span>' },
    ];"""

# Replace keeping \r\n vs \n in mind
old_array_regex = re.compile(re.escape(old_array).replace(r'\n', r'\r?\n'))
content = old_array_regex.sub(new_array, content)

with open('assets/main.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Main.js terminal lines updated successfully!")
