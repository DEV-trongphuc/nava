with open("assets/main.js", "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find("CART DRAWER LOGIC")
if idx != -1:
    with open("scratch/cart_drawer_logic.js", "w", encoding="utf-8") as out:
        out.write(content[idx:idx+5000])
    print("Extracted cart drawer logic!")
else:
    print("Not found!")
