with open("assets/main.js", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split('\n')
for i, line in enumerate(lines):
    if 'navastore.vn/cart.js' in line:
        print(f"Line {i+1}: {line}")
