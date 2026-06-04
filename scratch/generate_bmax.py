from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs("assets", exist_ok=True)

# Create an image with transparent background (RGBA)
# 300x100 for high resolution, downscaled by CSS max-height: 24px
width, height = 300, 100
image = Image.new("RGBA", (width, height), (255, 255, 255, 0))

draw = ImageDraw.Draw(image)

# Try using a standard system font, e.g., Arial Bold, Trebuchet MS Bold, or generic sans-serif
font_paths = [
    "C:\\Windows\\Fonts\\arialbd.ttf",       # Arial Bold
    "C:\\Windows\\Fonts\\trebucbd.ttf",      # Trebuchet MS Bold
    "C:\\Windows\\Fonts\\segoeuib.ttf",      # Segoe UI Bold
    "C:\\Windows\\Fonts\\tahomabd.ttf"       # Tahoma Bold
]

font = None
for path in font_paths:
    if os.path.exists(path):
        try:
            font = ImageFont.truetype(path, 52)
            break
        except Exception:
            continue

if font is None:
    font = ImageFont.load_default()

# Get text bounding box for centering
text = "BMAX"
try:
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
except AttributeError:
    # Fallback for older Pillow versions
    text_width, text_height = draw.textsize(text, font=font)

x = (width - text_width) // 2
y = (height - text_height) // 2 - 10 # slightly adjust vertically

# Draw text in a modern dark charcoal gray (similar to ASUS/Beelink text branding)
draw.text((x, y), text, fill=(15, 23, 42, 255), font=font)

# Save the image
image.save("assets/bmax.png", "PNG")
print("Bmax logo generated successfully at assets/bmax.png")
