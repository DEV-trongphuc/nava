with open("scratch/ssd24_live.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open("scratch/callback_code.txt", "w", encoding="utf-8") as out:
    out.write("=== JS Part 1 (Lines 4900 - 5200) ===\n")
    for i in range(4900-1, min(5200, len(lines))):
        out.write(f"{i+1}: {lines[i]}")
        
    out.write("\n\n=== JS Part 2 (Lines 5400 - 5800) ===\n")
    for i in range(5400-1, min(5800, len(lines))):
        out.write(f"{i+1}: {lines[i]}")
