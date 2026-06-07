import re

with open("C:/Users/AD/.gemini/antigravity-ide/brain/c67fc15a-2f7f-4635-8abd-f2a4ed79f6c7/.system_generated/steps/2317/content.md", "r", encoding="utf-8") as f:
    html = f.read()

# Extract all style blocks
style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', html, re.DOTALL)
print(f"Found {len(style_blocks)} style blocks in HTML.")

for i, block in enumerate(style_blocks):
    if "special-content" in block or "content_coll" in block or "specs" in block:
        print(f"Style Block {i+1} mentions specs/special-content:")
        # Search for rules
        lines = block.split('\n')
        for line in lines:
            if "special-content" in line or "max-height" in line or "overflow" in line or "spec-tables" in line:
                print("  ", line.strip())
        print("-" * 50)
