import re

with open("assets/main.js", "r", encoding="utf-8") as f:
    code = f.read()

# We will count brace levels
level = 0
lines = code.split('\n')
for idx, line in enumerate(lines):
    # remove comments and string literals to be safe
    line_clean = re.sub(r'//.*', '', line)
    line_clean = re.sub(r'".*?"', '""', line_clean)
    line_clean = re.sub(r"'.*?'", "''", line_clean)
    
    opens = line_clean.count('{')
    closes = line_clean.count('}')
    
    old_level = level
    level += opens - closes
    if level < 0:
        print(f"Line {idx+1} drops level below 0: {line}")
        level = 0

print(f"Final brace level: {level}")
