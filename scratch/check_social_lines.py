with open("assets/style.css", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split('\n')
with open("scratch/social_lines.txt", "w", encoding="utf-8") as out:
    for i, line in enumerate(lines):
        if 'floating-social-wrapper' in line:
            out.write(f"Line {i+1}: {line}\n")
            start = max(0, i-5)
            end = min(len(lines), i+6)
            out.write("\n".join(lines[start:end]))
            out.write("\n" + "="*50 + "\n")
print("Done!")
