import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"f:\BAO_SAPO\sapo_new\build_demos.py", "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        if "quick-view" in line or "quickview" in line or "openQuickView" in line:
            print(f"{i}: {line.strip()[:150]}")
