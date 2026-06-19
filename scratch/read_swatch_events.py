import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/live_scripts.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open("scratch/swatch_events.txt", "w", encoding="utf-8") as out:
    start_line = 2100
    end_line = 2350
    for i in range(start_line-1, min(end_line, len(lines))):
        out.write(f"{i+1}: {lines[i]}")

print("Saved scratch/swatch_events.txt")
