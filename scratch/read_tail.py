import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/ssd24_live.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Tail of ssd24_live.html (total {len(lines)} lines):")
start_line = max(1, len(lines) - 150)
for i in range(start_line - 1, len(lines)):
    print(f"{i+1}: {lines[i].rstrip()}")
