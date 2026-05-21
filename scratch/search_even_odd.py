import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"f:\BAO_SAPO\sapo_new\build_demos.py", "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        if "nth-child" in line or "nth-of-type" in line or "even" in line or "odd" in line:
            print(f"{i}: {line.strip()[:150]}")
