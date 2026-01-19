from PIL import Image
source_image = "assets/ejsolutions.png"
output_icon = "assets/ejsolutions.ico"

# Icon sizes for Windows compatibility
sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]

# Open source image
img = Image.open(source_image).convert("RGBA")

# Save ICO with all sizes
img.save(output_icon, format="ICO", sizes=sizes)

print(f"✅ Icon saved as {output_icon} with sizes {sizes}")
