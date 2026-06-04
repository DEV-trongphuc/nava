with open("sapo_BWT_new/layout/theme.bwt", "r", encoding="utf-8") as f:
    theme_content = f.read()

theme_lines = theme_content.split('\n')
with open("scratch/theme_navastore_matches.txt", "w", encoding="utf-8") as out:
    for i, line in enumerate(theme_lines):
        if 'navastore.vn' in line:
            out.write(f"Line {i+1}: {line}\n")
print("Done!")
