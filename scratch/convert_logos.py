import os
from PIL import Image

icon_dir = r"f:\BAO_SAPO\sapo_new\assets\icon"

# Convert ppt_logo.webp -> ppt_logo.jpg
try:
    ppt_webp = os.path.join(icon_dir, "ppt_logo.webp")
    ppt_jpg = os.path.join(icon_dir, "ppt_logo.jpg")
    with Image.open(ppt_webp) as img:
        img.convert("RGB").save(ppt_jpg, "JPEG")
    print("Converted ppt_logo.webp to ppt_logo.jpg successfully")
except Exception as e:
    print(f"Error converting ppt: {e}")

# Convert capcut_logo.png -> capcut_logo.jpg
try:
    capcut_png = os.path.join(icon_dir, "capcut_logo.png")
    capcut_jpg = os.path.join(icon_dir, "capcut_logo.jpg")
    with Image.open(capcut_png) as img:
        img.convert("RGB").save(capcut_jpg, "JPEG")
    print("Converted capcut_logo.png to capcut_logo.jpg successfully")
except Exception as e:
    print(f"Error converting capcut: {e}")

# Convert claude_ai logo.webp -> claude_ai.jpg / claude_ai_logo.jpg
try:
    claude_webp = os.path.join(icon_dir, "claude_ai logo.webp")
    claude_jpg = os.path.join(icon_dir, "claude_ai.jpg")
    claude_logo_jpg = os.path.join(icon_dir, "claude_ai_logo.jpg")
    with Image.open(claude_webp) as img:
        img.convert("RGB").save(claude_jpg, "JPEG")
        img.convert("RGB").save(claude_logo_jpg, "JPEG")
    print("Converted claude_ai logo.webp to claude_ai.jpg successfully")
except Exception as e:
    print(f"Error converting claude: {e}")
